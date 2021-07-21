import remote_call as rem
import time

# Creates an instance of the remote_control object.
r = rem.remote_control()

# Homes the robot
#r.init_robot(r.MIROBOT_ONE_PORT)

# Sets the robot in a position where it is posible to get data from the OpenMV.
#r.go_to_resting_point(r.MIROBOT_ONE_PORT)

# Picks up a cube at theese coordinates.
# Parameters are (x,y,z,rx,ry,rz,port,speed)
# rx,ry,rz are as default set to 0. 
# speed is defaulted to 750.
# Ports are either r.MIROBOT_ONE_PORT or r.MIROBOT_TWO_PORT, depending on which robot are being used.
# 
# ctr + z will activate the soft emergency stop. If activated please follow theese instructions,
# (also displayed in terminal),
# Press reset button and home robot before further operations.
r.pick_up_cartesian(224, 5, 59, port=r.MIROBOT_ONE_PORT)

    
