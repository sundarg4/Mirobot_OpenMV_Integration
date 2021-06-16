####
#
#
# TODO:
#
#  Check calibration function
#  Check ROI function
#  Check return values and loops
#
#  Check main loop.

#  Check draw_blobs and try the new rectangle method!!
#



import sensor, image, time, pyb, math

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# April Tag families to detect
tag_families = 0
tag_families |= image.TAG16H5 # comment out to disable this family
tag_families |= image.TAG25H7 # comment out to disable this family
tag_families |= image.TAG25H9 # comment out to disable this family
tag_families |= image.TAG36H10 # comment out to disable this family
tag_families |= image.TAG36H11 # comment out to disable this family (default family)
tag_families |= image.ARTOOLKIT

# threshold values to find_blob method
w_thresholds = (80, 100, -18, 90, -17, 69)
r_thresholds = (45, 79, 39, 90, -7, 78)
g_thresholds = (37, 86, -105, -22, -45, 71)
#b_thresholds = (9, 29, 10, 86, -69, -15)
b_thresholds = (28, 72, -60, 31, -67, -13)

# color of lines drawn around min area
r = (pyb.rng() % 127) + 128
g = (pyb.rng() % 127) + 128
b = (pyb.rng() % 127) + 128


def family_name(tag):
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

# Detecting April tags and return them in an april_tag dictionary
def calibration():
    # Initialize Apriltags dictionary
    april_tags = {}
    # Taking 10 samples to improve the chances of finding apriltags
    for iter in range(60):
        img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
        #sensor.skip_frames()

        #finding all the April tags and adding it in the april_tags dictionary with id
        for tag in img.find_apriltags(families=tag_families):
            tag_id = tag.id()
            #x = 0
            #y = 0
            #april_tags.update({id:[x,y]})
            april_tags.update({tag_id:tag})

    # if we detect all the 4 april tags return true, else false
    if(len(april_tags)==4):
        print("Calibration Success!")
        #print(april_tags)
        return april_tags, True
    else:
        print("Calibration Failed!")
        return april_tags, False

#returns avg sides of the april tags
def get_average_side_length(s1, s2):
    return (s1 + s2) / 2

def upscale_QQVGA_to_QVGA(x,y,w,h):
    return x*2,y*2,w*2,h*2


def get_roi(april_tags, success):
    if (success):
        #img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
        #sensor.skip_frames()

        x_min = 20000
        y_min = 20000
        x_max = 0
        y_max = 0
        #print("Still alive above NONE")
        min_tag = None
        max_tag = None
        #print("Still alive above loop")

        if(success):
            for tag_id,tag in april_tags.items():
                #id = tag.id()
                print(tag)
                print('\n')
                tag_corners = tag.corners()
                #print(tag_corners)
                #Iterating the Apriltag's corners and finding the min/max of x and y
                for corner in tag_corners:
                    #print(corner)
                    #for corner in cornerList:
                    #print(corner)
                    x_val = corner[0]
                    y_val = corner[1]
                    temp_sum = x_val + y_val
                    if (temp_sum < (x_min+y_min)):
                        x_min = x_val
                        y_min = y_val

                        min_tag = tag
                    if (temp_sum > (x_max+y_max)):
                        x_max = x_val
                        y_max = y_val

                        max_tag = tag

        min_width = min_tag.w()
        min_height = min_tag.h()
        max_width = max_tag.w()
        max_height = max_tag.h()

        min_tag_side_length = get_average_side_length(min_width, min_height)
        max_tag_side_length = get_average_side_length(max_width, max_height)

        y_min = int( round( y_min + min_tag_side_length))
        y_max = int( round(y_max - max_tag_side_length))

        b_width = int ( round( x_max - x_min ))
        b_height =int(  math.ceil( y_max - y_min ))

        print(b_width)
        print(b_height)

        return x_min, y_min+4, b_width, b_height-8


def find_blobs(x,y,w,h):
    #roi=(50,0,200,238)
    w_blobs = img.find_blobs([w_thresholds], area_threshold=100, merge=False, roi=(x,y,w,h))
    r_blobs = img.find_blobs([r_thresholds], area_threshold=100, merge=False, roi=(x,y,w,h))
    g_blobs = img.find_blobs([g_thresholds], area_threshold=100, merge=False, roi=(x,y,w,h))
    b_blobs = img.find_blobs([b_thresholds], area_threshold=100, merge=False, roi=(x,y,w,h))

    red = str(len(r_blobs))
    green = str(len(g_blobs))
    blue = str(len(b_blobs))
    white = str(len(w_blobs))

    return [w_blobs, r_blobs, g_blobs, b_blobs], [red, green, blue, white]


def draw_blobs(blobs, x, y, w, h):
    # Draw blobs
    for c_blob in blobs:
        for blob in c_blob:
            # Draw a rectangle where the blob was found
            corners = blob.min_corners()
            angle = blob.rotation_deg()
            c1 = corners[0]
            c2 = corners[1]
            c3 = corners[2]
            c4 = corners[3]

            img.draw_line(c1[0], c1[1], c2[0], c2[1], color = (r, g, b), thickness = 2)
            img.draw_line(c2[0], c2[1], c3[0], c3[1], color = (r, g, b), thickness = 2)
            img.draw_line(c3[0], c3[1], c4[0], c4[1], color = (r, g, b), thickness = 2)
            img.draw_line(c4[0], c4[1], c1[0], c1[1], color = (r, g, b), thickness = 2)

            img.draw_rectangle(x,y,w,h, color=255)
            # Draw a cross in the middle of the blob
            img.draw_cross(blob.cx(), blob.cy(), color=255)
            print(angle)

april_tags_dict = {}
april_tags_dict , calib_result = calibration()


sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
sensor.skip_frames()


x,y,w,h = get_roi(april_tags_dict , calib_result)
X,Y,W,H = upscale_QQVGA_to_QVGA(x,y,w,h)



while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
    bimg = img.to_bitmap(copy=True).clear().draw_rectangle(100, 100, 200, 200, fill=True, color=1)
    img.mean(2, mask=bimg)
    #img.mask_rectangle([100, 100, 20, 20])
    blobs, len_blobs_list = find_blobs(X,Y,W,H)
    draw_blobs(blobs, X,Y,W,H)











####################### GARBAGE :P #########################



#     get_roi:
#
#       for i in range(5):
#            clock.tick()
#            img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
#            sensor.skip_frames(25)
#            for tag in img.find_apriltags(families=tag_families):
#                if(len(april_tags)>0):
#                    id = tag.id()
#                    list_center = april_tags.get(id)
#                    list_center[0] = list_center[0] + tag.cx()
#                    list_center[1] = list_center[1] + tag.cy()
#                    april_tags.update({id: [list_center[0],list_center[1]]})

       # getting average value of coordinates of the april tag center
#        for key in april_tags:
##            list_center = april_tags.get(key)
 #           list_center[0] = list_center[0]/5
 #           list_center[1] = list_center[1]/5
 #           april_tags.update({key: [list_center[0],list_center[1]]})
 #       print(april_tags)

