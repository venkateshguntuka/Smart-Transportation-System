import pyrebase
import RPi.GPIO as GPIO
from time import sleep
import datetime

config = {
  "apiKey": "AIzaSyCBC47uVXIGcd27ospaSL3oagttarfQECE",
  "authDomain": "smart-transportation-system.firebaseapp.com",
  "databaseURL": "https://smart-transportation-system.firebaseio.com",
  "storageBucket": "smart-transportation-system.appspot.com",
}
def firebase_connect():
    firebase = pyrebase.initialize_app(config)
    print "Connecting to Firebase Cloud..."
    db = firebase.database()
    print "Connection to Firebase Established"
    all_tags=db.child("database").get()
    print "Connection to Database established"
    return all_tags


def print_database(all_tags):
    print "printing the contents of database"
    for tags in all_tags.each():
        print "RFID TAG VALUE: "+tags.key()
        all_values = tags.key()
        input = tags.val()
        print "RFID FINES : ",input['FINE']
        print "RFID INSURANCE : ",input['insurance']
        print "RFID LICENSE : ",input['license']
        print "RFID POLLUTION : ",input['pollution']

def firebase_lookup(all_tags, card_uid):
    found = 0
    for tags in all_tags.each():
        sts_id = tags.key()
        input = tags.val()
        dict_var = input['rfid']
        convert_val = str(dict_var['tag_value'])
        if convert_val == card_uid:
            found = 1
            break
    if found == 1:
        print "STS-ID for the given tag is : "+sts_id
    return found

def get_child(all_tags, card_uid):
    found = 0
    for tags in all_tags.each():
        sts_id = tags.key()
        input = tags.val()
        dict_var = input['rfid']
        convert_val = str(dict_var['tag_value'])
        if convert_val == card_uid:
            found = 1
            break
    return input
