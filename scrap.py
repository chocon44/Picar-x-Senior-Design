from picarx import Picarx
import time

POWER = 30
SafeDistance = 40   # > 40 safe
DangerDistance = 10 # > 20 && < 40 turn around,
                    # < 20 backward

def main():
    try:
        px = Picarx()
        # px = Picarx(ultrasonic_pins=['D2','D3']) # tring, echo

        while True:
            
            px.forward(30)
            time.sleep(1)
            distance = round(px.ultrasonic.read(), 2)
            print("distance: ",distance)
            
            

    finally:
        px.forward(0)


if __name__ == "__main__":
    main()
