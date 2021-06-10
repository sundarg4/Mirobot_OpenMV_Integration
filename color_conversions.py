#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 11:56:59 2021

@author: bjornandersson
"""

# Code borrowed from http://www.easyrgb.com/en/math.php#text8
# Only adapted for python.
# To et acurate transform from LAB to XYZ the return r,g,b values
# from XYZ_to_RGB should first be rounded to zero decimals and then
# be converted to an integer.

def LAB_to_XYZ(L, a, b):
    #Reference-X, Y and Z refer to specific illuminants and observers.
    #Common reference values are available below in this same page.
    
    var_Y = ( L + 16 ) / 116
    var_X = a / 500 + var_Y
    
    var_Z = var_Y - b / 200
    
    if ( pow( var_Y, 3)  > 0.008856 ):
        var_Y = pow( var_Y, 3 )
    else :
        var_Y = ( var_Y - 16 / 116 ) / 7.787
    if ( pow( var_X, 3)  > 0.008856 ):
        var_X = pow( var_X, 3)
    else:                
        var_X = ( var_X - 16 / 116 ) / 7.787
    if ( pow( var_Z, 3)  > 0.008856 ):
        var_Z = pow( var_Z, 3)
    else:
        var_Z = ( var_Z - 16 / 116 ) / 7.787
    
    X = var_X * 95.047
    Y = var_Y * 100.000
    Z = var_Z * 108.883
    
    return X,Y,Z


def XYZ_to_RGB(X,Y,Z):
    #X, Y and Z input refer to a D65/2° standard illuminant.
    #sR, sG and sB (standard RGB) output range = 0 ÷ 255
    
    var_X = X / 100
    var_Y = Y / 100
    var_Z = Z / 100
    
    var_R = var_X *  3.2406 + var_Y * -1.5372 + var_Z * -0.4986
    var_G = var_X * -0.9689 + var_Y *  1.8758 + var_Z *  0.0415
    var_B = var_X *  0.0557 + var_Y * -0.2040 + var_Z *  1.0570
    
    if ( var_R > 0.0031308 ):
        var_R = 1.055 * ( pow( var_R , ( 1 / 2.4 ) ) ) - 0.055
    else:
        var_R = 12.92 * var_R
        
    if ( var_G > 0.0031308 ):
        var_G = 1.055 * ( pow(var_G , ( 1 / 2.4 ) ) )- 0.055
    else:
        var_G = 12.92 * var_G
        
    if ( var_B > 0.0031308 ):
        var_B = 1.055 * ( pow( var_B , ( 1 / 2.4 ) ) ) - 0.055
    else:
        var_B = 12.92 * var_B
    
    sR = var_R * 255
    sG = var_G * 255
    sB = var_B * 255
    
    if (sR < 0):
        sR = 0
    if (sR > 255):
        sR = 255
    if (sG < 0):
        sG = 0
    if (sG > 255):
        sG = 255
    if (sB < 0):
        sB = 0
    if (sB > 255):
        sB = 255
    
    return sR, sG, sB


# TEST

#L = 53.23288178584245
#a = 80.10930952982204
#b = 67.22006831026425

#l2 = 54.3018719078641
#a2 = 77.76052622686625
#b2 = 56.58180454353558

#x,y,z = LAB_to_XYZ(L,a,b)
#r,g,b = XYZ_to_RGB(x, y, z)

#x2,y2,z2 = LAB_to_XYZ(l2,a2,b2)
#r2,g2,b2 = XYZ_to_RGB(x2, y2, z2)

#print(f"r: {int(round(r,0))}")
#print(f"g: {int(round(g,0))}")
#print(f"b: {int(round(b,0))}")

#print(f"r: {int(round(r2,0))}")
#print(f"g: {int(round(g2,0))}")
#print(f"b: {int(round(b2,0))}")

###
# working with integer, instad of 255 for red the conversion 
# returns 254. Which I think is acceptable.
###

#L = 53
#a = 80
#b = 67

#x,y,z = LAB_to_XYZ(L,a,b)
#r,g,b = XYZ_to_RGB(x, y, z)

#print(f"r: {int(round(r,0))}")
#print(f"g: {int(round(g,0))}")
#print(f"b: {int(round(b,0))}")
