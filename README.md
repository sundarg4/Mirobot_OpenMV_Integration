# WLKATA Mirobot - OpenMV remote control API

This API is split into two source files, `remote_device.py` which should be flashed onto the OpenMV module using the </br>
OpenMV IDE (https://openmv.io/pages/download). and `remote_call.py`which should be stored on the raspberry pi handeling the remote calls
to both the OpenMV and the Mirobot. </br>


To flash to a script to the openMV board:

1. Connect the openMV via USB to a computer and start the OpenMV IDE.
2. Press connect in the lower left corner of the IDE.
3. Make sure that the script you want to flash is open.
4. Press ```tools -> Save open script to OpenMV Cam (as main.py)```
5. Press ```tools -> Reset OpenMV Cam```

The OpenMV Cam should now be disconnected, and the main.py script is set to run automatically when powered.



`test_cam.py` and `test_robot.py`demonstrates examples of how to use the API. </br></br>


## Installation and dependencies

This project mainly focuses on working directly with the raspberry pi to communicate with both OpenMV and Mirobot, but if the need arises, OpenMV IDE can be installed on Windows, Mac, Linux, and even Raspberry. WLKATA Studio IDE is available for Windows, Mac, and Linux (Ubuntu). Mac and Windows versions worked perfectly but we had issues getting the linux version up and running. </br></br>

The raspberry pi is accessed through ssh, or through VNC if a GUI is required. </br>
Source code is located in /home/mirobot. </br></br>
Everything is set up to work in a virtual enviroment, to activate it simple run the following command in terminal: </br>
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

Dependencies </br>
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

## This API

```python
def calibration():
```
Initializes the dictionary of april tags used throughout the program.
Runs a loop 25 times and make a picture and store the found april tags 
in the dictionary.

Returns a the dictionary of april tags and a calibration_result,
True if all four tags where found, False if not.

```python
def get_roi(april_tags):
```
Finds the region of interest for where cubes are detected.

The algorithm loops through all the april tags,
finds its corners and loops through them.

For each corner, it's x and y coordinates will be
added to each other, If this sum is smaller than x_min + y_min
then this will be the new values for x_min and y_min.
And vice versa with larger values than x_max + y_max.

The width of the ROI is then found by subtracting x_min from x_max.
The height of the ROI is found by subtracting y_min from y_max.

The find blobs function that will be fed theese values requires
they are integers so therefore they are first rounded and then converted 
to integers before returning them.

The values returned will be the top left corner of the ROI given by
x_min and y_min. And also the width and height of the ROI. 
(x_min, y_min, w, h)


Importnat to remember is that ROI is found using QQVGA so
there is neccessary to call the function upscale_QQVGA_to_QVGA
on theese coordinates before using them to find blobs.


```python
def mask_april_tags(april_tags):
```
Using the inbuilt method to find the rectangle area of each april tag.
Then upscaling those coordinates from QQVGA to QVGA, and finally
drawing a black rectangle over them.

```python
def upscale_QQVGA_to_QVGA(x,y,w,h):
```
returns coordinates in QQVGA.

```python
def find_blobs(x,y,w,h):
```
Returns a list of blobs separated by color. 
Each color is also a list of its own, containing all
the blobs found of that color.

(white_blobs, red_blobs, green_blobs, blue_blobs)

```python
def find_len_of_blobs(blobs):
```
Returns the length of all lists returned from find_blobs().

```python
def get_blob_data(blobs, data_dict):
```
Parameters: The list of blobs returned from the fins_blobs function,
            and the data_dict containing data about position, orientation and 
            color of each blob.
            
Returns:    The data dictionary containg blob data.


Loops through the list of blob lists with the enumeration function of python, and so gaining
access to both the counter and the list.

Further loops through each list in the same manner and gains access to both counter and blob.

Gets the color by sending the "color_code" (counter from the first loop) to the function get_color().

The variable total count is used to keep an unique identifier for each blob to use as key while adding/updating
the dictionary.

The angle of rotation is found by calling the function get_angle_of_rotation_tan()

If the object is a cuboid or a rectangle is found by calling is_cuboid_or_rectangle()

Finally all data is stored to the dictionary like so,

data_dict[total_count] = (color, cx, cy, angle_of_rotation, is_cuboid).

```python
def get_color(color_code):
```
Translates the color code into its string representation.
0 = white,
1 = red,
2 = green,
3 = bluee

```python
def is_cuboid_or_rectangle(blob):
```
Parameter: A blob.

Returns:   True if its a rectangle, False if its a cube.

Checks how big the area of a blob is. Through experimentation we foud that 750 was a good value. Thus if the blob has an area of more than 750 it will be considered a rectangle, and if its less than 750 it will be considered a cuboid. 

This threshold value will be different if the camera mount is adjusted, so that the distance from the camera to the working space is different. Or if the objects used are of different diemensions than the ones we used writing this code.

Cube: x * x cm
Rectangle x * y cm

```python
def get_angle_of_rotation_tan(blob, prev_degree):
```
Parameters: A blob, The previous angle in degrees of that blob.

Returns:    The new angle.

By iterating through the corners of the minimum area the top corner and the right corner are detected.
The angle is then found by using the atan2 function, which returns in radians. This angle will then be converted to degrees. </br>

If there has been no previous degree than this will be equal to -1 and will be replaced by the angle in degrees.

If there already is a previous anlge, then an exponetial filter will be applied before returning the new angle.


```python
def draw_blobs(blobs):
```
Draws a rectangle around the minimum area of each blob.
Also draws a cross at cx,cy of each blob.

