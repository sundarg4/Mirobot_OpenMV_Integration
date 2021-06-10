# Untitled - By: bjornandersson - Mon Jun 7 2021

import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    ##################################################################
    # Threshold values the colors to detect.
    #
    # These thresholds are given in the LAB color space. (L*, a*, b*).
    #
    # Where:
    #
    # L* = brightness
    #
    # A postitive value for a* indicates the amount of red.
    # A negative value for a* indicates the amount of green.
    #
    # A positive value for b* indicates the amount of yellow.
    # A negative value for b* indicates the amount of blue.
    #
    # The values range between -128 to +128.
    #
    ###################################################################
    w_thresholds = (80, 100, -18, 90, -17, 69)
    r_thresholds = (45, 79, 39, 90, -7, 78)
    g_thresholds = (37, 86, -105, -22, -45, 71)
    b_thresholds = (30, 73, -42, 52, -119, -15)

    # Storing blobs of different colors in a separate variable.
    w_blobs = img.find_blobs([w_thresholds], area_threshold=150, merge=False)
    r_blobs = img.find_blobs([r_thresholds], area_threshold=150, merge=False)
    g_blobs = img.find_blobs([g_thresholds], area_threshold=150, merge=False)
    b_blobs = img.find_blobs([b_thresholds], area_threshold=150, merge=False)

    # Putting them all into a list for easy looping.
    blobs = [w_blobs, r_blobs, g_blobs, b_blobs]

    # Finding the number of blobs of each color.
    len_w_blobs = len(w_blobs)
    len_r_blobs = len(r_blobs)
    len_g_blobs = len(g_blobs)
    len_b_blobs = len(b_blobs)

    # Only used for color inside of the image.draw_line method.
    r = (pyb.rng() % 127) + 128
    g = (pyb.rng() % 127) + 128
    b = (pyb.rng() % 127) + 128


    for color in blobs:
        for blob in color:
            # The corners with corresponding coordinates for the minimum area rectangle.
            corners = blob.min_corners()
            c1 = corners[0]
            c2 = corners[1]
            c3 = corners[2]
            c4 = corners[3]

            # The idea was to make use of the min_area calculated here to pass it into the
            # draw rectangle method.
            #
            #
            #w = (c2[0]-c1[0])
            #h = (c4[1]-c1[1])
            #min_area = [c1[0], c1[1], w, h]


            # This is drawing a line from each corner to the other in the minimum area rectangle.
            img.draw_line(c1[0], c1[1], c2[0], c2[1], color = (r, g, b), thickness = 2)
            img.draw_line(c2[0], c2[1], c3[0], c3[1], color = (r, g, b), thickness = 2)
            img.draw_line(c3[0], c3[1], c4[0], c4[1], color = (r, g, b), thickness = 2)
            img.draw_line(c4[0], c4[1], c1[0], c1[1], color = (r, g, b), thickness = 2)


            # Draw a cross in the middle of the blob
            img.draw_cross(blob.cx(), blob.cy(), color=255)
