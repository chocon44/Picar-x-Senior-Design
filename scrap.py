# Monitor while car drives
# only for pi4, pi3 cannot pivot

from picarx import Picarx
from time import sleep
import readchar
import time

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

def show_info():
    print("\033[H\033[J",end='')  # clear terminal windows
    print(manual)


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
        show_info()
        power = 30
        turnPower = 50
        ref = 550
        offset = 20
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('wsadikjlgh'):        # added g and h
                if 'w' == key:          # go forward 
                    #px.set_dir_servo_angle(0)
                    #px.forward(power)
                    max_time = time.time() + 1
                    while time.time() < max_time:
                        gm_val_list = px.get_grayscale_data()
                        if gm_val_list[1] > ref:
                            px.set_dir_servo_angle(0)
                            px.forward(power)

                        elif (gm_val_list[0] > ref) and (gm_val_list[1] > ref) and (gm_val_list[2] > ref):
                            px.set_dir_servo_angle(0)
                            px.forward(power)
                        elif gm_val_list[0] > ref:   # line is on the left -- move right
                            px.set_dir_servo_angle(-offset)
                            px.forward(power)
                        elif gm_val_list[2] > ref:   # line is on the right -- move left
                            px.set_dir_servo_angle(offset)
                            px.forward(power)
                        else:
                            px.stop()

                elif 's' == key:        # go backward
                    px.set_dir_servo_angle(0)
                    px.backward(power)
                elif 'a' == key:        # turn left with servo
                    px.set_dir_servo_angle(-35)
                    px.forward(power)
                elif 'd' == key:        # turn right with servo
                    px.set_dir_servo_angle(35)
                    px.forward(power)
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
                show_info()
                sleep(0.5)
                px.forward(0)

            elif key == readchar.key.CTRL_C:
                print("\n Quit")
                break

    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)
        px.set_dir_servo_angle(0)
        px.stop()
        sleep(.2)
