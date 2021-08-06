### Remote device

The remote device script is run on the OpenMV module. Here is a description of the functionality in this script.

All functionality is wrapped within an object called openmv_remote.

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

(red_blobs, green_blobs, blue_blobs)

```python
def get_blob_data(blobs, data_dict):
```
Parameters: The list of blobs returned from the fins_blobs function,
            and the data_dict containing data about position, orientation and 
            color of each blob.
            
Returns:    The data dictionary containg blob data.


Loops through the list of blob lists with the enumeration function of python, and so gaining
access to both the counter and the list.

Then loops through each blob in the current blob_list and gets the following data from each blob:

cx and cy is taken directly from the OpenMV function blob.cx() and blob.cy().
Blob area is similarly gotten straight from blob.area(). Worth noting that this area is not the minimum area.
The corners of the minimum area are gotten from the inbuilt function blob.min_corners(). Although this function is sligthly unstable in the way it returns the corners. And they are returned as a tuple, which means they are unmutable. Thats why they are appended to a new list, in order to be further proseced on the remote_call.py running on the raspberry pi.

Gets the color by sending the "color_code" (counter from the first loop) to the function get_color().

As a sidenote angle of rotation is calculated on in the remote_call.py and not on the OpenMV.

Finally all data is appended to the dictionary: 
([cx, cy, area, corners_list, color])

```python
def get_color(color_code):
```
Translates the color code into its string representation.
0 = red,
1 = green,
2 = bluee



