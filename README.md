# WLKATA Mirobot - OpenMV remote control API

This API is split into two source files, `remote_device.py` which should be flashed onto the OpenMV module using the </br>
OpenMV IDE (https://openmv.io/pages/download), and `remote_call.py`which should be stored on the raspberry pi handeling the remote calls
to both the OpenMV and the Mirobot. </br>

`test_cam.py` and `test_robot.py`demonstrates examples of how to use the API. </br></br>


### Flashing a script to the OpenMV Cam

1. Connect the openMV via USB to a computer and start the OpenMV IDE.
2. Press connect in the lower left corner of the IDE.
3. Make sure that the script you want to flash is open.
4. Press ```tools -> Save open script to OpenMV Cam (as main.py)```
5. Press ```tools -> Reset OpenMV Cam```

The OpenMV Cam should now be disconnected, and the main.py script is set to run automatically when powered. </br></br>

### Software emergency stop
If to press ```ctr+c``` during the robots operation, the software emergency stop will be activated.
Follow the instructions given in the terminal.

1. Press the reset button on the Mirobot.
2. Home the robot before further operations.

</br></br>


## Installation and dependencies

This project mainly focuses on working directly with the raspberry pi to communicate with both OpenMV and Mirobot, but if the need arises, OpenMV IDE can be installed on Windows, Mac, Linux, and even Raspberry. WLKATA Studio IDE is available for Windows, Mac, and Linux (Ubuntu). Mac and Windows versions worked perfectly but we had issues getting the linux version up and running. </br></br>

The raspberry pi is accessed through ssh, or through VNC if a GUI is required. </br>
Source code is located in /home/mirobot. </br></br>
Everything is set up to work in a virtual enviroment, to activate it run the following command in terminal: </br>
`openmv`. </br>

The ports are configured static, so that they dont run into a problem with randomly addressed ports. </br>
The ports are: </br></br>
`/dev/ttyACM_OpenMV1`</br>
`/dev/ttyACM_OpenMV2`</br>
`/dev/ttyUSB_Mirobot1`</br>
`/dev/ttyUSB_Mirobot2`</br></br>

and corresponds to the following ports in code: </br>
`self.CAMERA_ONE_PORT` </br>
`self.CAMERA_TWO_PORT ` </br>
`self.MIROBOT_ONE_PORT` </br>
`self.MIROBOT_TWO_PORT` </br></br>

### Dependencies </br>
OpenMV library: needed for the remote_device.py
</br>
https://openmv.io/pages/download
</br></br>
rpc : part of the openMV library, needed for remote procedure calls.
Needs to be on both the remote device and the raspberry pi. 
Just copy the file rpc.py into the same folder as your scripts,
</br>
https://github.com/openmv/openmv/tree/master/tools/rpc 
</br></br>
pyserial : dependency from rpc
</br>
`pip install pyserial`
</br></br>
mirobot-py
</br>
`pip install mirobot-py`
</br></br>
ast v.: </br>
https://github.com/python/cpython/blob/main/Lib/ast.py 
</br></br>
Numpy: </br>
`pip install numpy`
</br></br>
Scipy: </br>
` pip install scipy`
</br></br>
plotille : For plotting in terminal </br>
`pip install plotille`
</br></br>


## Documentation

Official OpenMV docs: </br>
https://docs.openmv.io/ </br>

Docs for openMV RPC: </br>
https://github.com/openmv/openmv/blob/master/tools/rpc/README.md </br>

WLKATA Mirobot: </br>
https://www.wlkata.com/ </br></br>

The official mirobot manual: </br>
https://lin-nice.github.io/mirobot_gitbook_en/ </br>

The official python mirobot API: </br>
https://rirze.github.io/mirobot-py/mirobot/index.html </br>

Github for mirobot-py: </br>
https://github.com/wlkata/mirobot-py </br></br>
