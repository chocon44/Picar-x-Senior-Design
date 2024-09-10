from picarx import Picarx
import math
import time

def LaneChecking():    # this function checks for black line
   
    print("Lane check")
    car = Picarx()
    
    # read data from grayscale
    gm_val_list = car.get_grayscale_data()
    return gm_val_list
    
    
