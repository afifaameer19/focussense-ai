import time
import pandas as pd
from pynput import keyboard, mouse
from datetime import datetime
import os
from threading import Lock
from collections import deque
 
lock = Lock()
print("Tracking started... Press CTRL+C to stop")
 
log_data = []
last_move_time = {}  # Debounce mouse movements
 
# Debounce mouse moves to avoid spam (only log if 100ms+ since last move)
def on_move(x, y):
    global last_move_time
    current_time = time.time()
    
    if current_time - last_move_time.get('move', 0) > 0.1:  # 100ms threshold
        with lock:
            log_data.append({
                "event": "mouse_move",
                "time": datetime.now(),
                "x": x,
                "y": y
            })
        last_move_time['move'] = current_time
 
# Track mouse clicks
def on_click(x, y, button, pressed):
    if pressed:  # Only log on press, not release
        with lock:
            log_data.append({
                "event": f"mouse_{button.name}",
                "time": datetime.now(),
                "x": x,
                "y": y
            })
 
def on_press(key):
    try:
        # Log printable characters, ignore modifiers
        if hasattr(key, 'char') and key.char:
            with lock:
                log_data.append({
                    "event": "key_press",
                    "time": datetime.now(),
                    "key": key.char
                })
    except:
        pass
 
def on_release(key):
    # Optional: Track key releases for detecting held keys
    pass
 
def save_to_csv():
    global log_data
 
    with lock:
        if not log_data:
            return
 
        df = pd.DataFrame(log_data.copy())
        log_data = []
 
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
 
    file_exists = os.path.exists("data/activity_log.csv")
 
    # Use temp file to avoid corruption during writes
    temp_file = "data/activity_log.tmp"
    df.to_csv(temp_file, mode='a', header=not file_exists, index=False)
    
    # Atomic rename
    if os.path.exists("data/activity_log.csv"):
        os.replace(temp_file, "data/activity_log.csv")
    else:
        os.rename(temp_file, "data/activity_log.csv")
 
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Data saved! ({len(df)} events)")
 
# Set up listeners
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
 
keyboard_listener.start()
mouse_listener.start()
 
try:
    while True:
        time.sleep(10)
        save_to_csv()
except KeyboardInterrupt:
    print("\nStopping tracking...")
    save_to_csv()
    keyboard_listener.stop()
    mouse_listener.stop()
 