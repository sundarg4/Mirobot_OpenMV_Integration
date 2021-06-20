
import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

white_threshold = (58, 89, -2, 9, -19, 18)
red_threshold = (45, 79, 39, 90, -7, 78)
green_threshold = (31, 81, -88, -27, -51, 41)
blue_threshold = (9, 66, -20, 85, -128, -14)

def find_blobs():
    white_blobs = img.find_blobs([white_threshold], area_threshold=100, merge=False)
    red_blobs = img.find_blobs([red_threshold], area_threshold=100, merge=False)
    green_blobs = img.find_blobs([green_threshold], area_threshold=100, merge=False)
    blue_blobs = img.find_blobs([blue_threshold], area_threshold=100, merge=False)

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
            ##############################################################
            #
            #        1
            #       –––
            #    4 |   | 2
            #       –––
            #        3
            #
            ##############################################################

            top = img.draw_line(c1[0], c1[1], c2[0], c2[1], color = (255, 255, 0), thickness = 2)
            right = img.draw_line(c2[0], c2[1], c3[0], c3[1], color = (255, 0, 0), thickness = 2)
            bottom = img.draw_line(c3[0], c3[1], c4[0], c4[1], color = (0, 255, 0), thickness = 2)
            left = img.draw_line(c4[0], c4[1], c1[0], c1[1], color = (0, 0, 255), thickness = 2)

            degrees = 0
            for i in range(10):
                top_length = c2[0] - c1[0]
                right_length = c3[1] - c2[1]
                bottom_length = c3[0] - c4[0]
                left_length = c4[1] - c1[1]


                a =  top_length
                b = right_length

                if b == 0:
                    print("infinity")   # y - intercept will be infinity

                # if line is parallel to x axis
                if a == 0:
                    print("infinity")     # x - intercept will be infinity

                # Slope of the line
                m = a / b

                # y = mx + c in where c is unknown
                # Use any of the given point to find c
                x = c1[0]
                y = c1[1]
                c = y-m * x

                # For finding the x-intercept put y = 0
                y = 0
                x =(y-c)/m
                print("x-intercept: " + str(x) )

                # For finding the y-intercept put x = 0
                x = 0
                y = m * x + c
                print("y-intercept: " + str(y) )

                #slope = right_length / top_length


                hypotenusa_one = math.sqrt( (left_length * left_length) + (top_length * top_length) )
                hypotenusa_two = math.sqrt( (right_length * right_length) + (bottom_length * bottom_length) )

                if (hypotenusa_one < 0):
                    hypotenusa_one = 0

                if (hypotenusa_two < 0):
                    hypotenusa_two = 0

                angle_one = math.asin(top_length /  hypotenusa_one)
                angle_two = math.asin(bottom_length / hypotenusa_two)

                degreees = int (degrees + ( angle_one * (180 / math.pi) ) )
                degreees = int(degrees + ( angle_two * (180 / math.pi) ) )

            degrees = round( degrees / 20 )
            print(degreees)

            # Draw a cross in the middle of the blob
            img.draw_cross(blob.cx(), blob.cy(), color=255)


while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
    blobs = find_blobs()
    len_blobs_list = find_len_of_blobs(blobs)
    draw_blobs(blobs)
    #print(len_blobs_list)
