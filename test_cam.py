import remote_call as rem
import numpy as np
import time
#from pynput.keyboard import Listener, Key
import sys

####
# 
# Emergency software stop
#  
#def on_press(key):
#    try:
#        raise KeyboardInterrupt('Throwing')
#    
#    except KeyboardInterrupt as keypressevent:
#        print('Caught this keypress!: ' + repr(keypressevent))
#        sys.exit()
####

r = rem.remote_control()
cam = r.get_camera(r.CAMERA_ONE_PORT)

####
#
#   Start thread listening for emergency software stop
#
#with Listener(on_press=on_press) as listener: # Setup the listener
#    listener.join() # Join the thread to the main thread
####

start = time.time()
print("Processing...")
r.fill_data_list(cam)
end = time.time()
elapsed = end - start
elapsed = round(elapsed, 2)
print("Finnished getting data in: " + str(elapsed) + "s" + "\n\n" )


count = 0
for i in range(len(r.prev_cx)):
    if (r.prev_cx[i] != -1):
        count = count + 1
        
blobs = [-1] * count
tag_corners = r.get_tag_corners()

for i in range(len(r.prev_cx)):
    if (r.prev_cx[i] != -1):
        cx = r.prev_cx[i]
        cy = r.prev_cy[i]
        area = r.prev_area[i]
        rotation = r.prev_rotation_angle[i]
        color = r.color[i]
        
        cx_robot_frame, cy_robot_frame = r.rescale(cx, cy, tag_corners)
        blob_tuple = [cx, cy, area, rotation, color, int(cy_robot_frame), int(cx_robot_frame)]
        blobs[i] = blob_tuple
        
r.draw(r.prev_cx, r.prev_cy)

sorted_list = sorted(blobs , key=lambda k: [k[0], k[1]])
print("\n")
print("Sorted from left to right on x")
print("[cx, cy, area, rotation, color, robot_cx, robot_cy]")
print()

for i in range(len(sorted_list)):
    count = i + 1
    print(str(count) + ": " + str(sorted_list[i]))
    


