from picarx import Picarx 
import math 
import time
import numpy as np
import heapq
from typing import List, Tuple
import pyrebase
#from vilib import Vilib
from robot_hat import Motors


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




car = Picarx() 

def main():
    # Initialize Firebase
    firebase = pyrebase.initialize_app(config)
    database = firebase.database()

    data = {
        "Presence": 1}
        
    database.child("Emergency vehicle").set(data)

    speed = 50
    car.set_motor_speed(1, speed) #right motor
    #car.set_motor_speed(2,-1*speed+20)   # left motor
    time.sleep(3)

    time.sleep(3)
    car.stop() 
    data = {
        "Presence": 0}
        
    database.child("Emergency vehicle").set(data)

main()