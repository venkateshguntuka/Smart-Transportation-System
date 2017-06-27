#importing the required libraries
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import datetime
from firebase_connector import firebase_connect,print_database
from firebase_connector import firebase_lookup,get_child
#control flag to start and stop loop
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

#set the bcm mode
RED_LED = 5
GREEN_LED = 38
BLUE_LED = 40
GPIO.setwarnings(False)

def validate(child):
    pollution_expiry = str(child['pollution']['last_date'])
    license_expiry = str(child['license']['last_date'])
    insurance_expiry = str(child['insurance']['last_date'])
    reg_expiry = str(child['vehicle_details']['last_date'])

    current_date = (datetime.date.today())

    pollution=datetime.date(int(pollution_expiry[6:]), int(pollution_expiry[3:5]), int(pollution_expiry[0:2]))
    license = datetime.date(int(license_expiry[6:]), int(license_expiry[3:5]), int(license_expiry[0:2]))
    insurance = datetime.date(int(insurance_expiry[6:]), int(insurance_expiry[3:5]), int(insurance_expiry[0:2]))
    reg = datetime.date(int(reg_expiry[6:]),int(reg_expiry[3:5]), int(reg_expiry[0:2]))

    flags = {}

    if pollution < current_date:
        print "pollution check has expired"
        flags['poll_flag'] = 1
    if license < current_date:
        print "license has expired"
        flags['lic_flag'] = 1
    if insurance < current_date:
        print "insurance has expired"
        flags['ins_flag'] = 1
    if reg < current_date:
        print "registration has expired"
        flags['reg_flag'] = 1
    if len(flags) == 0:
        print "ALL OK!"

    return flags



# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "\n\n"
print "****************************************************************"
print "Welcome to the Smart transportation system"
print "****************************************************************"
print "\n"
print "Note : Press Ctrl-C to stop."
print "\n"
print "Place the STS tags on the reader"
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
       
        #get the child tag of the given card
        child = get_child(all_tags, card_uid)

        #validate the given credentials
        fgs = validate(child)
        #print fgs
        GPIO.setup(RED_LED,GPIO.OUT)
        GPIO.setup(GREEN_LED,GPIO.OUT)
        if len(fgs) > 0:
            GPIO.output(RED_LED,True)
            time.sleep(10)
            GPIO.output(RED_LED,False)
        else:
            GPIO.output(GREEN_LED,True)
            time.sleep(10)
            GPIO.output(GREEN_LED,False)

       # Print UID
       # print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        card_uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
        print "STS tag read "
        print "STS UID: "+card_uid
        print "\n\n"

        #calls the method from firebaseconnector
        #connects to the firebase cloud
        all_tags = firebase_connect()


        #authenicates whether the card_uid exists in the databse or not
        res = firebase_lookup(all_tags,card_uid)
        print "\n\nAuthenticating the sts-tag..."
        if res == 1:
            print "Result : Valid card!"
        else:
            print "Result : Invalid card!"
            continue_reading = False
            GPIO.setup(BLUE_LED,GPIO.OUT)
            GPIO.output(BLUE_LED,True)
            time.sleep(10)
            GPIO.output(BLUE_LED,False)
            break


        #get the child tag of the given card
        child = get_child(all_tags, card_uid)

        #validate the given credentials
        fgs = validate(child)
        #print fgs
        GPIO.setup(RED_LED,GPIO.OUT)
        GPIO.setup(GREEN_LED,GPIO.OUT)
        if len(fgs) > 0:
            GPIO.output(RED_LED,True)
            time.sleep(10)
            GPIO.output(RED_LED,False)
        else:
            GPIO.output(GREEN_LED,True)
            time.sleep(10)
            GPIO.output(GREEN_LED,False)
