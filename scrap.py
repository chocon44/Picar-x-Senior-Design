# Monitor while car drives
# only for pi4, pi3 cannot pivot

from picarx import Picarx
from time import sleep
import readchar
import time
from robot_hat import Motors

manual = '''
Press keys on keyboard to control PiCar-X!
    w: Forward
    a: Turn left
    s: Backward
    d: Turn right
    g: Pivot left          
    h: Pivot right
    j: Turn head left
    l: Turn head right
    
    i: Head up
    k: Head down
    
    ctrl+c: Quit
'''

#def show_info():
    #print("\033[H\033[J",end='')  # clear terminal windows
    #print(manual)





def main():
    px = Picarx()
    px.forward(20)
    time.sleep(0.2)
    px.stop()
            


if __name__ == "__main__":
    try:
        pan_angle = 0
        tilt_angle = 0
        px = Picarx()
        #show_info()
        power = 10
        turnPower = 50
        ref = 550
        offset = 20
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('wsadikjlghqe'):        # added g and h
                if 'w' == key:          # go forward 
                    px.set_dir_servo_angle(0)
                    px.forward(power)
                    #px.set_motor_speed(1, power+40)
                    #px.set_motor_speed(2, -1*power-20)  
                   
                elif 'q' == key:        # look left 
                    px.set_cam_pan_angle(35)
                    time.sleep(1)
                    px.set_dir_servo_angle(0)
                elif 'e' == key:        # look right
                    px.set_cam_pan_angle(-35)
                    time.sleep(1)
                    px.set_dir_servo_angle(0)
                elif 's' == key:        # go backward
                    px.set_dir_servo_angle(0)
                    px.backward(power)
                elif 'a' == key:        # turn left with servo -- pivot left no servo
                    px.set_dir_servo_angle(0)
                    px.left(turnPower)
                    #px.set_dir_servo_angle(-35)
                    #px.forward(power)
                elif 'd' == key:        # turn right with servo
                    #px.set_dir_servo_angle(35)
                    #px.forward(power)
                    px.set_dir_servo_angle(0)
                    px.right(turnPower)
                elif 'g' == key:        # pivot left 
                    px.set_dir_servo_angle(0)
                    px.left(turnPower)
                elif 'h' == key:        # pivot right 
                    px.set_dir_servo_angle(0)
                    px.right(turnPower)
                
                elif 'i' == key:                      
                    tilt_angle+=5
                    if tilt_angle>35:
                        tilt_angle=35
                elif 'k' == key:
                    tilt_angle-=5
                    if tilt_angle<-35:
                        tilt_angle=-35
                elif 'l' == key:        # head left 
                    pan_angle+=5
                    if pan_angle>35:
                        pan_angle=35
                elif 'j' == key:        # head right
                    pan_angle-=5
                    if pan_angle<-35:
                        pan_angle=-35

                px.set_cam_tilt_angle(tilt_angle)
                px.set_cam_pan_angle(pan_angle)
                #show_info()
                sleep(0.4)          # time for each movement
                px.forward(0)

            elif key == readchar.key.CTRL_C:
                print("\n Quit")
                break

    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)
        px.set_dir_servo_angle(0)
        px.stop()
        sleep(.5)
