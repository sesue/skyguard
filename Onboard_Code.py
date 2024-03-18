
#to execute, run: python3.9 . /gps. py

#---GPS Imports---
import serial
import pynmea2
import time
#-----------------

#--Camera Imports--
import picamera
#------------------

#--LED/Button Import--
import RPi.GPIO as GPIO
#---------------------

#---Debug Constants---
DEBUG = False
#---------------------


#----Camera Constants----
RECORD_TIME_SEC = 10
CAMERA_RESOLUTION = (640, 480)
RESOLUTION_FIRST_STR = "640"
RESOLUTION_SECOND_STR = "480"
CAMERA_FRAMERATE = 10
FRAMERATE_STR = "10"
DATE = "UNKNOWN_DATE"
#-----------------

#--Input/Output Constants--
CAMERA_LED = 17
BUTTON_PIN = 16
#--------------------------


print("> Initializing Skyguard")
#Initialize Camera
camera = picamera.PiCamera()
camera.resolution = CAMERA_RESOLUTION
camera.framerate = CAMERA_FRAMERATE

#Initialize Input/Output
GPIO.setmode(GPIO.BCM)
GPIO.setup(CAMERA_LED,GPIO.OUT)
GPIO.setup(BUTTON_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Initialize Variables
test_number = 1

print("> ---Starting Skyguard---")

#Wait for Button Press
while(True):
        timer = 100
        flag = True
        print("> Waiting on Button...")
        while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                if(timer <= 0):
                        if(flag):
                                GPIO.output(CAMERA_LED,GPIO.HIGH)
                                flag = False
                        else:
                                GPIO.output(CAMERA_LED,GPIO.LOW) 
                                flag = True
                        timer = 100

        time.sleep(0.01)
        timer -= 1

        print("> ---Start Recording---")

        #Start Camera
        camera.start_recording('data/video/skyguard_' + DATE + '_test' + str(test_number) + '_' + RESOLUTION_FIRST_STR + 'x' + RESOLUTION_SECOND_STR + '_FR' + FRAMERATE_STR + '.h264')

        #Turn On Recording LED
        GPIO.output(CAMERA_LED,GPIO.HIGH)

        #Setup Loop Time
        curr_time = time.time()
        f = open("data/test" + str(test_number) + "_data.txt", "a")
        time_str = time.strftime('%H:') + time.strftime('%M:') + time.strftime('%S.') + str(int((curr_time - int(curr_time)) * 1000)) + "\n"
        final_str = "Video Start: " + time_str
        f.write(final_str)
        f.close()

        while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                #Camera Loop
                camera.wait_recording()

                #GPS Loop
                port="/dev/ttyAMA0"
                ser=serial.Serial(port, baudrate=9600, timeout=0.5)
                dataout = pynmea2.NMEAStreamReader()
                newdata=ser.readline()
                n_data = newdata.decode('latin-1')
                if n_data[0:6] == '$GPRMC':
                        if(DEBUG):
                                print("> Receiving GPS Data")
                        newmsg=pynmea2.parse(n_data)
                        lat=newmsg.latitude
                        lng=newmsg.longitude
                        latClng = str(lat) + "," + str(lng)
                        time_obj = time.time()
                        time_str = time.strftime('%H:') + time.strftime('%M:') + time.strftime('%S.') + str(int((time_obj - int(time_obj)) * 1000)) + "\n"
                        final_str = latClng + "," + time_str
                        f = open("data/gps/gps_test" + test_number + ".txt", "a")
                        f.write(final_str)
                        f.close()

        print("> ---Stop Recording---")
        curr_time = time.time()
        f = open("data/test" + test_number + "_data.txt", "a")
        time_str = time.strftime('%H:') + time.strftime('%M:') + time.strftime('%S.') + str(int((curr_time - int(curr_time)) * 1000)) + "\n"
        final_str = "Video End: " + time_str
        f.write(final_str)
        f.close()
        camera.stop_recording()

        GPIO.output(CAMERA_LED,GPIO.LOW)

        test_number += 1

print("> ---Ending Skyguard---")