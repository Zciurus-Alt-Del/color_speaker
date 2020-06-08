import time
import sys
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from tkinter import *
from PIL import Image
from math import sqrt
from gtts import gTTS
from playsound import playsound
import threading
import os

"""
Dieses Skript fragt den Benutzer nach einer RGB-Farbe oder nach einer Bilddatei, aus der im Anschluss der mittlere Farbwert ermittelt wird.
Daraus wird dann aus der unten stehenden Liste die am nächsten liegende Farbe ermittelt und der Name via tts ausgegeben.
"""

root = Tk()
root.withdraw()

color_space = [
    [(0,0,1), "Blau"],
    [(0,1,1), "Türkis"],
    [(1,0,1), "Magenta"],
    [(1,1,1), "Weiß"],
    [(0,0,0), "Schwarz"],
    [(0,1,0), "Grün"],
    [(1,0,0), "Rot"],
    [(1,1,0), "Gelb"],
	# Weitere Farben hinzufügen, aber beachten, dass der RGB-Raum gleichmäßig gefüllt werden sollte
]

def askrgb():
    r,g,b = askcolor()[0]
    r /= 256
    g /= 256
    b /= 256
    return r,g,b

def askfile():
    return filedialog.askopenfilename(initialdir = "Desktop",title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("bmp files","*.bmp"),("all files","*.*")))

def avg_color(image_path):
    img = Image.open(image_path)
    lis = list(img.getdata())

    r, g, b = 0,0,0
    for entry in lis:
        r += entry[0]
        g += entry[1]
        b += entry[2]

    l = len(lis)
    r = (r/l)/255
    g = (g/l)/255
    b = (b/l)/255
    return r,g,b


def vector_len(vec1,vec2):
    return sqrt((vec1[0]-vec2[0])**2+(vec1[1]-vec2[1])**2+(vec1[2]-vec2[2])**2)


def get_nearest_color(r,g,b):
    deviation_list = []
    for entry in color_space:
        deviation_list.append(vector_len(entry[0],(r,g,b)))
    best_fit = deviation_list.index(min(deviation_list))
    return color_space[best_fit][1]


def gettemp():
    temp = str(time.time()).replace(".","") + ".mp3"
    return temp

def tts(text,language="en"):
    text = gTTS(text=text, lang=language)
    temp = gettemp()
    text.save(temp)
    playsound(temp)
    os.system(f"del {sys.path[0]}\\{temp}")


def dotts():
    tts(best_color, language="de")


while True:
    try:
        r,g,b = askrgb()
    except TypeError:
        r,g,b = avg_color(askfile())

    print(r,g,b)
    best_color = get_nearest_color(r,g,b)
    print(best_color)
    th = threading.Thread(target=dotts)
    th.start()
