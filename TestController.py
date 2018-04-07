'''from inputs import devices 
from inputs import get_gamepad

while True:
	events = get_gamepad()
	for event in events:
		print(event.ev_type, event.code, event.state)'''
from tkinter import *
from inputs import get_gamepad
from inputs import get_key
from inputs import get_mouse
'''
while 1:
	events = get_gamepad()
	for event in events:
		print(event.ev_type, event.code, event.state)

from inputs import get_key
while 1:
	events = get_key()
	for event in events:
		print(event.ev_type, event.code, event.state)

from inputs import get_mouse
while 1:
	events = get_mouse()
	for event in events:
		print(event.ev_type, event.code, event.state)
'''

def init(data):
	data.clicked = False

def mousePressed(event,data):
	print("blah blah blah") 

def keyPressed(event, data):
	print("hello1!")
	events = get_key()
	for a in events:
		if a.code == "BTN_SOUTH" and event.state == 1:
			data.clicked = True
			print("hello!")

def timerFired(data):
	pass

def redrawAll(canvas, data):
	if data.clicked:
		canvas.create_rectangle(0,0,data.width,data.height, fill = "black")

def gamepad(data):
	events = get_gamepad()
	for a in events:
		if a.code == "BTN_SOUTH" and a.state == 1:
			data.clicked = True
			print("hello!")
		elif a.code == "BTN_SOUTH" and a.state == 0:
			data.clicked = False
		
		
	'''events = get_mouse()
	for event in events:
		print(event.ev_type, event.code, event.state)'''


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def gamepadWrapper(canvas, data):
    	gamepad(data)
    	redrawAllWrapper(canvas,data)
    	canvas.after(1, gamepadWrapper, canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    #root.bind("<Button-1>", lambda event:
    #                        mousePressedWrapper(event, canvas, data))
    #root.bind("<Key>", lambda event:
    #                        keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app

    gamepadWrapper(canvas, data)
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 300)

#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.
'''
import os
import pprint
import pygame

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                
                os.system('clear')
                pprint.pprint(self.button_data)
                pprint.pprint(self.axis_data)
                pprint.pprint(self.hat_data)


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()'''