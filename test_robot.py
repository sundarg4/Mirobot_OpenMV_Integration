import remote_call as rem
import time

r = rem.remote_control()
#r.init_robot(r.MIROBOT_ONE_PORT)
#r.go_to_resting_point(r.MIROBOT_ONE_PORT)
r.pick_up_cartesian(224, 5, 59, port=r.MIROBOT_ONE_PORT)

    
