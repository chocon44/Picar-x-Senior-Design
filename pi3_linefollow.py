from picarx import Picarx
from time import sleep
import time 

px = Picarx()
# px = Picarx(grayscale_pins=['A0', 'A1', 'A2'])

# Please run ./calibration/grayscale_calibration.py to Auto calibrate grayscale values
# or manual modify reference value by follow code
#px.set_line_reference([0, 1300, 0])

current_state = None
px_power = 10
offset = 20
last_state = "stop"

def outHandle():
    global last_state, current_state
    if last_state == 'left':
        px.set_dir_servo_angle(-30)
        px.backward(10)
    elif last_state == 'right':
        px.set_dir_servo_angle(30)
        px.backward(10)
    while True:
        gm_val_list = px.get_grayscale_data()
        gm_state = get_status(gm_val_list)
        print("outHandle gm_val_list: %s, %s"%(gm_val_list, gm_state))
        currentSta = gm_state
        if currentSta != last_state:
            break
    sleep(0.01)

def get_status(val_list):
    _state = px.get_line_status(val_list)  # [bool, bool, bool], 0 means line, 1 means background
    if _state == [0, 0, 0]:     # no line detected
        return 'stop'
    elif _state == [0,0,1]:     # line on the right
        return 'left'           # move left
    elif _state == [0,1,0]:     # line on the middle
        return 'forward'        # go forward
    elif _state == [0,1,1]:     # line on slight right
        return 'slight left'           # go left 
    elif _state == [1,1,0]:     # line on slight left
        return 'slight right'          # go right
    elif _state == [1,1,1]:     # all three sensors got the line
        return 'stop'

if __name__=='__main__':
    try:
        time_end = time.time() + 7
        while time.time() <= time_end:
            gm_val_list = px.get_grayscale_data()
            gm_state = get_status(gm_val_list)
            print("gm_val_list: %s, %s"%(gm_val_list, gm_state))

            if gm_state != "stop":
                last_state = gm_state
            if gm_state == 'forward':
                px.set_dir_servo_angle(0)
                px.forward(px_power)
            elif gm_state == 'left':
                px.set_dir_servo_angle(offset)
                px.forward(px_power)
            elif gm_state == 'slight left':
                px.set_dir_servo_angle(offset-10)
                px.forward(px_power)
            elif gm_state == 'right':
                px.set_dir_servo_angle(-offset)
                px.forward(px_power)
            elif gm_state == 'slight right':
                px.set_dir_servo_angle(-offset+10)
                px.forward(px_power)
            else:
                outHandle()
    finally:
        px.stop()
        print("stop and exit")
        sleep(0.1)