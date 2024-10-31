# This code is done for picar 4

from picarx import Picarx
from time import sleep
import time

px = Picarx()
px_power = 30
offset = 20
ref = 600
# px = Picarx(grayscale_pins=['A0', 'A1', 'A2'])

#px.set_line_reference([1400, 1400, 1400])

def main():
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

main()