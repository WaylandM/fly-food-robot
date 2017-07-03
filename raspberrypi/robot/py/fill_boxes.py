#!/usr/bin/env python

##################################################################################
#                                                                                #
#  Fly Food Robot                                                                #
#                                                                                #
#  Version 0.1                                                                   #
#                                                                                #
#  Copyright (C) 2017 Matthew Thomas Wayland                                     #
#                                                                                #
#  This file is part of Fly Food Robot.                                          #
#                                                                                #
#  Fly Food Robot is free software: you can redistribute it and/or modify it     #
#  under the terms of the GNU General Public License as published by the Free    #
#  Software Foundation, either version 3 of the License, or (at your option)     #
#  any later version.                                                            #
#                                                                                #
#  Fly Food Robot is distributed in the hope that it will be useful, but         #
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY    #
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License      #
#  for more details.                                                             #
#                                                                                #
#  You should have received a copy of the GNU General Public License along       #
#  with Fly Food Robot.                                                          #
#  If not, see <http://www.gnu.org/licenses/>.                                   #
#                                                                                #
#                                                                                #
##################################################################################

# SCRIPT TO GENERATE G-CODE FOR FILLING VIALS

# SETTINGS
# modify values of variables in this section to match your system

# filenames
filename1Box = '/home/pi/robot/nc/1_box.nc'
filename2Boxes = '/home/pi/robot/nc/2_boxes.nc'

# home/datum + homing pull-off (mm) (value of Grbl setting $27)
x_home = -5
y_home = -5
z_home = -5

# z value providing minimal clearance between nozzle and top of vials
z_clearance = -62 

# peristaltic pump settings
fill_time = 0.43
# pause to allow for drips before moving to next vial
drip_pause = 0.1 

# vial coordinates (x,y)
box1FirstVial = (-8,-14)
box1LastVial = (-236,-240)
box2FirstVial = (-8,-286)
box2LastVial = (-236,-513)

nrows=10
ncols=10
nVials=nrows*ncols


# G-CODE GENERATION

# function for generating g-code
# f: file object
# firstVial: coordinates (x,y) of first vial
# lastVial: coordinates (x,y) of last vial
def generateG(f, firstVial, lastVial):

    # home 
    f.write('$h\n')

    # make sure pump set to CW
    f.write('m3\n')

    # lower nozzle to fill height
    f.write('z'+str(z_clearance)+'\n')

    # calculate distance between adjacent vials
    x_interval = (lastVial[0]-firstVial[0])/(ncols-1.0) # -1.0 to ensure converted to float
    y_interval = (lastVial[1]-firstVial[1])/(nrows-1.0)

    y_current = firstVial[1]
    for i in range(1, nrows+1, 1):
        if i % 2 == 0:
            x_current = lastVial[0]
        else:
            x_current = firstVial[0]
        for j in range(1, ncols+1, 1):
            f.write('x' + str(x_current) + ' y' + str(y_current) + '\n')
            f.write('m8\n')
            f.write('g4 p' + str(fill_time) + '\n')
            f.write('m9\n')
            if drip_pause > 0:
                f.write('g4 p' + str(drip_pause) + '\n')
            if i % 2 == 0:
                x_current = round((x_current - x_interval),2)
            else:
                x_current = round((x_current + x_interval),2)
        y_current =round((y_current + y_interval), 2)


# generate g-code for filling one box of vials

fobj = open(filename1Box, 'w')

f.write('(gcode instructions to fill one box of ' + str(nVials) + ' vials.)\n')

generateG(fobj, box1FirstVial, box1LastVial)

# return to home position
fobj.write('z' + str(z_home) + '\n')
fobj.write('x' + str(x_home) + ' y' + str(y_home) + '\n')

fobj.close()

# generate g-code for filling two boxes of vials

fobj = open(filename2Boxes, 'w')

f.write('(gcode instructions to fill two boxes of ' + str(nVials) + ' vials.)\n')

generateG(fobj, box1FirstVial, box1LastVial)
generateG(fobj, box2FirstVial, box2LastVial)

fobj.write('z' + str(z_home) + '\n')
fobj.write('x' + str(x_home) + ' y' + str(y_home) + '\n')

fobj.close()


