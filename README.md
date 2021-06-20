# Small image processing library for WLKATA Mirobot using OpenMV.


## Instructions
Here we shall put some information.


## Code
```
get_roi(april_tags):
```
Finds the region of interest for where cubes are detected.

The algorithm loops through all the april tags,
finds its corners and loops through them.

For each corner that corners x and y coordinates will be
added to each other, If this sum is smaller then x_min + y_min
then this will be the new values for x_min and y_min.
And vice versa with larger values than x_max + y_max.

The width of the ROI is then found by subtracting x_min from x_max.
The height of the ROI is found by subtracting y_min from y_max.

The find blobs function that will be fed theese values requires
they are of the type int so therefore round them and then convert them to
integers before we return them,

The values returned will be the top left corner of the ROI given by
x_min and y_min. And also the width and height of the ROI.

Importnat to remember is that ROI is found using QQVGA so
there is neccessary to call the function upscale_QQVGA_to_QVGA
on theese coordinates before using them to find blobs.



