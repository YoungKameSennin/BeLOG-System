# BeLog Server for Linux
# version 1.0
# Data: Feb 29, 2024

from pynput import keyboard
import subprocess
import time

def print_log(log_message):
    log_time = time.strftime("%T-%m/%d/%Y") + ": "
    print(log_time + log_message)
    with open(logger_path, 'a') as file:
        print(log_time + log_message, file=file)
        file.close()

def read_name(subject):
    project_file_name = projects_folder + \
                    "/subject" + str(subject) + ".boris"

    with open(project_file_name, 'r') as file:
        content = file.read()
        # get the start index of the subject's name and its length
        name_start = content.find("\"name\": \"") + 9
        name_end = content[name_start:].find("\",")
        file.close()
    
    # save the subject's name
    subject_name = content[name_start: name_start + name_end]
    
    return subject_name

def switch_sub0():
    global subject
    global subject_name
    global rec
    subject = 0
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def switch_sub1():
    global subject
    global subject_name
    global rec
    subject = 1
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def switch_sub2():
    global subject
    global subject_name
    global rec
    subject = 2
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def switch_sub3():
    global subject
    global subject_name
    global rec
    subject = 3
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def switch_sub4():
    global subject
    global subject_name
    global rec
    subject = 4
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def switch_sub5():
    global subject
    global subject_name
    global rec
    subject = 5
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def switch_sub6():
    global subject
    global subject_name
    global rec
    subject = 6
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def switch_sub7():
    global subject
    global subject_name
    global rec
    subject = 7
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def switch_sub8():
    global subject
    global subject_name
    global rec
    subject = 8
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def switch_sub9():
    global subject
    global subject_name
    global rec
    subject = 9
    subject_name = read_name(subject)
    print_log(f"Changed to Subject{subject}: {subject_name}")

def record():
    global subject
    global subject_name
    global rec

    #python_script = "/Users/ws/Desktop/BeLog/BeLOG-System/Codes/Recording_Control_Regular.py"
    python_script = "/media/psf/Home/Desktop/BeLog/BeLOG-System/Codes/Recording_Control_Linux.py"
    arguments = [str(subject), subject_name]
    command = ["python3", python_script] + arguments
    recording = subprocess.Popen(command)
    recording.wait()

# Ubuntu
#projects_folder = "/media/psf/Home/Desktop/BeLog/BeLOG-System/Projects"
#logger_path = "/media/psf/Home/Desktop/BeLog/BeLOG-System/Log.txt"

# MAC
logger_path = "/Users/ws/Desktop/BeLog/BeLOG-System/Log.txt"
projects_folder = "/Users/ws/Desktop/BeLog/BeLOG-System/Projects"
application_path = 'C:/BeLog/dist/Recording_Control.exe'
next_key = None
subject = 0
subject_name = read_name(subject)
rec = 0

h = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+0': switch_sub0,
        '<ctrl>+<alt>+1': switch_sub1,
        '<ctrl>+<alt>+2': switch_sub2,
        '<ctrl>+<alt>+3': switch_sub3,
        '<ctrl>+<alt>+4': switch_sub4,
        '<ctrl>+<alt>+5': switch_sub5,
        '<ctrl>+<alt>+6': switch_sub6,
        '<ctrl>+<alt>+7': switch_sub7,
        '<ctrl>+<alt>+8': switch_sub8,
        '<ctrl>+<alt>+9': switch_sub9,
        '<ctrl>+<alt>+r': record})
h.start()

print_log("Ready")

while True:
    pass





