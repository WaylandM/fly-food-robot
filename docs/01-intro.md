# Introduction {#intro}

The fruit fly, *Drosophila melanogaster*, is one of the most important model organisms in biological research. Maintaining stocks of fruit flies in the laboratory is labour-intensive. One task which lends itself to automation is the production of the vials of food in which the flies are reared. Fly facilities typically have to generate several thousand vials of fly food each week to sustain their fly stocks. The system presented here combines a Cartesian coordinate robot with a peristaltic pump (Figure \@ref(fig:architecture)). The design of the robot is based on the Routy CNC Router created by Mark Carew (http://openbuilds.org/builds/routy-cnc-router-v-slot-belt-pinion.101/), and uses belt and pully actuators for the X and Y axes, and a leadscrew actuator for the Z axis. CNC motion and operation of the peristaltic pump are controlled by grbl (https://github.com/gnea/grbl), an open source, embedded, high performance g-code parser. Grbl is written in optimized C and runs directly on an Arduino. A Raspberry Pi is used to generate and stream G-code instructions to Grbl. A touch screen on the Raspberry Pi provides a graphical user interface to the system. The system has capacity to fill two boxes of fly food vials at a time.  Instructions for building the hardware are available on [DocuBricks](http://docubricks.com/viewer.jsp?id=8652757760093769728).

\begin{figure}

{\centering \includegraphics[width=0.75\linewidth]{images/system_architecture} 

}

\caption{System architecture.}(\#fig:architecture)
\end{figure}
 
Software installation and configuration on the Arduino and raspberry pi are detailed in chapters \@ref(grbl) and \@ref(raspi). Chapter \@ref(gcode) explains how to program the robot to fill vials of fly food. Instructions for the routine use of the robot are provided in chapter \@ref(operation). To see a video of the robot in action, go to:

https://doi.org/10.6084/m9.figshare.5175223.v1
 
 
