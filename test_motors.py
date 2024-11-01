from picarx import Picarx
from time import sleep
import time
from vilib import Vilib
import math

px = Picarx()
px_power = 30
offset = 20
ref = 100
short = 0.85
long = 1.65     # time to travel 1 block 

def reset_dir_servo():
    px.set_dir_servo_angle(0)

def main():
    try:
        Vilib.camera_close()
       
        px.set_dir_servo_angle(30)
        px.forward(20)
        sleep(1)  # Give servo time to turn
        #px.forward(20)
        #time.sleep(0.4)
        
        #time_max = time.time() + 3 
        #while time.time() <= time_max:
        #    gm_val_list = px.get_grayscale_data()
        #    print("Grayscale values:", gm_val_list)  # Debug print
            
        #    if any(val > ref for val in gm_val_list):
        #        print("Line detected, stopping")
        #        px.stop()
        #        break
        #    else:
        #        print("Moving forward")
        #        px.forward(20)
        #        sleep(0.1)  # Small delay to prevent CPU overload
                
   
        
    finally: 
        px.stop()
        reset_dir_servo()

if __name__ == "__main__":
    main()
