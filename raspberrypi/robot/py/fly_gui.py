#!/usr/bin/python

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

# graphical user interface for touch screen and g-code streamer

# stream method is based on stream.py written by Sungeun K. Jeon (https://github.com/gnea/grbl/blob/master/doc/script/stream.py)

# import modules
from Tkinter import *
import tkFont
import tkMessageBox
import os
import time

import serial
import re
import sys
import threading

class FlyGUI():
    
    def __init__(self):
        #self.loop = False
        self.continueRun = True
        self.deviceFile = "/dev/ttyACM0"
        self.homingGCode = "/home/pi/robot/nc/home.nc"
        self.fillOneBoxGCode = "/home/pi/robot/nc/1_box.nc"
        self.fillTwoBoxesGCode = "//home/pi/robot/nc/2_boxes.nc"
        #self.switchOffPumpGCode = "/home/pi/grbl/nc/switch_off_pump.nc"
        self.homeBtnBgEnabled = "#984EA3"
        self.homeBtnBgDisabled = "grey80"
        self.shutdownBtnBgEnabled = "#FF7F00"
        self.shutdownBtnBgDisabled = "grey80"
        self.stopBtnBgEnabled = "#E41A1C"
        self.stopBtnBgDisabled = "grey80"
        self.oneBoxBtnBgEnabled = "#377EB8"
        self.oneBoxBtnBgDisabled = "grey80"
        self.twoBoxesBtnBgEnabled = "#4DAF4A"
        self.twoBoxesBtnBgDisabled = "grey80"
        
    def stream(self, gCodeFile):

        self.continueRun = True
        
        RX_BUFFER_SIZE = 128

        # Initialize
        s = serial.Serial(self.deviceFile,115200)
        f = open(gCodeFile, 'r')

        # Wake up grbl
        s.write("\r\n\r\n")

        # Wait for grbl to initialize and flush startup text in serial input
        time.sleep(2)
        s.flushInput()

        # reset grbl in case started in locked condition
        s.write(chr(24) + '\n')

        # Stream g-code to grbl
        l_count = 0
 
        # Send g-code program 
        g_count = 0
        c_line = []
        # periodic() # Start status report periodic timer
        for line in f:
            if self.continueRun == False:

                s.flushInput
                #s.write(chr(24) + '\n')
                s.write("m9\n")
                f.close()
                s.close()

                return
            l_count += 1 # Iterate line counter
            # l_block = re.sub('\s|\(.*?\)','',line).upper() # Strip comments/spaces/new line and capitalize
            l_block = line.strip()
            c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
            grbl_out = '' 
            while sum(c_line) >= RX_BUFFER_SIZE-1 | s.inWaiting() :
                out_temp = s.readline().strip() # Wait for grbl response
                if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                    print "  Debug: ",out_temp # Debug response
                else :
                    grbl_out += out_temp;
                    g_count += 1 # Iterate g-code counter
                    grbl_out += str(g_count); # Add line finished indicator
                    del c_line[0] # Delete the block character count corresponding to the last 'ok'
        
            s.write(l_block + '\n') # Send g-code block to grbl
 
        # Close file and serial port
        f.close()
        s.close()
        self.continueRun=False
        time.sleep(10)
        self.activateMenu()
        
    def streamInThread(self, gCodeFile):
 
        self.deactivateMenu()
        self.thread = threading.Thread(group=None, target=self.stream, args=(gCodeFile,), kwargs={})
        self.thread.start()

    def shutdown(self):
        if tkMessageBox.askyesno("Shutdown", "Are you sure?", icon="warning"):
            os.system("sudo shutdown -h now")

    def home(self):
        self.streamInThread(self.homingGCode)
        
        
    def stop(self):
        self.continueRun = False
        time.sleep(10)
        self.activateMenu()
    
    def fillOneBox(self):
        self.streamInThread(self.fillOneBoxGCode)
   
    def fillTwoBoxes(self):
        self.streamInThread(self.fillTwoBoxesGCode)
        
    def activateMenu(self):
        self.stopBtn.config(state="disabled", bg=self.stopBtnBgDisabled)
        self.homeBtn.config(state="normal", bg=self.homeBtnBgEnabled)
        self.shutdownBtn.config(state="normal", bg=self.shutdownBtnBgEnabled)
        self.oneBoxBtn.config(state="normal", bg=self.oneBoxBtnBgEnabled)
        self.twoBoxesBtn.config(state="normal", bg=self.twoBoxesBtnBgEnabled)
        self.root.update()
    
    def deactivateMenu(self):
        self.stopBtn.config(state="normal", bg=self.stopBtnBgEnabled)
        self.homeBtn.config(state="disabled", bg=self.homeBtnBgDisabled)
        self.shutdownBtn.config(state="disabled", bg=self.shutdownBtnBgDisabled)
        self.oneBoxBtn.config(state="disabled", bg=self.oneBoxBtnBgDisabled)
        self.twoBoxesBtn.config(state="disabled", bg=self.twoBoxesBtnBgDisabled)
        self.root.update()
    
        
    def createUI(self):
        # define custom font
        customFont = tkFont.Font(family="Helvetica", size=16, weight=tkFont.BOLD)

        self.homeBtn = Button(self.root, text="Home", fg="white", bg=self.homeBtnBgEnabled, activeforeground="white", activebackground=self.homeBtnBgEnabled, font=customFont, command=self.home)
        self.homeBtn.grid(row=0, column=0, columnspan=1, rowspan=1,sticky="nesw")
        
        self.shutdownBtn = Button(self.root, text="Shutdown", fg="white", bg=self.shutdownBtnBgEnabled, activeforeground="white", activebackground=self.shutdownBtnBgEnabled, font=customFont, command=self.shutdown)
        self.shutdownBtn.grid(row=1, column=0, columnspan=1, rowspan=1, sticky="nesw")
        
        self.stopBtn = Button(self.root, text="STOP", fg="white", bg=self.stopBtnBgDisabled, activeforeground="white", activebackground=self.stopBtnBgDisabled, font=customFont, command=self.stop)
        self.stopBtn.grid(row=0, column=1, columnspan=1, rowspan=2, sticky="nesw")
        self.stopBtn.config(state="disabled")
        
        self.oneBoxBtn = Button(self.root, text="1 Box", fg="white", bg=self.oneBoxBtnBgEnabled, activeforeground="white", activebackground=self.oneBoxBtnBgEnabled, font=customFont, command=self.fillOneBox)
        self.oneBoxBtn.grid(row=2, column=0, columnspan=1, rowspan=1, sticky="nesw")
        
        self.twoBoxesBtn = Button(self.root, text="2 Boxes", fg="white", bg=self.twoBoxesBtnBgEnabled, activeforeground="white", activebackground=self.twoBoxesBtnBgEnabled, font=customFont, command=self.fillTwoBoxes)
        self.twoBoxesBtn.grid(row=2, column=1, columnspan=1, rowspan=1, sticky="nesw")
        
        self.root.geometry("320x240")
        self.root.attributes('-fullscreen', True)
        self.root.columnconfigure(0, minsize=160)
        self.root.columnconfigure(1, minsize=160)
        self.root.rowconfigure(0, minsize=60)
        self.root.rowconfigure(1, minsize=60)
        self.root.rowconfigure(2, minsize=120)

    
    def app(self):
        self.root = Tk()
        
        self.createUI()
        self.root.mainloop()
        
# ======================================================================
if __name__ == '__main__':
    
    fg = FlyGUI()
    fg.app()
