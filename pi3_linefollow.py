from picarx import Picarx
from time import sleep
import time

px = Picarx()
px_power = 10  # This is quite low, might need to increase
offset = 20

def main():
    print("Starting line follower program...")
    print("Initial setup complete. Power:", px_power, "Offset:", offset)
    
    # Test basic movement first
    print("Testing basic movement...")
    px.forward(px_power)
    sleep(1)
    px.stop()
    print("Basic movement test complete")
    sleep(1)
    
    max_time = time.time() + 7
    print("Starting main loop. Will run for 7 seconds.")
    
    while time.time() < max_time:
        gm_val_list = px.get_grayscale_data()
        print(f"Grayscale values: Left: {gm_val_list[0]}, Center: {gm_val_list[1]}, Right: {gm_val_list[2]}")
        
        if gm_val_list[1] > 1000:
            print("Center sensor detected line - moving forward")
            px.set_dir_servo_angle(0)
            px.forward(px_power)
        
        elif all(val > 1000 for val in gm_val_list):
            print("All sensors detected line - moving forward")
            px.set_dir_servo_angle(0)
            px.forward(px_power)
            
        elif gm_val_list[0] > 1000:
            print("Left sensor detected line - turning right")
            px.set_dir_servo_angle(-offset)
            px.forward(px_power)
            
        elif gm_val_list[2] > 1000:
            print("Right sensor detected line - turning left")
            px.set_dir_servo_angle(offset)
            px.forward(px_power)
            
        else:
            print("No line detected - stopping")
            px.stop()
            
        sleep(0.1)  # Small delay to prevent overwhelming the system
        
    print("Time limit reached - stopping")
    px.stop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
        px.stop()
    finally:
        print("Program ended")