#
# Last updated 10/29/24
#

import time
from pyrebase import pyrebase
from vilib import Vilib

#-------- Firebase -----------#

config = {
    'apiKey': "AIzaSyBL9UezOELm7LsBLvfZdlJDkhCTZQAKlx4",
      'authDomain': "jetbot-ece-493.firebaseapp.com",
      'projectId': "jetbot-ece-493",
      'storageBucket': "jetbot-ece-493.appspot.com",
      'messagingSenderId': "906874678062",
      'appId': "1:906874678062:web:6c50c28e26fbb59c0ca8bf",
      'databaseURL': "https://jetbot-ece-493-default-rtdb.firebaseio.com/"
    }
    

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
database = firebase.database()

def main():
	Vilib.camera_start()
	Vilib.display()	
	Vilib.color_detect("red")
	
	while True:
		if Vilib.detect_obj_parameter['color_n'] != 0:	# if red is detected...
			data = { "Red light detected": 1}			# database value is 1
			database.child("Picam pico").set(data)
			print("Red detected")
		else:											# if no red is detected...
			data = { "Red light detected": 0}			# databse value is 0
			database.child("Picam pico").set(data)
			

if __name__ == "__main__":
	try:
		main()
	finally:
		Vilib.camera_close()
