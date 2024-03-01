# Recording Control for Linux
# version 1.0
# Data: Feb 29, 2024

import numpy as np
import cv2
import time
import os
import pyaudio
from pynput import keyboard
import wave
import json
import time
import sys

def print_log(log_message):
    log_time = time.strftime("%T-%m/%d/%Y") + ": "
    print(log_time + log_message)
    with open(logger_path, 'a') as file:
        print(log_time + log_message, file=file)
        file.close()

def stop_record():
    global subject
    global subject_name
    global rec
    global start_time
    global events_list
    global current_time
    global current_time_prj
    global rounded_duration
    global logger_path
    global rgb_path

    rec = 0

    duration = time.time() - start_time
    rounded_duration = round(duration, 1)
    print_log("Recording stopped. Duration: " + time_converter(duration))
    print_log("Saving the observation...")

    # Save data as BORIS project file
    project_file_name = projects_folder + \
        "/subject" + str(subject) + ".boris"
    events_list_str = json.dumps(events_list)
    target_string = "}, \"behavioral_categories\""
    string_to_insert = f'"{current_time}": {{"file": {{"1": ["{rgb_path}"], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": []}}, "type": "MEDIA", "date": "{current_time_prj}", "description": "", "time offset": 0.0, "events": {events_list_str}, "observation time interval": [0, 0], "independent_variables": {{}}, "visualize_spectrogram": false, "visualize_waveform": false, "media_creation_date_as_offset": false, "media_scan_sampling_duration": 0, "image_display_duration": 1, "close_behaviors_between_videos": false, "media_info": {{"length": {{"{rgb_path}": {rounded_duration}}}, "fps": {{"{rgb_path}": 20.0}}, "hasVideo": {{"{rgb_path}": true}}, "hasAudio": {{"{rgb_path}": true}}, "offset": {{"1": 0.0}}}}}}'

    with open(project_file_name, 'r') as file:
        content = file.read()
    index = content.find(target_string)
    if content[index - 1] == '}':
        string_to_insert = ', ' + string_to_insert
    # Check if the target string was found
    if index != -1:
        # Insert the desired string just before the target string
        modified_content = content[:index] + \
            string_to_insert + content[index:]
        index = content.find(target_string)
        # Open the file in write mode and write the modified content back to the file
        with open(project_file_name, 'w') as file:
            file.write(modified_content)
            log_time = time.strftime("%T-%m/%d/%Y") + ": "
            print_log("Observation saved successfully.\n")

def aggressive_behavior():
    global b1_start
    global b1_stop
    global b1
    global events_list
    global subject_name
    global start_time
    if not b1:
        b1_start = time.time() - start_time
        event = [round(b1_start, 1), subject_name, "A", "", "", "NA"]
        events_list.append(event)
        print_log("Aggressive behavior starts at: " + time_converter(b1_start))
        b1 = 1
    else:
        b1_stop = time.time() - start_time
        event = [round(b1_stop, 1), subject_name, "A", "", "", "NA"]
        events_list.append(event)
        print_log("Aggressive behavior ends at: " +time_converter(b1_stop))
        b1 = 0

def violent_behavior():
    global b2_start
    global b2_stop
    global b2
    global events_list
    global subject_name
    global start_time
    if not b2:
        b2_start = time.time() - start_time
        event = [round(b2_start, 1), subject_name, "V", "", "", "NA"]
        events_list.append(event)
        print_log("Violent behavior starts at: " + time_converter(b2_start))
        b2 = 1
    else:
        b2_stop = time.time() - start_time
        event = [round(b2_stop, 1), subject_name, "V", "", "", "NA"]
        events_list.append(event)
        print_log("Violent behavior ends at: " + time_converter(b2_stop))
        b2 = 0

