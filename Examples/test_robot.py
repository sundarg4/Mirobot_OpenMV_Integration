import r2 as rem
#import remote_call as rem
import time

r = rem.remote_control()
r.init_robot(r.MIROBOT_ONE_PORT)
time.sleep(5)
#r.go_to_resting_point(r.MIROBOT_ONE_PORT)
r.pick_up_cartesian(208, 74, 59, port=r.MIROBOT_ONE_PORT)

    
