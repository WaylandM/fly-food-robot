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

# SCRIPT TO GENERATE G-C0DE FOR CALIBRATING PUMP

# SETTINGS

# filename
filename = '/home/pi/robot/nc/calibrate_pump.nc'

# home/datum + homing pull-off (mm) (value of Grbl setting $27)
x_home = -5
y_home = -5
z_home = -5

# z value providing minimal clearance between nozzle and top of vials
z_fill = -62 

# peristaltic pump settings
min_fill_time = 0.3
max_fill_time = 0.6
# pause to allow for drips before moving to next vial
drip_pause = 0.1 

# vial coordinates (x,y)
frontLeft = (-8,-14)
backRight = (-236,-240)

nrows=10
ncols=10



# G-CODE GENERATION

fill_times = [round(min_fill_time + (i * (max_fill_time - min_fill_time) / (nrows-1.0)), 2) for i in range(0,10,1)]

f = open(filename, 'w')

f.write('(Pump calibration)\n(Fill times:)\n')

for i in range(0,len(fill_times),1):
	f.write('(Row ' + str(i+1) + ': ' + str(fill_times[i]) + ' secs)\n')

# home 
f.write('$h\n')

# make sure pump set to CW
f.write('m3\n')

# lower nozzle to fill height
f.write('z'+str(z_fill)+'\n')

# calculate distance between adjacent vials
x_interval = (backRight[0]-frontLeft[0])/(ncols-1.0) # -1.0 to ensure converted to float
y_interval = (backRight[1]-frontLeft[1])/(nrows-1.0)

y_current = frontLeft[1]

for i in range(1, nrows+1, 1):
    if i % 2 == 0:
        x_current = backRight[0]
    else:
        x_current = frontLeft[0]
    for j in range(1, ncols+1, 1):
        f.write('x' + str(x_current) + ' y' + str(y_current) + '\n')
        f.write('m8\n')
        f.write('g4 p' + str(fill_times[i-1]) + '\n')
        f.write('m9\n')
        if drip_pause > 0:
            f.write('g4 p' + str(drip_pause) + '\n')
        if i % 2 == 0:
            x_current = round((x_current - x_interval),2)
        else:
            x_current = round((x_current + x_interval),2)
    y_current =round((y_current + y_interval), 2)


# return to home position
f.write('z' + str(z_home) + '\n')
f.write('x' + str(x_home) + ' y' + str(y_home) + '\n')

f.close()

