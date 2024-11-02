from picarx import Picarx
import time

POWER = 40
SafeDistance = 40   # > 40 safe
DangerDistance = 10 # > 20 && < 40 turn around,
                    # < 20 backward

def main():
    px = Picarx()
    px.forward(30)
    time.sleep(0.7)
    px.stop()
            



if __name__ == "__main__":
    main()
