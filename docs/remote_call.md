### Remote call

remote_call consists of an object "remote_control" which give the user access to remotly control the OpenMV Cam and the WLKATA Mirobot.

## 1. Controlling the OpenMV CAM

First the object needs to be instanziated, eg:
``` python
    import remote_call as rem

    r = rem.remote_control()

    cam_one = r.get_camera(r.CAMERA_ONE_PORT)
```

cam_one will now hold a reference to the interface needed to communicate with the OpenMV.

To request data from the camera the remote_control object has a function called ```fill_data_list``` which will take an interface as an argument. This function will then get data from the camera and store this data in the instance variables of the remote_call obejct.

```python
r.fill_data_list(cam_one)
```

See the ```test_cam.py``` for an example of how this data can be retrieved.

To access a different camera, a reference could just be stored in the same way as above:

```python
cam_two = r.get_camera(valid port name)
```

In our setup there is only two cameras, but the code is written in such a way that it would work with any given valid port. For convinience, we have defined the camera port as instance variables:

    self.CAMERA_ONE_PORT
    self.CAMERA_TWO_PORT

## 2. Controlling the WLKATA Mirobot

To control the robot we also need an instance of the remote_control object, eg:

```python 
    import remote_call as rem

    r = rem.remote_control()
```

This part is a little different from the camera, in the way that we dont store an actual robot object.
This will be instansiated within each call to move the robot. This way of operating make sure that the ports to the robot always will be closed after it is finnished moving.

There are four functions to control the robot in this api.

1. ```python
    init_robot(self, port=None):
   ```
    This function will home the robot. The port will be way to control which robot is moving. To move robot 1 make call such as:

    ```python
    r.init_robot(r.MIROBOT_ONE_PORT)
    ```
2. ```python
    go_to_resting_poing(self, port=None, speed=750):
    ```
    This will move the robot to a position where it is easy to calibrate the camera, and also to get a good image of the working space. Port works the same way as above. Speed can be changed if wanted. We have found 750 to be a good speed, and set it as default. It is not recommended to go under 500. Max is 2000, and is also not recommended, because then it moves really fast. IF something were to go wrong, there will be very little time to react.

3. ```python
     def go_to_zero(self, port=None, speed=750):
   ```
    This will move the robot to it's zero point. This is the position reached after homing and is ideal as starting point for performing tasks. Port and speed, are the same as above.

4. ```python
     def pick_up_cartesian(self, x, y, z, rx=0, ry=0, rz=0, port=None, speed=750, is_cube=True):
   ```
    This will pick up a cube/domino brick at the spesified coordinates. rx, ry, rz are provided with the default value 0 to make using the function more smooth. As this only controls the angle of the end effector. Port and speed are the same as above. is_cube is a bool telling if the object to pick up is a cube or a domino brick. The z value will be different depending on this.
