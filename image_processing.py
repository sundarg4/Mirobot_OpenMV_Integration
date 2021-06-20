
##########################################################
##########################################################
#
#   DIEMENSIONS
#
##########################################################
#
#
#              28.6
#            < - - >
#             _ _ _
#        ^   |     |    ^
#        |   |     |    |
#  24.0  |   |     |    | 23.9
#        |   | _ _ |    |
#
#            < - - >
#              28.5
#
#
#widthdown = 28.5
#widthup = 28.6
#heightleft = 24.0
#heightright = 23.9
##########################################################

import sensor, image, time, pyb, math
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

##########################################################
#
#   Globals
#
##########################################################

# April Tag families to detect
tag_families = 0
tag_families |= image.TAG16H5 # comment out to disable this family
tag_families |= image.TAG25H7 # comment out to disable this family
tag_families |= image.TAG25H9 # comment out to disable this family
tag_families |= image.TAG36H10 # comment out to disable this family
tag_families |= image.TAG36H11 # comment out to disable this family (default family)
tag_families |= image.ARTOOLKIT

# threshold values to find_blob method
white_threshold = (58, 89, -2, 9, -19, 18)
red_threshold = (45, 79, 39, 90, -7, 78)
green_threshold = (31, 81, -88, -27, -51, 41)
blue_threshold = (9, 66, -20, 85, -128, -14)


# color of lines drawn around min area
r = (pyb.rng() % 127) + 128
g = (pyb.rng() % 127) + 128
b = (pyb.rng() % 127) + 128


##########################################################
#
#   Function definitions
#
##########################################################

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
    # Taking 25 samples to improve the chances of finding apriltags
    for iter in range(25):
        img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)

        #finding all the April tags and adding it in the april_tags dictionary with id
        for tag in img.find_apriltags(families=tag_families):
            tag_id = tag.id()
            april_tags.update({tag_id:tag})

    # if we detect all the 4 april tags return true, else false
    if(len(april_tags)==4):
        #print(april_tags)
        return april_tags, True
    else:
        return april_tags, False


def get_roi(april_tags):
    # Initializing x/y min and max.
    x_min = float("inf")
    y_min = float("inf")
    x_max = 0
    y_max = 0

    for tag_id,tag in april_tags.items():

        # The four corners of a april tag
        tag_corners = tag.corners()

        # Iterating the Apriltag's corners and finding the min/max of x and y
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


def upscale_QQVGA_to_QVGA(x,y,w,h):
    return x*2,y*2,w*2,h*2


def mask_april_tags(april_tags):

    for tag_id,tag in april_tags.items():
        x,y,w,h = tag.rect()
        X,Y,W,H = upscale_QQVGA_to_QVGA(x,y,w,h)
        img.draw_rectangle(X-int(W/3),Y-int(H/3),int(W*1.65),int(H*1.65), color=0, fill=True)


def find_blobs(x,y,w,h):
    white_blobs = img.find_blobs([white_threshold], area_threshold=100, merge=False, roi=(x,y,w,h))
    red_blobs = img.find_blobs([red_threshold], area_threshold=100, merge=False, roi=(x,y,w,h))
    green_blobs = img.find_blobs([green_threshold], area_threshold=100, merge=False, roi=(x,y,w,h))
    blue_blobs = img.find_blobs([blue_threshold], area_threshold=100, merge=False, roi=(x,y,w,h))

    return [white_blobs, red_blobs, green_blobs, blue_blobs]


def find_len_of_blobs(blobs):
    length_of_blobs_list = [len(blob) for blob in blobs]
    return length_of_blobs_list


def draw_blobs(blobs):

    for color in blobs:
        for blob in color:
            # The corners of the minimum area rectangle of each blob.
            corners = blob.min_corners()
            c1 = corners[0]
            c2 = corners[1]
            c3 = corners[2]
            c4 = corners[3]

            # Draw lines between each corner. ( color = (r,g,b) )
            img.draw_line(c1[0], c1[1], c2[0], c2[1], color = (255, 255, 0), thickness = 2)
            img.draw_line(c2[0], c2[1], c3[0], c3[1], color = (255, 0, 0), thickness = 2)
            img.draw_line(c3[0], c3[1], c4[0], c4[1], color = (0, 255, 0), thickness = 2)
            img.draw_line(c4[0], c4[1], c1[0], c1[1], color = (0, 0, 255), thickness = 2)

            # Draw a cross in the middle of the blob
            img.draw_cross(blob.cx(), blob.cy(), color=255)


##########################################################
#
#   Main program
#
##########################################################

april_tags_dict = {}
april_tags_dict , calib_result = calibration()

#Check for Calibration malfunction and retry
for iter in range(10):
    if not calib_result:
        april_tags_dict , calib_result = calibration()
        print("Retrying Calibration, Attempt: "+ str(iter+1))
    else:
        break

if (calib_result):

    print("Calibration Success!")

    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)

    sensor.set_auto_gain(False) # must be turned off for color tracking
    sensor.set_auto_whitebal(False) # must be turned off for color tracking


    x,y,w,h = get_roi(april_tags_dict)
    X,Y,W,H = upscale_QQVGA_to_QVGA(x,y,w,h)

    # Draw a rectangle to mark the ROI boundary
    img.draw_rectangle(X,Y,W,H, color=255)

    while(True):
        clock.tick()
        img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
        mask_april_tags(april_tags_dict)
        blobs = find_blobs(X,Y,W,H)
        len_blobs_list = find_len_of_blobs(blobs)
        draw_blobs(blobs)
        print(len_blobs_list)
else:
    print("Calibration Failed!!!. \n Please check camera for lens focus, overheat or april tags obstruction")










