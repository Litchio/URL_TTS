# -*- coding: utf-8 -*-
import pyttsx3
import urllib
import sys
import PySimpleGUI as sg
import pygame
import time
from bs4 import BeautifulSoup

pygame.mixer.init()
engine = pyttsx3.init()
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def TextOfHtml(file):
    soup = BeautifulSoup(file, 'html.parser')
    all = ""
    for p in soup.find_all('p'):
        all += p.get_text() + "\n\n"
    return all


def ReadText(text):
    outfile = "temp.wav"
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
    engine.save_to_file(text, outfile)
    engine.runAndWait()
    pygame.mixer.music.load(outfile)
    pygame.mixer.music.play()


def FileFromURL(url):
    request = urllib.request.Request(url, None, headers=hdr)
    response = urllib.request.urlopen(request)
    file = response.read()
    return file


def stop():
    pygame.mixer.music.stop()


def pause():
    pygame.mixer.music.pause()


def unpause():
    pygame.mixer.music.unpause()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        layout = [[sg.Text('URL TTS')],
                  [sg.InputText(key='URL')],
                  [sg.Button("Read"), sg.Button("Pause"), sg.Button("Resume"), sg.Button("Close")]]
        window = sg.Window('URL TTS', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == "Read":
                url = values.get("URL")
                ReadText(TextOfHtml(FileFromURL(url)))
            if event == "Pause":
                pause()
            if event == "Resume":
                unpause()
            if event == "Close":
                stop()
                window.close()
        window.close()
    else:
        url = sys.argv[1]
        ReadText(TextOfHtml(FileFromURL(url)))
        time.sleep(3)
        while pygame.mixer.music.get_busy():
            pass
