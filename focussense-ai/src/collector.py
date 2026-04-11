import time
import pandas as pd
from pynput import keyboard, mouse
from datetime import datetime

print("Tracking started... Press CTRL+C to stop")

log_data = []

def on_press(key):
    log_data.append({
        "event": "key_press",
        "time": datetime.now()
    })

def on_move(x, y):
    log_data.append({
        "event": "mouse_move",
        "time": datetime.now()
    })

def save_to_csv():
    df = pd.DataFrame(log_data)
    df.to_csv("../data/activity_log.csv", index=False)
    print("Data saved!")

keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_move=on_move)

keyboard_listener.start()
mouse_listener.start()

try:
    while True:
        time.sleep(10)
        save_to_csv()
except KeyboardInterrupt:
    print("Stopped tracking")
    save_to_csv()