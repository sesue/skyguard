#--LED/Button Import--
import RPi.GPIO as GPIO
import time
#---------------------

#--Input/Output Constants--
CAMERA_LED = 17
BUTTON_PIN = 16
#--------------------------

#Initialize Input/Output
GPIO.setmode(GPIO.BCM)
GPIO.setup(CAMERA_LED,GPIO.OUT)
GPIO.setup(BUTTON_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)


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