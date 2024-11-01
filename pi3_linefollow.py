# This code is done for picar 3

from picarx import Picarx
from time import sleep
import time
import pyrebase 

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

firebase = pyrebase.initialize_app(config)
database = firebase.database()


px = Picarx()
px_power = 30
offset = 20
ref = 600
# px = Picarx(grayscale_pins=['A0', 'A1', 'A2'])

#px.set_line_reference([1400, 1400, 1400])

def main():
    data = {
        "Presence": 1}
        
    database.child("Emergency vehicle").set(data)
    time.sleep(3)    # notify for 3 sec before emergency car starts moving
    
    max_time = time.time() + 10
    while time.time() < max_time:
        gm_val_list = px.get_grayscale_data()
        if gm_val_list[1] > ref:
            px.set_dir_servo_angle(0)
            px.forward(px_power)

        elif (gm_val_list[0] > ref) and (gm_val_list[1] > ref) and (gm_val_list[2] > ref):
            px.set_dir_servo_angle(0)
            px.forward(px_power)
        elif gm_val_list[0] > ref:   # line is on the left -- move right
            px.set_dir_servo_angle(-offset)
            px.forward(px_power)
        elif gm_val_list[2] > ref:   # line is on the right -- move left
            px.set_dir_servo_angle(offset)
            px.forward(px_power)
        else:
            px.stop()
    px.stop()
    data = {
        "Presence": 0}
        
    database.child("Emergency vehicle").set(data)
   


main()
