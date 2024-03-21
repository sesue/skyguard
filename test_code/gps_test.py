#to execute, run: python3.9 ./gps.py
import serial
import pynmea2

print("---Running GPS Test---")
#f = open("gpsdata.txt", "a")
while True:
        port="/dev/ttyAMA0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata=ser.readline()
        n_data = newdata.decode('latin-1')
        if n_data[0:6] == '$GPRMC':
                newmsg=pynmea2.parse(n_data)
                lat=newmsg.latitude
                lng=newmsg.longitude
                gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
                print("> " + gps)
                latClng = str(lat) + "," + str(lng) + "\n"
                f = open("gpsdata.txt", "a")
                f.write(latClng)
                f.close()
