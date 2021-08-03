import remote_call as rem
import time

# Initialize the remote control object
r = rem.remote_control()

# Home the robot
r.init_robot(r.MIROBOT_ONE_PORT)

#time.sleep(5)

# Go to a 'sleeping' position to give the camera a good view of the workspace.
#r.go_to_resting_point(r.MIROBOT_ONE_PORT)

# Pick up a cube
# (cx, cy, cz, rx=0, ry=0, rz=0, port=None, speed=750)
# Some parameters where given standard values to simplify the use of the function.
r.pick_up_cartesian(208, 74, 59, port=r.MIROBOT_ONE_PORT)

    
