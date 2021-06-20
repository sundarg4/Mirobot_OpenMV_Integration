# Small image processing library for WLKATA Mirobot using OpenMV.


## Instructions
Here we shall put some information.



# Code Documentation

```
def calibration():
```
Initializes the dictionary of april tags used throughout the program.
Runs a loop 25 times and make a picture and store the found april tags 
in the dictionary.

Returns a the dictionary of april tags and a calibration_result,
True if all four tags where found, False if not.

```
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


```
def mask_april_tags(april_tags):
```
Using the inbuilt method to find the rectangle area of each april tag.
Then upscaling those coordinates from QQVGA to QVGA, and finally
drawing a black rectangle over them.

```
def upscale_QQVGA_to_QVGA(x,y,w,h):
```
returns coordinates in QQVGA.

```
def find_blobs(x,y,w,h):
```
Returns a list of blobs separated by color. 
Each color is also a list of its own, containing all
the blobs found of that color.

(white_blobs, red_blobs, green_blobs, blue_blobs)

```
def find_len_of_blobs(blobs):
```
Returns the length of all lists returned from find_blobs().

```
def draw_blobs(blobs):
```
Draws a rectangle around the minimum area of each blob.
Also draws a cross at cx,cy of each blob.



