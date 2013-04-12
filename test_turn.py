
from time import time
import RPi.GPIO as GPIO
import AngleHelper

FR = 2
FL = 17
BR = 3
BL = 27
US = 4
EN1 = 22
EN2 = 23
EN3 = 24
EN4 = 25
PFR = None
PFL = None
PBR = None
PBL = None

# Sleep Times for Degree Turns
deg_90 = .73
deg_45 = .405
inches_36 = 3.9

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(FL, GPIO.OUT)
    GPIO.setup(FR, GPIO.OUT)
    GPIO.setup(BL, GPIO.OUT)
    GPIO.setup(BR, GPIO.OUT)
    GPIO.setup(US, GPIO.OUT)
    enableEverything()
    global PFR
    global PFL
    global PBR
    global PBL
    PFR = GPIO.PWM(FR, 200)
    PFL = GPIO.PWM(FL, 200)
    PBR = GPIO.PWM(BR, 200)
    PBL = GPIO.PWM(BL, 200)
    
    
def enableEverything():
    GPIO.setup(EN1, GPIO.OUT)
    GPIO.setup(EN2, GPIO.OUT)
    GPIO.setup(EN3, GPIO.OUT)
    GPIO.setup(EN4, GPIO.OUT)
    GPIO.output(EN1, True)
    GPIO.output(EN2, True)
    GPIO.output(EN3, True)
    GPIO.output(EN4, True)

    
def clearCommand():
    GPIO.output(EN1, False)
    GPIO.output(FL, False)
    GPIO.output(FR, False)
    GPIO.output(BL, False)
    GPIO.output(BR, False)
    GPIO.output(US, False)
    PFR.stop()
    PFL.stop()
    PBR.stop()
    PBL.stop()
 
 
def forward(duration):
    clearCommand()
    PFR.start(51.25)
    PFL.start(49.35)
    GPIO.output(EN1, True)
    start_time = time()
    while(time() - start_time < duration):
        continue
    clearCommand()

    
def backward(duration):
    clearCommand()
    PBR.start(51.1)
    PBL.stat(48.65)
    GPIO.output(EN1,True)
    start_time = time()
    while(time() - start_time < duration):
        continue
    clearCommand()

    
def left(duration):
    clearCommand()
    PBL.start(48.65)
    PFR.start(51.25)
    GPIO.output(EN1,True)
    start_time = time()
    while(time() - start_time < duration):
        continue
    clearCommand()

    
def right(duration):
    clearCommand()
    PBR.start(51.1)
    PFL.start(53.5)
    GPIO.output(EN1,True)
    start_time = time()
    while(time() - start_time < duration):
        continue
    clearCommand()
  
  
def stop(duration):
    clearCommand()
    start_time = time()
    while(time() - start_time < duration):
        continue
    clearCommand()

    
def test():
    setup()
    for index in range(8):
        right(deg_45)
        stop(2)
test()


