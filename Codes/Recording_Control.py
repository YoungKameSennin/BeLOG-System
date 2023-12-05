# Recording Control
# version 1.0
# Data: Nov 12, 2023

import pyrealsense2 as rs
import numpy as np
import cv2
import time
import os
import pyaudio
import wave
import json
from moviepy.editor import VideoFileClip, AudioFileClip
import keyboard
import time
import sys

cv2.namedWindow("Preview")
cv2.moveWindow("Preview", 620, 0)
cv2.resizeWindow('Preview', 640, 720)

audio_chunk_size = 1450
audio_format = pyaudio.paInt16
audio_channels = 1
audio_sample_rate = 44100
audio_device_index = 0

p = pyaudio.PyAudio()
audio_stream = p.open(format=audio_format,
                      channels=audio_channels,
                      rate=audio_sample_rate,
                      input=True,
                      frames_per_buffer=audio_chunk_size,
                      input_device_index=audio_device_index)


def time_converter(time):
    hours = int(time // 3600)
    minutes = int((time % 3600) // 60)
    seconds = int(time % 60)
    milliseconds = int((time - int(time)) * 1000)
    formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    return formatted_duration

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

recordings_folder = "C:/Data/Recordings"
projects_folder = "C:/Data/Projects"
logger_path = "C:/Data/Log.txt"
    
color_path = ''
depth_path = ''
colorwriter = None
depthwriter = None
start_time = 0

b1_start, b1_stop, b2_start, b2_stop, b3_start, b3_stop, b4_start, b4_stop = (-1 for i in range(8))
b1, b2, b3, b4 = (0 for i in range(4))

pipeline.start(config)

recording = False

audio_frames = []

log_time = time.strftime("%T-%m/%d/%Y") + ": "

subject = 0
if len(sys.argv) > 1:
        subject = sys.argv[1]

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        if recording:
            if colorwriter is None or depthwriter is None:
                current_time = time.strftime("%Y-%m-%d%a%H-%M-%S")
                current_time_prj = time.strftime("%Y-%m-%d%a%T")
                current_time_prj = current_time_prj[:11] + current_time_prj[13:]

                color_path = os.path.join(recordings_folder, f'{current_time}_rgb.avi')
                depth_path = os.path.join(recordings_folder, f'{current_time}_depth.avi')
                audio_path = os.path.join(recordings_folder, f'{current_time}_audio.wav')
                
                colorwriter = cv2.VideoWriter(color_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (1280, 720), 1)
                depthwriter = cv2.VideoWriter(depth_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (1280, 720), 1)
                start_time = time.time()  # Capture start time
            # Capture audio frames
            audio_data = audio_stream.read(audio_chunk_size)
            audio_frames.append(audio_data)
            
            colorwriter.write(color_image)
            depthwriter.write(depth_colormap)
        
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        combined_image = np.vstack((color_image, depth_colormap))

        # Resize the combined image to fit the window size
        resized_combined_image = cv2.resize(combined_image, (640, 720))

        # Display the combined and resized image in the "Preview" window
        cv2.imshow('Preview', resized_combined_image)
        
        key = cv2.waitKey(1)
        

        if not recording:
            recording = True
            events_list = []
            log_time = time.strftime("%T-%m/%d/%Y") + ": "
            print(log_time + "Recording started. Current subject: Subject" + str(subject))
            with open(logger_path, 'a') as file:
                print(log_time + "Recording started. Current subject: Subject" + str(subject), file=file)
        
        if keyboard.is_pressed('ctrl+alt+r'):
            recording = False
            if start_time:
                end_time = time.time()
                duration = end_time - start_time
                rounded_duration = round(duration, 1)
                log_time = time.strftime("%T-%m/%d/%Y") + ": "
                print(log_time + "Recording stopped. Duration:", time_converter(duration))
                print(log_time + "Saving the observation...")
                with open(logger_path, 'a') as file:
                    print(log_time + "Recording stopped. Duration:", time_converter(duration), file=file)
                    print(log_time + "Saving the observation...", file=file)
                rounded_dur =round(duration, 1)
                start_time = 0
                if colorwriter is not None:
                    colorwriter.release()
                    colorwriter = None
                if depthwriter is not None:
                    depthwriter.release()
                    depthwriter = None
                # Save audio as WAV file
                if audio_frames:
                    with wave.open(audio_path, 'wb') as audio_file:
                        audio_file.setnchannels(audio_channels)
                        audio_file.setsampwidth(p.get_sample_size(audio_format))
                        audio_file.setframerate(audio_sample_rate)
                        audio_file.writeframes(b''.join(audio_frames))
                    audio_frames = []

                    # Combine audio and video using moviepy
                    video_clip = VideoFileClip(color_path)
                    audio_clip = AudioFileClip(audio_path)
                    video_with_audio = video_clip.set_audio(audio_clip)
                    combined_path = os.path.join(recordings_folder, f'{current_time}_combined.avi')
                    video_with_audio.write_videofile(combined_path, codec='libx264', logger=None)
                    video_clip.close()
                    audio_clip.close()

                # Save data as BORIS project file
                project_file_name = projects_folder + "/subject" + str(subject) + ".boris"
                events_list_str = json.dumps(events_list)
                target_string = "}, \"behavioral_categories\""
                string_to_insert = f'"{current_time}": {{"file": {{"1": ["C:/Data/Recordings/{current_time}_combined.avi"], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": []}}, "type": "MEDIA", "date": "{current_time_prj}", "description": "", "time offset": 0.0, "events": {events_list_str}, "observation time interval": [0, 0], "independent_variables": {{}}, "visualize_spectrogram": false, "visualize_waveform": false, "media_creation_date_as_offset": false, "media_scan_sampling_duration": 0, "image_display_duration": 1, "close_behaviors_between_videos": false, "media_info": {{"length": {{"C:/Users/Wei/Documents/Recordings/{current_time}_combined.avi": {rounded_duration}}}, "fps": {{"C:/Users/Wei/Documents/Recordings/{current_time}_combined.avi": 30.0}}, "hasVideo": {{"C:/Users/Wei/Documents/Recordings/{current_time}_combined.avi": true}}, "hasAudio": {{"C:/Users/Wei/Documents/Recordings/{current_time}_combined.avi": true}}, "offset": {{"1": 0.0}}}}}}'

                with open(project_file_name, 'r') as file:
                    content = file.read()
                index = content.find(target_string)
                if content[index - 1] == '}':
                    string_to_insert = ', ' + string_to_insert
                # Check if the target string was found
                if index != -1:
                    # Insert the desired string just before the target string
                    modified_content = content[:index] + string_to_insert + content[index:]
                    index = content.find(target_string)
                    # Open the file in write mode and write the modified content back to the file
                    with open(project_file_name, 'w') as file:
                        file.write(modified_content)
                        log_time = time.strftime("%T-%m/%d/%Y") + ": "
                        print(log_time + "Observation saved successfully.\n")
                        with open(logger_path, 'a') as file:
                            print(log_time + "Observation saved successfully.\n", file=file)
                            
            break
                    

        if recording:
            if keyboard.is_pressed('ctrl+alt+a'):
                time.sleep(0.15)
                if not b1:
                    b1_start = time.time() - start_time
                    event = [round(b1_start, 1), "name1", "code1","", "", "NA"]
                    events_list.append(event)
                    log_time = time.strftime("%T-%m/%d/%Y") + ": "
                    print(log_time + "Behavior1 starts at:", time_converter(b1_start))
                    with open(logger_path, 'a') as file:
                        print(log_time + "Behavior1 starts at:", time_converter(b1_start), file=file)
                    b1 = 1
                else:
                    b1_stop = time.time() - start_time
                    event = [round(b1_stop, 1), "name1", "code1","", "", "NA"]
                    events_list.append(event)
                    log_time = time.strftime("%T-%m/%d/%Y") + ": "
                    print(log_time + "Behavior1 ends at:  ", time_converter(b1_stop))
                    with open(logger_path, 'a') as file:
                        print(log_time + "Behavior1 ends at:  ", time_converter(b1_stop), file=file)
                    b1 = 0
            elif keyboard.is_pressed('ctrl+alt+b'):
                time.sleep(0.15)
                if not b2:
                    b2_start = time.time() - start_time
                    event = [round(b2_start, 1), "name1", "code2","", "", "NA"]
                    events_list.append(event)
                    log_time = time.strftime("%T-%m/%d/%Y") + ": "
                    print(log_time + "Behavior2 starts at:", time_converter(b2_start))
                    with open(logger_path, 'a') as file:
                        print(log_time + "Behavior2 starts at:", time_converter(b2_start), file=file)
                    b2 = 1
                else:
                    b2_stop = time.time() - start_time
                    event = [round(b2_stop, 1), "name1", "code2","", "", "NA"]
                    events_list.append(event)
                    log_time = time.strftime("%T-%m/%d/%Y") + ": "
                    print(log_time + "Behavior2 ends at:  ", time_converter(b2_stop))
                    with open(logger_path, 'a') as file:
                        print(log_time + "Behavior2 ends at:  ", time_converter(b2_stop), file=file)
                    b2 = 0
            elif keyboard.is_pressed('ctrl+alt+c'):
                time.sleep(0.15)
                if not b3:
                    b3_start = time.time() - start_time
                    event = [round(b3_start, 1), "name1", "code3","", "", "NA"]
                    events_list.append(event)
                    log_time = time.strftime("%T-%m/%d/%Y") + ": "
                    print(log_time + "Behavior3 starts at:", time_converter(b3_start))
                    with open(logger_path, 'a') as file:
                        print(log_time + "Behavior3 starts at:", time_converter(b3_start), file=file)
                    b3 = 1
                else:
                    b3_stop = time.time() - start_time
                    event = [round(b3_stop, 1), "name1", "code3","", "", "NA"]
                    events_list.append(event)
                    log_time = time.strftime("%T-%m/%d/%Y") + ": "
                    print(log_time + "Behavior3 ends at:  ", time_converter(b3_stop))
                    with open(logger_path, 'a') as file:
                        print(log_time + "Behavior3 ends at:  ", time_converter(b3_stop), file=file)
                    b3 = 0
            elif keyboard.is_pressed('ctrl+alt+d'):
                time.sleep(0.15)
                if not b4:
                    b4_start = time.time() - start_time
                    event = [round(b4_start, 1), "name1", "code4","", "", "NA"]
                    events_list.append(event)
                    log_time = time.strftime("%T-%m/%d/%Y") + ": "
                    print(log_time + "Behavior4 starts at:", time_converter(b4_start))
                    with open(logger_path, 'a') as file:
                        print(log_time + "Behavior4 starts at:", time_converter(b4_start), file=file)
                    b4 = 1
                else:
                    b4_stop = time.time() - start_time
                    event = [round(b4_stop, 1), "name1", "code4","", "", "NA"]
                    events_list.append(event)
                    log_time = time.strftime("%T-%m/%d/%Y") + ": "
                    print(log_time + "Behavior4 ends at:  ", time_converter(b4_stop))
                    with open(logger_path, 'a') as file:
                        print(log_time + "Behavior4 ends at:  ", time_converter(b4_stop), file=file)
                    b4 = 0
            
finally:
    if colorwriter is not None:
        colorwriter.release()
    if depthwriter is not None:
        depthwriter.release()
    audio_stream.stop_stream()
    audio_stream.close()
    p.terminate()
    pipeline.stop()
    cv2.destroyAllWindows()

    log_time = time.strftime("%T-%m/%d/%Y") + ": "
    print(log_time + "Ready")
    with open(logger_path, 'a') as file:
        print(log_time + "Ready", file=file)