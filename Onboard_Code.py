
#to execute, run: python3.9 . /gps. py

#---GPS Imports---
import serial
import pynmea2
import time
#-----------------

#--Camera Imports--
        #import picamera
#------------------

#--LED/Button Import--
import RPi.GPIO as GPIO
#---------------------

#---File Imports---
import json
import csv
#------------------




#---Debug Constants---
DEBUG = False
#---------------------

#---Date Constants---
DAY = "01"
MONTH = "01"
YEAR = "2024"
#---------------------

#----Camera Constants----
CAMERA_RESOLUTION = (640, 480)
CAMERA_FRAMERATE = 10
RECORD_TIME_SEC = 10
#-----------------------

#--Input/Output Constants--
CAMERA_LED = 17
BUTTON_PIN = 16
#--------------------------

#----File Constants----
FRAME_INDEX_HOLDER = "0"
STANDARD_HEADING = "0.0"  # Heading for North
STANDARD_HEIGHT = "3.048" # 10ft = 3.048m
#----------------------

#--Hardware ID Constants--
BOX_MODEL_NUMBER = "1.0"
BOX_SERIAL_NUMBER = "00001"
#-------------------------


print("---Initializing Skyguard---\n")
#Initialize Camera
        #camera = picamera.PiCamera()
        #camera.resolution = CAMERA_RESOLUTION
        #camera.framerate = CAMERA_FRAMERATE

#Initialize Input/Output
GPIO.setmode(GPIO.BCM)
GPIO.setup(CAMERA_LED,GPIO.OUT)
GPIO.setup(BUTTON_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Initialize Variables
test_number = 1
metadata = {
    "boxModelNumber": BOX_MODEL_NUMBER,
    "boxSerialNumber": BOX_SERIAL_NUMBER,
    "recordStart": "-",
    "recordEnd": "-",
    "recordingTime": RECORD_TIME_SEC,
    "fps": CAMERA_FRAMERATE,
    "resolution": CAMERA_RESOLUTION
    }
    

#Wait for Button Press
while(True):
        timer = 100
        flag = True
        print("Waiting on Button to Start...\n")
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

        print("---Start Skyguard---")
        time.sleep(0.5)

        #Start Camera
#        recordingFilePath = 'data/video/recording' + str(test_number) + '.h264'
#        if(DEBUG):
#            print("> Created " + recordingFilePath)
#        camera.start_recording(recordingFilePath)
        print("> Recording")

        #Turn On Recording LED
        GPIO.output(CAMERA_LED,GPIO.HIGH)

        #Setup meta.json and frames.csv
        curr_time = time.time()
        metadata["recordStart"] = YEAR + "-" + MONTH + "-" + DAY + "T" + time.strftime('%H:') + time.strftime('%M:') + time.strftime('%S.') + str(int((curr_time - int(curr_time)) * 1000)) + "Z"

        framesFilePath = "data/framedata/frames" + str(test_number) + ".csv"
        framesWriter = csv.writer(open(framesFilePath, "w", newline = ''))
        framesWriter.writerow(["frameIndex", "timestamp", "latitude", "longitude", "heading", "groundHeightMeters"])
        
        if(DEBUG):
            print("> Created " + framesFilePath)

        while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                #Camera Loop
#                camera.wait_recording()

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
                        time_obj = time.time()
                        time_str = DATE + "T" + time.strftime('%H:') + time.strftime('%M:') + time.strftime('%S.') + str(int((time_obj - int(time_obj)) * 1000)) + "Z"
                        framesWriter.writerow([FRAME_INDEX_HOLDER, time_str, str(lat), str(lng), STANDARD_HEADING, STANDARD_HEIGHT])

        print(">Recording Stopped")
        curr_time = time.time()
        metadata["recordEnd"] = DATE + "T" + time.strftime('%H:') + time.strftime('%M:') + time.strftime('%S.') + str(int((curr_time - int(curr_time)) * 1000)) + "Z"
#        camera.stop_recording()

        #MetaData File Dump
        metaFilePath = "data/metadata/meta" + str(test_number) + ".json"
        if(DEBUG):
            print("> Created " + metaFilePath)
        json_object = json.dumps(metadata, indent=4)
        with open(metaFilePath,"w") as outfile:
                outfile.write(json_object)

        GPIO.output(CAMERA_LED,GPIO.LOW)
        print("---Stop Skyguard---\n")

        test_number += 1
        time.sleep(0.5)

print("> ---Broken Loop Skyguard---")