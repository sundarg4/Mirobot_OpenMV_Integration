# Copyright (c) 2021-2021 Björn Andersson <bjorn.s.andersson@hiof.no>
# Copyright (c) 2021-2021 Sundarrajan Gopalakrishnan <>
#
# This work is licensed under the MIT license, see the file LICENSE for details.

# Imports
import sensor, image, time, pyb, math,rpc,struct,utime,network, omv

# Initializes the camera
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# Used by the find_apriltags function.
tag_families = 0
tag_families |= image.TAG16H5
tag_families |= image.TAG25H7
tag_families |= image.TAG25H9
tag_families |= image.TAG36H10
tag_families |= image.TAG36H11
tag_families |= image.ARTOOLKIT

class openmv_remote:
    '''
        Class to remotley send data from the OpenMV to the raspberry pi
    
        ...
        
        Attributes
        ----------
        interface : (rpc.rpc_usb_vcp_slave())
            The interface communicating with the remote caller.
        calibration_success : (bool)
            A bool determing if the calibration of the OpenMV has been successfull or not.
        april_tags : (dict)
           If calibration_success is True then the april tags dictionary will be stored here, to make the script more efficient.
        red_threshold : (int) tuple
            The threshold used for finding red blobs by find_blobs()
        green_threshold : (int) tuple
            The threshold used for finding green blobs by find_blobs()
        blue_threshold : (int) tuple
            The threshold used for finding blue blobs by find_blobs()
    '''
    
    def __init__(self):
        self.interface = rpc.rpc_usb_vcp_slave()
        self.calibration_success = False
        self.april_tags = {}
        self.red_threshold = (16, 57, 50, 84, -55, 59)
        self.green_threshold = (31, 81, -88, -27, -51, 41)
        self.blue_threshold = (9, 66, -20, 85, -128, -14)
        
    def family_name(self, tag):
        '''
            Identifying a tag family.
            
            Parameters
            ----------
                tag : an april tag
             
            Returns
            ----------
                tag family : The family of the april tag
        '''
        if(tag.family() == image.TAG16H5):
            return "TAG16H5"
        if(tag.family() == image.TAG25H7):
            return "TAG25H7"
        if(tag.family() == image.TAG25H9):
            return "TAG25H9"
        if(tag.family() == image.TAG36H10):
            return "TAG36H10"
        if(tag.family() == image.TAG36H11):
            return "TAG36H11"
        if(tag.family() == image.ARTOOLKIT):
            return "ARTOOLKIT"
        
    def calibration(self):
        '''
            Calibrates the camera.
        
            Returns
            ----------
                april_tags (dict) : A dictionary containing the april tags
                calibration_result (bool) : True if successful, False if failed
        '''
        sensor.set_pixformat(sensor.GRAYSCALE)
        sensor.set_framesize(sensor.QQVGA)
        april_tags = {}
        for iter in range(25):
            img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
            for tag in img.find_apriltags(families=tag_families):
                tag_id = tag.id()
                april_tags.update({tag_id:tag})
        if(len(april_tags)==4):
            return april_tags, True
        else:
            return april_tags, False
        
    def get_roi(self, april_tags):
        '''
           Gets the region of interest for where blobs will be detected.
           
           The algorithm loops through all the april tags, finds its corners and loops through them.
          
           For each corner, it's x and y coordinates will be added to each other, If this sum is smaller than 
           x_min + y_min then this will be the new values for x_min and y_min. And vice versa with larger values than x_max + y_max.

           The width of the ROI is then found by subtracting x_min from x_max. The height of the ROI is found by subtracting y_min from y_max.

           The find blobs function that will be fed theese values requires they are integers so therefore they are first rounded 
           and then converted to integers before returning them.

           Importnat to remember is that ROI is found using QQVGA so there is neccessary to call the function upscale_QQVGA_to_QVGA 
           on theese coordinates before using them to find blobs
           
           
            Parameters
            ----------
                april_tags (dict) : a dictionary of april tags
            
            Returns
            ----------
                x_min, y_min, w, h : (x,y) of the top left corner of the and the width and height of ROI.
          
        '''
        x_min = float("inf")
        y_min = float("inf")
        x_max = 0
        y_max = 0
        for tag_id,tag in april_tags.items():
            tag_corners = tag.corners()
            for corner in tag_corners:
                x_val = corner[0]
                y_val = corner[1]
                temp_sum = x_val + y_val
                if (temp_sum < (x_min+y_min)):
                    x_min = x_val
                    y_min = y_val
                if (temp_sum > (x_max+y_max)):
                    x_max = x_val
                    y_max = y_val
        roi_width = int ( round( x_max - x_min ))
        roi_height = int( math.ceil( y_max - y_min ))
        return x_min, y_min, roi_width, roi_height

    def upscale_QQVGA_to_QVGA(self, x,y,w,h):
        '''
            Scales from QQVGA to QVGA

            Parameters
            ----------
                x, y, w, h (int) : coordinates in QQVGA
            
            Returns
            ----------
                x, y, w, h (int) : coordinates in QVGA
        '''
        return x*2,y*2,w*2,h*2

    def find_mode(self, sample):
        return max(set(sample), key=sample.count)

    def mask_april_tags(self, april_tags,img):
        '''
            Masking the april tags by drawing a black rectangle on top of them, to avoid confusion with image processing. 
            Mostly an issue if looking for white blobs.
        
            Parameters
            ----------
                april_tags (dict) : A dictionary of april tags
                img (image) : the image to work on.
            
            Returns
            ----------
                None
        '''
        for tag_id,tag in april_tags.items():
            x,y,w,h = tag.rect()
            X,Y,W,H = self.upscale_QQVGA_to_QVGA(x,y,w,h)
            img.draw_rectangle(X-int(W/3),Y-int(H/3),int(W*1.65),int(H*1.65), color=0, fill=True)

    def find_blobs(self, x,y,w,h,img):
        '''
            Finding blobs with help of the OpenMV function find_blobs()
            https://docs.openmv.io/library/omv.image.html#image.image.Image.image.find_blobs
            
            Parameters
            ----------
                x, y, w, h (int) : The region of interest passed in to the find_blobs()
                img (image) : The image to find blobs in
            
            Returns
            ----------
                blobs (list) : A list of blob lists (red, green, blue)
        '''
        red_blobs = img.find_blobs([self.red_threshold], area_threshold=100, merge=False, roi=(x,y,w,h))
        green_blobs = img.find_blobs([self.green_threshold], area_threshold=100, merge=False, roi=(x,y,w,h))
        blue_blobs = img.find_blobs([self.blue_threshold], area_threshold=100, merge=False, roi=(x,y,w,h))
        return [red_blobs, green_blobs, blue_blobs]

    def get_blob_data(self, blobs):
        '''
            A function to collect all the needed data.

            Loops through the list of blob lists with the enumeration function of python, and so gaining access to both the counter and the list.
            Then loops through each blob in the current blob_list and gets the following data from each blob:

            cx and cy is taken directly from the OpenMV function blob.cx() and blob.cy(). 

            Blob area is similarly gotten straight from blob.area(). 
            Worth noting that this area is not the minimum area. 
            
            The corners of the minimum area are gotten from the inbuilt function blob.min_corners(). 
            Although this function is sligthly unstable in the way it returns the corners. And they are returned as a tuple, 
            which means they are unmutable. Thats why they are appended to a new list, in order to be further proseced on the 
            remote_call.py running on the raspberry pi.

            Gets the color by sending the "color_code" (counter from the first loop) to the function get_color().

            As a sidenote angle of rotation is calculated on in the remote_call.py and not on the OpenMV.

            Parameters
            ----------
                blobs (list) : a list of blob lists (red, green, blue)

            Returns
            ----------
            blob_data_list (list) : A list of blob data, each entry stores the following information about a blob
                                    (cx, cy, area, corners_list, color)
        '''
        blob_data_list = []
        for color_code, blob_list in enumerate(blobs):
            for blob in blob_list:
                cx = blob.cx()
                cy = blob.cy()
                area = blob.area()
                corners_tuple = blob.min_corners()
                corners_list = []
                for corner in corners_tuple:
                    corners_list.append(corner)
                color = self.get_color(color_code)
                blob_data_list.append([cx, cy, area, corners_list, color])
        return blob_data_list

    def get_color(self, color_code):
        '''
            Gets the string representation of a blob color.

            Parameters
            ----------
                color_code (int) : The color code
            
            Returns
            ----------
                The string representation of the code
        '''
        if (color_code == 0):
            return "Red"
        elif (color_code == 1):
            return "Green"
        elif (color_code == 2):
            return "Blue"

    def get_data(self, data):
        '''
            Callback function that gathers data and sends it to the remote caller.

            If calibraion_success is True (the instance variable) then the function will proceed
            with gathering and sending data, skipping calibrating the camera.

            If False, then no data will be gatherd and calibration will be called.

            Data is sent with the OpenMV rpc package. This remote device is the slave device.


            Paraneters
            ----------
                data () : used by the OpenMV rpc to send data
            
            Returns
            ----------
                If calibration_success = True, then the blob data is sent.
                If calibration_success = False, then a message saying "Calibrating will be sent".

        '''
        if (self.calibration_success):
            print("Calibration Success!")
            x,y,w,h = self.get_roi(self.april_tags)
            X,Y,W,H = self.upscale_QQVGA_to_QVGA(x,y,w,h)
            sensor.set_pixformat(sensor.RGB565)
            sensor.set_framesize(sensor.QVGA)
            sensor.set_auto_gain(False)
            sensor.set_auto_whitebal(False)
            img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
            self.mask_april_tags(self.april_tags,img)
            blobs = self.find_blobs(X,Y,W,H,img)
            blob_data_list = self.get_blob_data(blobs)
            bytes_data = str(blob_data_list)
            bytes_data = bytes_data + "apriltag" + str(self.april_tags)
            return struct.pack('{}s'.format(len(bytes_data)), bytes_data)
        else:
            self.april_tags, self.calibration_success = self.calibration()
            return struct.pack('{}s'.format(len("Calibrating")), "Calibrating")

    def register_callback(self, call_back_function):
        '''
            Helper function to register the callback function to the interface.

            Parameters
            ----------
                The function to register

            Returns
            ----------
                None
        '''
        self.interface.register_callback(call_back_function)

# Inisializing the remote object
openmv_one = openmv_remote()

# Regestering the call back function
openmv_one.register_callback(openmv_one.get_data)

# Starting the listening loop, awaiting calls from the remote caller (raspberry pi)
print('Ready To Rock!!!!!!')
openmv_one.interface.loop()