def self_injurious_behavior():
    global b3_start
    global b3_stop
    global b3
    global events_list
    global subject_name
    global start_time
    if not b3:
        b3_start = time.time() - start_time
        event = [round(b3_start, 1), subject_name, "SI", "", "", "NA"]
        events_list.append(event)
        print_log("Self-injurious behavior starts at: " + time_converter(b3_start))
        b3 = 1
    else:
        b3_stop = time.time() - start_time
        event = [round(b3_stop, 1), subject_name, "SI", "", "", "NA"]
        events_list.append(event)
        print_log("Self-injurious behavior ends at: " + time_converter(b3_stop))
        b3 = 0

def other_behavior():
    global b4_start
    global b4_stop
    global b4
    global events_list
    global subject_name
    global start_time
    if not b4:
        b4_start = time.time() - start_time
        event = [round(b4_start, 1), subject_name, "O", "", "", "NA"]
        events_list.append(event)
        print_log("Other behavior starts at: " + time_converter(b4_start))
        b4 = 1
    else:
        b4_stop = time.time() - start_time
        event = [round(b4_stop, 1), subject_name, "O", "", "", "NA"]
        events_list.append(event)
        print_log("Other behavior ends at: " + time_converter(b4_stop))
        b4 = 0

def time_converter(time):
    hours = int(time // 3600)
    minutes = int((time % 3600) // 60)
    seconds = int(time % 60)
    milliseconds = int((time - int(time)) * 1000)
    formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    return formatted_duration

# Initialize the audio stream
audio_chunk_size = 1024
audio_format = pyaudio.paInt16
audio_channels = 1
audio_sample_rate = 44100
audio_device_index = 1

p = pyaudio.PyAudio()
audio_stream = p.open(format=audio_format,
                      channels=audio_channels,
                      rate=audio_sample_rate,
                      input=True,
                      frames_per_buffer=audio_chunk_size,
                      input_device_index=audio_device_index)


recordings_folder = "/Users/ws/Desktop/BeLog/BeLOG-System/Recordings"
projects_folder = "/Users/ws/Desktop/BeLog/BeLOG-System/Projects"
logger_path = "/Users/ws/Desktop/BeLog/BeLOG-System/Log.txt"
audio_frames = []
b1_start, b1_stop, b2_start, b2_stop, b3_start, b3_stop, b4_start, b4_stop = (
    -1 for i in range(8))
b1, b2, b3, b4 = (0 for i in range(4))
subject = -1
subject_name = "unknown"

if len(sys.argv) > 1:
    subject = sys.argv[1]
    subject_name = sys.argv[2]

current_time = time.strftime("%Y-%m-%d%a%H-%M-%S")
current_time_prj = time.strftime("%Y-%m-%d%a%T")
current_time_prj = current_time_prj[:11] + \
current_time_prj[13:]

rgb_path = os.path.join(recordings_folder, f'{current_time}_rgb.avi')
audio_path = os.path.join(recordings_folder, f'{current_time}_audio.wav')
start_time = time.time()

events_list = []
rec = 1

# Initialize the video capture object with the default camera
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print_log("Error: Could not open camera")
    exit()

# Define the codec and create VideoWriter object 
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
rgb_writer = cv2.VideoWriter(rgb_path, fourcc, 20.0, (1280, 720))

# Create a window to display the camera feed
cv2.namedWindow('Preview')
cv2.moveWindow('Preview', 620, 0)

# Define the hotkeys
h = keyboard.GlobalHotKeys({'<ctrl>+<alt>+r': stop_record, 
                            '<ctrl>+<alt>+a': aggressive_behavior,
                            '<ctrl>+<alt>+b': violent_behavior,
                            '<ctrl>+<alt>+c': self_injurious_behavior,
                            '<ctrl>+<alt>+d': other_behavior})
h.start()

print_log("Recording started. Subject" + str(subject) + ": " + subject_name)

while rec:
    ret, frame = cap.read()
    if not ret:
        print_log("Failed to grab frame")
        break

    # audio_data = audio_stream.read(audio_chunk_size)
    # audio_frames.append(audio_data)

    rgb_writer.write(frame)

    cv2.imshow('Preview', frame)

    key = cv2.waitKey(1)

rgb_writer.release()
cap.release()
p.terminate()
cv2.destroyAllWindows()

print_log("Ready")