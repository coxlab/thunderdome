# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:28:20 2013

@author: Godwin
"""

from flask import (Flask,
                   g,
                   request,
                   render_template,
                   redirect,
                   url_for,
                   jsonify,
                   abort)
#Basic imports
from ctypes import *
import sys
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, PositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.Devices.Servo import ServoTypes

#open phidget control board 
advancedServo = AdvancedServo()

def Attached(e):
    attached = e.device
    print("Servo %i Attached!" % (attached.getSerialNum()))


advancedServo.openRemoteIP('127.0.0.1', 5001)

#attach phidget, engage motors, and set them to default position 
advancedServo.waitForAttach(100000)
for k in range(0,8):
    advancedServo.setServoType(k, ServoTypes.PHIDGET_SERVO_HITEC_HS422)
    advancedServo.setEngaged(k, True)
    advancedServo.setVelocityLimit(k, 100.00)
    if k % 2 == 0:
		advancedServo.setPosition(k,0)
    elif k % 2 == 1:
		advancedServo.setPosition(k,180)

    

    

#_______________________________________________________________________________________________________
# -------------------------------------------------------
# Flask App Setup (flask + flask-restful)
# -------------------------------------------------------

app = Flask(__name__)
   
@app.route('/')
def index():
    return render_template('gui2.html')

#@app.route('/start')


@app.route('/door1')
def open1():
    if advancedServo.getPosition(0) == 0 and advancedServo.getPosition(1) == 180:
        advancedServo.setPosition(0, 90.00)
        advancedServo.setPosition(1, 90.00)
    elif advancedServo.getPosition(0) == 90 and advancedServo.getPosition(1) == 90:
        advancedServo.setPosition(0, 0.00)
        advancedServo.setPosition(1, 180.00)
    return render_template('gui2.html')

@app.route('/door2')
def door2():
    if advancedServo.getPosition(2) == 0 and advancedServo.getPosition(3) == 180:
        advancedServo.setPosition(2, 90.00)
        advancedServo.setPosition(3, 90.00)
    elif advancedServo.getPosition(2) == 90 and advancedServo.getPosition(3) == 90:
        advancedServo.setPosition(2, 0.00)
        advancedServo.setPosition(3, 180.00)
    return render_template('gui2.html')

@app.route('/door3')
def door3():
    if advancedServo.getPosition(4) == 0 and advancedServo.getPosition(5) == 180:
        advancedServo.setPosition(4, 90.00)
        advancedServo.setPosition(5, 90.00)
    elif advancedServo.getPosition(4) == 90 and advancedServo.getPosition(5) == 90:
        advancedServo.setPosition(4, 0.00)
        advancedServo.setPosition(5, 180.00)
    return render_template('gui2.html')

#all door controls
@app.route('/alldoors')
def omnidoor():
	for k in range (0,8):
		if k % 2 == 0:
			if advancedServo.getPosition(k) == 0:
				advancedServo.setPosition(k, 90.00)
				advancedServo.setPosition(k+1, 90.00)
			elif advancedServo.getPosition(k) == 90:
				advancedServo.setPosition(k, 0.00)
				advancedServo.setPosition(k+1, 180.00)
        return render_template('gui2.html')

@app.route('/alldoors_open')
def omnidoor_o():
    for k in range(0,8):
		if k % 2 == 0:
			if advancedServo.getPosition(k) == 0:
				advancedServo.setPosition(k, 90.00)
				advancedServo.setPosition(k+1, 90.00)		
    return render_template('gui2.html')

@app.route('/alldoors_close')
def omnidoor_c():
    for k in range(0,8):
            if k % 2 == 0:
			if advancedServo.getPosition(k) == 90:
				advancedServo.setPosition(k, 0.00)
				advancedServo.setPosition(k+1, 180.00)		
    return render_template('gui2.html')

@app.route('/shutdown')
def shutdown():
    for k in range(0,8):
        advancedServo.setEngaged(k, False)    
    return render_template('gui2.html')
#Door States    
@app.route('/door_state1')
def DoorState1():
    if advancedServo.getEngaged(0) == True and advancedServo.getEngaged(1) == True:
        return "Door1 is ON"
    elif advancedServo.getEngaged(0) == False or advancedServo.getEngaged(1) == False:
        return "Door1 is OFF"

@app.route('/door_state2')
def DoorState2():
    if advancedServo.getEngaged(2) == True and advancedServo.getEngaged(3) == True:
        return "Door2 is ON"
    elif advancedServo.getEngaged(1) == False or advancedServo.getEngaged(3) == False:
        return "Door2 is OFF"

@app.route('/door_state3')
def DoorState3():
    if advancedServo.getEngaged(4) == True and advancedServo.getEngaged(5) == True:
        return "Door3 is ON"
    elif advancedServo.getEngaged(4) == False or advancedServo.getEngaged(5) == False:
        return "Door3 is OFF"
# Door open or closed 
@app.route('/door_open_close1')
def Dooropenclose():
    if advancedServo.getEngaged(0) == False or advancedServo.getEngaged(1) == False:
        return "Door1 is not on"
    elif advancedServo.getEngaged(0) == True and advancedServo.getEngaged(1) == True:
        if advancedServo.getPosition(0) == 90 and advancedServo.getPosition(1) == 90:
            return "Door1 is OPEN"
        elif advancedServo.getPosition(0) == 0 and advancedServo.getPosition(1) == 180.00:
            return "Door1 is CLOSED"    

@app.route('/door_open_close2')
def Dooropenclose2():
    if advancedServo.getEngaged(2) == False or advancedServo.getEngaged(3) == False:
        return "Door2 is not on"
    elif advancedServo.getEngaged(2) == True and advancedServo.getEngaged(3) == True:
        if advancedServo.getPosition(2) == 90 and advancedServo.getPosition(3) == 90:
            return "Door2 is OPEN"
        elif advancedServo.getPosition(2) == 0 and advancedServo.getPosition(3) == 180.00:
            return "Door2 is CLOSED" 
            
@app.route('/door_open_close3')
def Dooropenclose3():
    if advancedServo.getEngaged(4) == False or advancedServo.getEngaged(5) == False:
        return "Door3 is not on"
    elif advancedServo.getEngaged(4) == True and advancedServo.getEngaged(5) == True:
        if advancedServo.getPosition(4) == 90 and advancedServo.getPosition(5) == 90:
            return "Door3 is OPEN"
        elif advancedServo.getPosition(4) == 0 and advancedServo.getPosition(5) == 180.00:
            return "Door3 is CLOSED" 
#Door position 
@app.route('/door_posit1')
def doorposition1():
	if advancedServo.getEngaged(0) == True and advancedServo.getEngaged(1) == True:
		return str(advancedServo.getPosition(0))

@app.route('/door_posit2')
def doorposition2():
    if advancedServo.getEngaged(2) == True and advancedServo.getEngaged(3) == True:
		return str(advancedServo.getPosition(2))

@app.route('/door_posit3')
def doorposition3():
    if advancedServo.getEngaged(4) == True and advancedServo.getEngaged(5) == True:
		return str(advancedServo.getPosition(4))
# -------------------------------------------------------
# Debug
# -------------------------------------------------------
if __name__ == "__main__":
    app.run(port=2667, debug=True)


#______________________________________________________________________________________________________


 


    
