import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import sys



def setup(self):
    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()
    print "Welcome to the Workshop Riset Infromatika"
    reading(True)


def reading(self, continue_reading):
    while continue_reading:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print "Card detected"
            validasi()
        (status, uid) = MIFAREReader.MFRC522_Anticoll()


def autentikasi():
    print "card read uid: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
    uuid = "%s%s%s%s" % (uid[0], uid[1], uid[2], uid[3])

    key = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]

    MIFAREReader.MFRC522_SelectTag(uid)
    status = MIFAREReader.MFRC522_Auth(
        MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

    # Check if authenticated
    if status == MIFAREReader.MI_OK:
        MIFAREReader.MFRC522_Read(8)
        client.cek_status(str(uuid))
        MIFAREReader.MFRC522_StopCrypto1()
        end_read()
    else:
        print "Authentication error"


def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = True
    GPIO.cleanup()
    
setup()
