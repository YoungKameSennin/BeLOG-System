# BeLog
# version 1.0
# Data: Nov 12, 2023
import keyboard
import subprocess
import pyautogui
import time

subject_mapping = {
    'ctrl+alt+0': 0,
    'ctrl+alt+1': 1,
    'ctrl+alt+2': 2,
    'ctrl+alt+3': 3,
    'ctrl+alt+4': 4,
    'ctrl+alt+5': 5,
    'ctrl+alt+6': 6,
    'ctrl+alt+7': 7,
    'ctrl+alt+8': 8,
    'ctrl+alt+9': 9
}
logger_path = "C:/Data/Log.txt"
application_path = 'C:\\BeLog\\dist\\Recording_Control.exe'
rec = 0
subject = 0
log_time = time.strftime("%T-%m/%d/%Y") + ": "
print(log_time + "Ready")
with open(logger_path, 'a') as file:
    print(log_time + "Ready", file=file)
while True:
    if not rec:
        for key_combination, value in subject_mapping.items():
            if keyboard.is_pressed(key_combination):
                time.sleep(0.15)
                subject = value
                log_time = time.strftime("%T-%m/%d/%Y") + ": "
                print(log_time + "Changed to Subject" + str(subject))
                with open(logger_path, 'a') as file:
                    print(log_time + "Changed to Subject" + str(subject), file=file)
    if not rec and keyboard.is_pressed('ctrl+alt+r'):
        subprocess.Popen([application_path, str(subject)])
        rec = 1
        time.sleep(0.15)
    
    if rec and keyboard.is_pressed('ctrl+alt+r'):
        time.sleep(0.15)
        rec = 0