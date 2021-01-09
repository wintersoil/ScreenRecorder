import pyautogui
import pynput
from pynput import mouse
from pynput import keyboard
from PIL import Image
import datetime
import pygame

data_file = input("Enter the data storage file path and name: ")
photo_storage_folder = input("Enter folder where to store screenshots: ")

file = open(data_file, 'w')
current_time = datetime.datetime.now().timestamp()
counter = 0
mouse2 = pynput.mouse.Controller()
coordinates = mouse2.position
current_time_2 = datetime.datetime.now().timestamp()
timeDiff = current_time_2 - current_time
file.write("mm," + str(timeDiff) + "," + str(coordinates[0]) + "," + str(coordinates[1]) + "\n")

myScreenshot = pyautogui.screenshot()
myScreenshot.save(r''+ photo_storage_folder + '/Screenshot-'+ str(counter) +'.png')
current_time_2 = datetime.datetime.now().timestamp()
timeDiff = current_time_2 - current_time
file.write("mc," + str(timeDiff) + "," + photo_storage_folder + '/Screenshot-'+ str(counter) +'.png' + "\n")
im = Image.open(photo_storage_folder + '/Screenshot-'+ str(counter) +'.png')
im = im.resize((900, 600), Image.ANTIALIAS)
im.save(photo_storage_folder + '/Screenshot-'+ str(counter) +'.png', dpi=(100,100))
counter = counter + 1
print("Welcome to Video Transcripter")
addingNote = False
comment = ""
leftClick = pynput.mouse.Controller()
coordinatesLeft = leftClick.position




def on_press(key):
    global comment
    global addingNote
    global coordinatesLeft
    current_time_2 = datetime.datetime.now().timestamp()
    timeDiff = current_time_2 - current_time
    if key == pynput.keyboard.Key.ctrl:
        coordinatesLeft = pynput.mouse.Controller().position
    if key == pynput.keyboard.Key.shift_r and not addingNote:
        addingNote = not addingNote
    elif addingNote and not key == pynput.keyboard.Key.shift_r:
        if key == pynput.keyboard.Key.shift:
            comment = comment + " "
        else:
            comment = comment + str(key)
    elif addingNote and key == pynput.keyboard.Key.shift_r:
        current_time_2 = datetime.datetime.now().timestamp()
        timeDiff = current_time_2 - current_time
        mouse2 = pynput.mouse.Controller()
        coordinates = mouse2.position
        file.write("kc," + str(timeDiff) + "," + comment + "," + str(coordinatesLeft[0]) + "," + str(coordinatesLeft[1]) + "\n")
        comment = ""
        addingNote = not addingNote
    if key == pynput.keyboard.Key.esc:
        file.close()
        listener1.stop()
        listener2.stop()
        return False

        
        

def on_move(x, y):
    current_time_2 = datetime.datetime.now().timestamp()
    timeDiff = current_time_2 - current_time
    file.write("mm," + str(timeDiff) + "," + str(x) + "," + str(y) + "\n")

def on_click(x, y, button, pressed):
    global counter
    global coordinatesLeft
    if not pressed:
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(r'' + photo_storage_folder + '/Screenshot-'+ str(counter) +'.png')
        current_time_2 = datetime.datetime.now().timestamp()
        timeDiff = current_time_2 - current_time
        file.write("mc," + str(timeDiff) + "," + photo_storage_folder + '/Screenshot-'+ str(counter) +'.png,' + str(x) + "," + str(y) + "\n")
        im = Image.open(photo_storage_folder + '/Screenshot-'+ str(counter) +'.png')
        im = im.resize((900, 600), Image.ANTIALIAS)
        im.save(photo_storage_folder + '/Screenshot-'+ str(counter) +'.png', dpi=(100,100))
        counter = counter + 1
    elif pressed:
        current_time_2 = datetime.datetime.now().timestamp()
        timeDiff = current_time_2 - current_time
        file.write("mm," + str(timeDiff) + "," + str(x) + "," + str(y) + "\n")

def on_scroll(x, y, dx, dy):
    file.write(str(dx))
    print(dx, dy)
    file.close()
    listener1.stop()
    listener2.stop()
    return False

listener1 = keyboard.Listener(on_press=on_press)
listener1.start()


listener2 = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
listener2.start()

