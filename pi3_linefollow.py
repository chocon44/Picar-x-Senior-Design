  
from picarx import Picarx
from time import sleep
import time

px = Picarx()
px_power = 10
offset = 20
# px = Picarx(grayscale_pins=['A0', 'A1', 'A2'])

# Please run ./calibration/grayscale_calibration.py to Auto calibrate grayscale values
# or manual modify reference value by follow code
#px.set_line_reference([1400, 1400, 1400])


def main():
    max_time = time.time() + 7
    while time.time() < max_time:
        gm_val_list = px.get_grayscale_data()
        if gm_val_list[1] > 1000:
            px.set_dir_servo_angle(0)
            px.forward(px_power)
        
        elif (gm_val_list[0] > 1000) and (gm_val_list[1] > 1000) and (gm_val_list[2] > 1000):
            px.set_dir_servo_angle(0)
            px.forward(px_power)
        elif gm_val_list[0] > 1000:   # line is on the left -- move right
            px.set_dir_servo_angle(-offset)
            px.forward(px_power)
        elif gm_val_list[2] > 1000:   # line is on the right -- move left
            px.set_dir_servo_angle(offset)
            px.forward(px_power)
        else:
            px.stop()
    px.stop()

main()

