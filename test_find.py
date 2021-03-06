
import time
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
time_per_inch = 3.9 / 36

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
    print "Stopping"
    GPIO.output(EN1, False)
    PFR.stop()
    PFL.stop()
    PBR.stop()
    PBL.stop()
    GPIO.output(FL, False)
    GPIO.output(FR, False)
    GPIO.output(BL, False)
    GPIO.output(BR, False)
    GPIO.output(US, False)
 
 
def forward(duration):
    clearCommand()
    print "Moving forward " + str(duration)
    PFR.start(51.25)
    PFL.start(49.35)
    GPIO.output(EN1, True)
    time.sleep(duration)
    clearCommand()

    
def backward(duration):
    clearCommand()
    print "Moving backward " + str(duration)
    PBR.start(51.1)
    PBL.stat(48.65)
    GPIO.output(EN1,True)
    time.sleep(duration)
    clearCommand()

    
def left(duration):
    clearCommand()
    print "Moving left " + str(duration)
    PBL.start(48.65)
    PFR.start(51.25)
    GPIO.output(EN1,True)
    time.sleep(duration)
    clearCommand()

    
def right(duration):
    clearCommand()
    print "Moving right " + str(duration)
    PBR.start(51.1)
    PFL.start(54.00)
    GPIO.output(EN1,True)
    time.sleep(duration)
    clearCommand()


def stop():
    print "Stopping " + str(duration)
    clearCommand()

  
def final_turn(angle):
    if(angle < 0): # Left Turn
        abs_angle = abs(angle)
        if(abs(45-abs_angle) < abs(90-abs_angle)):
            print "Turning Left(45) " + str(abs_angle)
            left((abs_angle*deg_45)/45)
            return True
        elif(abs(45-abs_angle) >= abs(90-abs_angle)):
            print "Turning Left(90) " + str(abs_angle)
            left((abs_angle*deg_90)/90)
            return True
        else:
            return False
    else: # Right Turn
        if(abs(45-angle) < abs(90-angle)):
            print "Turning Right(45) " + str(angle)
            right((angle*deg_45)/45)
            return True
        elif(abs(45-angle) >= abs(90-angle)):
            print "Turning Right(90) " + str(angle)
            right((angle*deg_90)/90)
            return True
        else:
            return False

            
def take_pictures():
    for index in range(8):
        print("Turn " + str(index))
        print "Getting angle and distance"
        angle, distance = AngleHelper.getAngle()
        if(angle != None):
            print("Angle was: " + str(angle)) + " degrees"
            print("Distance was: " + str(distance)) + " inches"
            return angle, distance
        print("None")
        right(deg_45)
    return None, None
    
    
def search_room():
    angle, distance = take_pictures()
    if(angle != None):
        print "Found QR code at " + str(angle) + " degrees"
        final_turn(angle)
        if(distance > 72): 
            print "Moving " + str(distance / 2) + " inches"
            forward(time_per_inch * distance / 2)
            nAngle, nDistance = AngleHelper.getAngle()
            if(nAngle != None):
                angle = nAngle
                distance = nDistance
                print "Angle was: " + str(angle) + " degrees"
                print "Distance was: " + str(distance) + " inches"
                final_turn(angle)
                clearCommand()
            else:
                distance -= time_per_inch * distance / 2
                print "Did not find QR code 2nd time. Distance of " + str(distance)
        print "Moving " + str(distance) + " inches"
        forward(time_per_inch * distance)
    else:
        print("Coult Not Find the QR Code")
    
    
if __name__ == "__main__":
    setup()
    clearCommand()
    search_room()

