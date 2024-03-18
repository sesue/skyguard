#--LED/Button Import--
import RPi.GPIO as GPIO
import time
#---------------------

#--Input/Output Constants--
CAMERA_LED = 17
#--------------------------

#Initialize Input/Output
GPIO.setmode(GPIO.BCM)
GPIO.setup(CAMERA_LED,GPIO.OUT)

flag = True
while(True):
        print("> Flash Lights")
        if(flag):
                GPIO.output(CAMERA_LED,GPIO.HIGH)
                flag = False
        else:
                GPIO.output(CAMERA_LED,GPIO.LOW) 
                flag = True
        time.sleep(1)