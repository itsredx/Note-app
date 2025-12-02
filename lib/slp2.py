import time
import datetime

def detect_sleep_by_time():
    last_check_time = time.time()
    while True:
        time.sleep(5)  # Check every 5 seconds
        current_time = time.time()
        time_difference = current_time - last_check_time
        if time_difference > 10:  # If more than 10 seconds have passed
            print(f"System likely resumed from sleep at {datetime.datetime.now()}")
            # You can trigger your desired action here
        last_check_time = current_time

if __name__ == '__main__':
    detect_sleep_by_time()