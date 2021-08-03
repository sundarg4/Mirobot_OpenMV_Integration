import remote_call as rem
import numpy as np
import time
import sys

# Initialize the remote control object
r = rem.remote_control()

# Get camera one
cam = r.get_camera(r.CAMERA_ONE_PORT)

# Starting timer and getting data
start = time.time()
print("Processing...")
# Getting data
r.fill_data_list(cam)
end = time.time()
elapsed = end - start
elapsed = round(elapsed, 2)
print("Finnished getting data in: " + str(elapsed) + "s" + "\n\n" )

# Getting the length of data to used for initializing arrays of correct size
count = 0
for i in range(len(r.prev_cx)):
    if (r.prev_cx[i] != -1):
        count = count + 1

# Initializing an array to keep the blob data
blobs = [-1] * count
# Getting the april tag corners
tag_corners = r.get_tag_corners()

# looping through the data stored in the object, adding it to a new array to be displayed later
for i in range(len(r.prev_cx)):
    if (r.prev_cx[i] != -1):
        cx = r.prev_cx[i]
        cy = r.prev_cy[i]
        area = r.prev_area[i]
        rotation = r.prev_rotation_angle[i]
        color = r.color[i]    
        cx_robot_frame, cy_robot_frame = r.rescale(cx, cy, tag_corners)
        is_cube = r.is_cube_list[i]
        blob_tuple = [cx, cy, area, rotation, color, int(cx_robot_frame), int(cy_robot_frame), is_cube]
        blobs[i] = blob_tuple

# Drawing the blobs
r.draw(r.prev_cx, r.prev_cy)

# sorting blobs left to right
sorted_list = sorted(blobs , key=lambda k: [k[0], k[1]])

print("\n")
print("Sorted from left to right on x")
print("[cx, cy, area, rotation, color, robot_cx, robot_cy, is_cube]")
print()

# Print blob data
for i in range(len(sorted_list)):
    count = i + 1
    print(str(count) + ": " + str(sorted_list[i]))
    


