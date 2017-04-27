#!/usr/bin/env python

#home/datum + offset
x_home = -5
y_home = -5
z_home = -5

z_clearance = -62 # previous value -77 
#z_fill = -99

# need 8-9 ml
# pump speed 1800ml/min
# ml/s = 1800/60 = 30
# fill time = 0.3

fill_time = 0.43
drip_pause = 0.1 # pause to allow for drips before moving to next vial
x1 = -8 # previous value -5
y1 = -14 # previous value -6
x100 = -236 # previous value -240
y100 = -240 # previous value -240
nrows = 10
ncols = 10

# -1.0 to ensure converted to float
x_interval = (x100 - x1)/(ncols-1.0)
y_interval = (y100 - y1)/(nrows-1.0)

f = open('../nc/1_box_vials_no_dip.nc', 'w')

f.write('(gcode instructions to fill box of 100 vials.)\n')

f.write('$h\n')

# make sure pump set to CW
f.write('m3\n')

f.write('z'+str(z_clearance)+'\n')

y_current = y1

for i in range(1, nrows+1, 1):
    if i % 2 == 0:
        x_current = x100
    else:
        x_current = x1
    for j in range(1, ncols+1, 1):
        f.write('x' + str(x_current) + ' y' + str(y_current) + '\n')
        #f.write('z' + str(z_fill) + '\n')
        f.write('m8\n')
        f.write('g4 p' + str(fill_time) + '\n')
        f.write('m9\n')
        if drip_pause > 0:
            f.write('g4 p' + str(drip_pause) + '\n')
        #f.write('z' + str(z_clearance) + '\n')
        if i % 2 == 0:
            x_current = round((x_current - x_interval),2)
        else:
            x_current = round((x_current + x_interval),2)
    y_current =round((y_current + y_interval), 2)
f.write('z' + str(z_home) + '\n')
f.write('x' + str(x_home) + ' y' + str(y_home) + '\n')
    


f.close()

