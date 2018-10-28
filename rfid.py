import RPi.GPIO as GPIO
import sys
sys.path.insert(0,'MFRC522')
import MFRC522
import signal
import time
import requests
from Stepper

print 'Workshop Dan Riset Informatika'

GPIO.setwarnings(False)
GPIO.setup(8, GPIO.OUTPUT)

continue_reading = True
MIFAREReader = MFRC522.MFRC522()

while continue_reading:

    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        print "Card detected"
        print "card read uid: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
        uuid = "%s%s%s%s" % (uid[0], uid[1], uid[2], uid[3])
        api_wri = requests.get('http://127.0.0.1:5000/smartlock/wri/api/v1/{}/'.format(uuid))

        if api_wri.status_code == 200:

            stateRFID = GPIO.input(8)

            if stateRFID == 0:
                GPIO.output(8,GPIO.HIGH)
                stepper_jalan(0)

            if stateRFID == 1:
                GPIO.output(8,GPIO.LOW)
                stepper_jalan(1)
        time.sleep(.5)
