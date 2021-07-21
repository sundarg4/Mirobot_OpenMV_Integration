import remote_call as rem
import numpy as np
import time
import sys

r = rem.remote_control()
cam = r.get_camera(r.CAMERA_ONE_PORT)

# Starting a timer, getting data and displaying how long time it took to retrieve data.
start = time.time()
print("Processing...")
r.fill_data_list(cam)
end = time.time()
elapsed = end - start
elapsed = round(elapsed, 2)
print("Finnished getting data in: " + str(elapsed) + "s" + "\n\n" )

# Getting the length of the data.
count = 0
for i in range(len(r.prev_cx)):
    if (r.prev_cx[i] != -1):
        count = count + 1

# Initializing an array with the size of the data.   
blobs = [-1] * count

# Getting the tag corners
tag_corners = r.get_tag_corners()

# Storing blob data in blobs array.
for i in range(len(r.prev_cx)):
    if (r.prev_cx[i] != -1):
        cx = r.prev_cx[i]
        cy = r.prev_cy[i]
        area = r.prev_area[i]
        rotation = r.prev_rotation_angle[i]
        color = r.color[i]    
        cx_robot_frame, cy_robot_frame = r.rescale(cx, cy, tag_corners)
        blob_tuple = [cx, cy, area, rotation, color, int(cx_robot_frame), int(cy_robot_frame)]
        blobs[i] = blob_tuple

# Plotting the blobs     
r.draw(r.prev_cx, r.prev_cy)

# Sorts the blobs before printing.
sorted_list = sorted(blobs , key=lambda k: [k[0], k[1]])
print("\n")
print("Sorted from left to right on x")
print("[cx, cy, area, rotation, color, robot_cx, robot_cy]")
print()

# Prints the blob data to terminal.
for i in range(len(sorted_list)):
    count = i + 1
    print(str(count) + ": " + str(sorted_list[i]))
    


