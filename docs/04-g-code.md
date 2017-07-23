# Program robot to fill vials {#gcode}

Running job without GUI - for testing

<!--
# need 8-9 ml
# pump speed 1800ml/min
# ml/s = 1800/60 = 30
# fill time = 0.3
-->


```
ssh pi@192.168.1.3

sudo minicom -D /dev/ttyACM0 -b115200

?<Idle|MPos:-5.000,-5.000,-4.993|FS:0,0|Ov:100,100,100>

x-10 y-10 z-10
ok
?<Idle|MPos:-10.000,-10.000,-10.005|FS:0,0>


x-20 y-20 z-30
ok
?<Idle|MPos:-20.000,-20.000,-29.996|FS:0,0>


x-8 y-14 z-62
ok
?<Idle|MPos:-8.000,-14.000,-62.006|FS:0,0>


./robot/py/calibrate_pump.py

./robot/py/stream2.py robot/nc/calibrate_pump.nc /dev/ttyACM0

./robot/py/fill_boxes.py

```

## Overview
The movement of the robot is programmed in [G-code](https://en.wikipedia.org/wiki/G-code). We only need nine G-code commands to control the robot (table \@ref(tab:gCodes)).


Table: (\#tab:gCodes)G-code commands used to control robot.

Code   Description                                        
-----  ---------------------------------------------------
x      absolute position of x-axis                        
y      absolute position of y-axis                        
z      absolute position of z-axis                        
g4     dwell time (control parameter p specifies seconds) 
m3     set pump rotation to clockwise                     
m4     set pump rotation to counter clockwise             
m8     start pump                                         
m9     stop pump                                          
$h     initiate homing cycle                              

A G-code program for filling vials of food could be created manually, by listing the necessary commands sequentially in a text file.  However, this would be laborious and error prone. If the size of the boxes of vials are known, the G-code can be programmatically generated. 

## Start system {#startSystem}

1. Switch on all devices: 
 * power supply unit for gShield and motors
 * raspberry pi
 * peristaltic pump

2. Prime pump 
 * Position a beaker under the nozzle  (figure \@ref(fig:primeBeaker)).
 * Press and hold the prime button on the front of the peristaltic pump until a continuous stream of fly food is pumped into the beaker (figure \@ref(fig:primeButton))


<div class="figure" style="text-align: center">
<img src="images/prime_beaker.jpg" alt="Positioning of beaker under nozzle to collect fly food expelled during priming of peristaltic pump." width="75%" />
<p class="caption">(\#fig:primeBeaker)Positioning of beaker under nozzle to collect fly food expelled during priming of peristaltic pump.</p>
</div>


<div class="figure" style="text-align: center">
<img src="images/prime_button.jpg" alt="Prime button on peristaltic pump." width="75%" />
<p class="caption">(\#fig:primeButton)Prime button on peristaltic pump.</p>
</div>









## Determine box coordinates

<div class="figure" style="text-align: center">
<img src="images/one_box_loaded.jpg" alt="Loading boxes of vials." width="50%" /><img src="images/two_boxes_loaded.jpg" alt="Loading boxes of vials." width="50%" />
<p class="caption">(\#fig:loadBoxes2)Loading boxes of vials.</p>
</div>


First we need to determine the Cartesian coordinates of the first and last vial in each box.

1. Load boxes onto the platform of the robot (figure \@ref(fig:loadBoxes2)).
 * The first box should be flush with the fence and the guide rail.
 * The second box should be flush with the first and the guide rail.
 * The boxes we are using have a pair of double-thickness side-walls and a pair of single-thickness side-walls. The pairs are on opposite sides of the box. With this type of box it is important to note the orientation of the boxes when the Cartesian coordinates of the vials are determined, because the same orientation must be used when filling vials with food. We load the boxes with a double-thickness side-wall facing forwards.

2. Login to raspberry pi using ssh. My raspberry pi has the IP address 192.168.1.3 and so I would use:
* ``` ssh pi@192.168.1.3 ```
* Default password for the **pi** user account is 'raspberry'.

3. Use minicom to connect to the Grbl controller running on the Arduino:
```
sudo minicom -D /dev/ttyACM0 -b115200
```

4. Make sure nozzle is at ** home ** position by issuing homing command:
```
$h
```

6. First we will determine the Cartesian coordinates of the first vial in the first box; this is the vial in the front left corner. 

* Make small movements in X and Y until the nozzle is centred over this vial, *e.g.*:
```
x-8 y-8
```

* Lower the nozzle in small increments until it is just 2-3mm above the the top of the first vial (figure ), *e.g.*:
```
z-20
```

* Query the current X, Y and Z coordinates:
```
?
```
Make a note of all three coordinates. 


<div class="figure" style="text-align: center">
<img src="images/box1_first_vial.jpg" alt="Nozzle positioned over the first vial in box 1." width="50%" />
<p class="caption">(\#fig:box1FirstVial)Nozzle positioned over the first vial in box 1.</p>
</div>

<div class="figure" style="text-align: center">
<img src="images/box1_last_vial.jpg" alt="Nozzle positioned over last vial in box 1." width="50%" />
<p class="caption">(\#fig:box1LastVial)Nozzle positioned over last vial in box 1.</p>
</div>

<div class="figure" style="text-align: center">
<img src="images/box2_first_vial.jpg" alt="Nozzle positioned over the first vial in box 2." width="50%" />
<p class="caption">(\#fig:box2FirstVial)Nozzle positioned over the first vial in box 2.</p>
</div>

<div class="figure" style="text-align: center">
<img src="images/box2_last_vial.jpg" alt="Nozzle positioned over the last vial in box 2." width="50%" />
<p class="caption">(\#fig:box2LastVial)Nozzle positioned over the last vial in box 2.</p>
</div>




## Calibrate pump


## Generate G-code instructions for filling vials


