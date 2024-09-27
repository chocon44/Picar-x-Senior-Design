#NOTES: ADDED ATTRIBUTE TO ROOT FILE AND RE-INSTALLED, LEFT AND RIGHT FUNCTIONS WORKED,
# ANGLES DEPEND ON TIME.SLEEP()
# ADDED ULTRA SERVO SUCCESSFULLY


from picarx import Picarx
import math
import time


car = Picarx()

def test_motors():  # passed
    car = Picarx()
    
    car.left(30)
    time.sleep(2)
    car.stop()
    time.sleep(1)
    car.right(30)
    time.sleep(1.8)
    car.stop()

def ultra():    # passed
    car.stop()
    




def main():
    car = Picarx()
    
    ultra() 
  

main()

car.stop()
