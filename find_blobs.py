##########################################################
#
#   CHANGE LOG
#
##########################################################
#
# - Added simple image to better visualize diemensions
#   of the vison set table.
#
# - Cleaned up unused code. If need to change back
#   we can refer to an older version of the script.
#
#
# - Moved the calibration success check out of the
#   get_roi function and out into the main program.
#
# - In get_roi function, changed b_width and b_height
#   for roi_width and roi_height.
#
# - Added some comments
#
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
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
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
w_thresholds = (58, 89, -2, 9, -19, 18)
r_thresholds = (45, 79, 39, 90, -7, 78)
g_thresholds = (31, 81, -88, -27, -51, 41)
b_thresholds = (9, 66, -20, 85, -128, -14)

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
    # Taking 10 samples to improve the chances of finding apriltags
    for iter in range(60):
        img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
        #sensor.skip_frames()

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

##########################################################
#
#  get_roi
#
#
# Finds the region of interest for where cubes are detected.
#
# The algorithm loops through all the april tags,
# finds its corners and loops through them.
#
# For each corner that corners x and y coordinates will be
# added to each other, If this sum is smaller then x_min + y_min
# then this will be the new values for x_min and y_min.
# And vice versa with larger values than x_max + y_max.
#
# The width of the ROI is then found by subtracting x_min from x_max.
# The height of the ROI is found by subtracting y_min from y_max.
#
# The find blobs function that will be fed theese values requires
# they are of the type int so therefore round them and then convert them to
# integers before we return them,
#
# The values returned will be the top left corner of the ROI given by
# x_min and y_min. And also the width and height of the ROI.
#
# Importnat to remember is that ROI is found using QQVGA so
# there is neccessary to call the function upscale_QQVGA_to_QVGA
# on theese coordinates before using them to find blobs.
#
##########################################################
def get_roi(april_tags):
    # Initializing x/y min and max.
    x_min = math.inf
    y_min = math.inf
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
    roi_height = int(  math.ceil( y_max - y_min ))

    return x_min, y_min, roi_width, roi_height


##########################################################
#
# Converts coordinates from QQVGA to QVGA
#
##########################################################

def upscale_QQVGA_to_QVGA(x,y,w,h):
    return x*2,y*2,w*2,h*2

##########################################################
#
#  Masks the april tags so that they wont be detected
#  by the object detection function,
#
##########################################################
def mask_april_tags(april_tags):

    tag_xy = []

    for tag_id,tag in april_tags.items():
        tag_corners = tag.corners()
        xy_min = 2000
        x = 0
        y = 0

        for corner in tag_corners:
            x_val = corner[0]
            y_val = corner[1]
            if (x_val+y_val < xy_min):
                xy_min = x_val+y_val
                x = x_val
                y = y_val

        X,Y,W,H = upscale_QQVGA_to_QVGA(x,y,tag.w(),tag.h())

        img.draw_rectangle(X-10,Y-10,W+16,H+16, color=0, fill=True)

##########################################################
#
# Finding all blobs of desired color and returns a list
# of those blobs and another list of the length of those lists.
#
##########################################################
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

##########################################################
#
# Drawing lines between the corners of the minimum area
# of each blob.
#
# Also draws a cross at the center of each blob.
#
##########################################################

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


##########################################################
#
#   Main program
#
##########################################################


april_tags_dict = {}
april_tags_dict , calib_result = calibration()

if (calib_result):

    print("Calibration Success!")

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
    mask_april_tags(april_tags_dict)
    blobs, len_blobs_list = find_blobs(X,Y,W,H)
    draw_blobs(blobs, X,Y,W,H)
    print(len_blobs_list)

else:
    print("Calibration Failed!")

    ## Prompt user to try again or exit the program

    ## If calibration fails more than e.g 3 times in a row
    ## then ask the user to wait for some time while waiting
    ## for the camera to cool down. Set some timer to display
    ## how long the user must wait.
    ## Then promt the user to try again or quit the program.
    ## Possibly also give a hint to the user to check the
    ## focus of the camera lens, or that the view of the
    ## april tags are not obstructed,







