from picarx import Picarx
from time import sleep
import time

px = Picarx()

def main():
    while True:
        gm_val_list = px.get_grayscale_data()
        for val in gm_val_list:
            print (val, end =" ")
        print()

main()