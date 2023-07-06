import pyttsx3
import speech_recognition as sr
from time import ctime
import webbrowser
import time
import os
import datetime
import subprocess
from pytube import YouTube
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QLabel, QWidget

#Nural Import
import pyaudio
import wave
import numpy as np
import speech_recognition as sr


r = sr.Recognizer()

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def record_audio():
    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()
    
    # starts recording
    stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
    )

    print("start recording...")

    frames = []
    seconds = 10
    for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    print("recording stopped")

    stream.stop_stream()
    stream.close()
    p.terminate()


    wf = wave.open("audio.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def test():
    print("HI")

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            print(ask)
        print("Listening")
        speak("Listening")
        r.pause_threshold = 1
        r.energy_threshold = 1500
        audio = r.listen(source)
        voice_data = ''
        try:
            print("recognizing")
            speak("recognizing")
            voice_data = r.recognize_google(audio)
            print(f"user said: {voice_data}\n ")
        except sr.UnknownValueError:
            print("Sorry ! I did'nt get that.")
            speak("Sorry ! I did'nt get that.")
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            speak("Sorry, my speech service is down.")
        return voice_data


def note(text, file):
    # date = datetime.datetime.now()
    # file_name = str(date).replace(":", "-")+"-note.txt"
    file_name = file
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])
    return file_name


def vscode(code, file):
    # date = datetime.datetime.now()
    # file_name = str(date).replace(":", "-")+"-note.txt"
    file_name = file
    with open(file_name, "w") as f:
        f.write(code)

    subprocess.Popen(
        ["C:\\Users\\user\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", file_name])


def respond(voice_data):

    if "what is your name" in voice_data:
        print("My name is SpeechGenie.")
        speak("My name is SpeechGenie.")

    if "what is the time" in voice_data:
        print(ctime())
        speak(ctime())

    if "search google" in voice_data:
        speak("What do you want to search for ?")
        search = record_audio("What do you want to search for ?")
        url = "https://www.youtube.com/results?search_query=" + search
        webbrowser.get().open(url)
        print("Here it what I found for "+search)
        speak("Here it what I found")

    if "find location" in voice_data:
        location = record_audio("What is the location ?")
        url = "https://google.nl/maps/place/" + location + "/&amp"
        webbrowser.get().open(url)
        speak("Here is the location")
        print("Here is the location of "+location)

    if "open code" in voice_data:
        codePath = "C:\\Users\\user\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)

    if "make a note" in voice_data:
        # option = record_audio("New File or Existing File ?")'

        try:
            speak("What is the filename?")
            file_name = record_audio("What is the filename?") + ".txt"
            r.phrase_threshold = 1
            speak(
                "What would you like me to write down ?")
            note_text = record_audio(
                "What would you like me to write down ?")

            file = note(note_text, file_name)
            print(file)
            print("I've made a note of it.")
            speak("I've made a note of it.")
        except sr.UnknownValueError:
            print("Sorry ! I did'nt get that.")
            speak("Sorry ! I did'nt get that.")
    # if "new file" in voice_data:
    #     # try:
    #     file_name = record_audio("What is the filename?") + ".txt"
    #     note_text = record_audio(
    #         "What would you like me to write down ?")
    #     file = note(note_text, file_name)
    #     print(file)
    #     print("I've made a note of it.")
        # except sr.UnknownValueError:
        #     print("Sorry ! I did'nt get that.")
        # except sr.RequestError:
        #     print("Sorry, my speech service is down.")

    # if "existing file" or "old file" in voice_data:
    #     # try:
    #     file_name = record_audio("What is the filename?") + ".txt"
    #     file = file_name
    #     note_text_again = record_audio(
    #         "What would you like me to write down ?")
    #     with open(file, "a") as f:
    #         f.write(" " + note_text_again)
    #     subprocess.Popen(
    #         ["C:\\Users\\user\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", file])

        # except sr.UnknownValueError:
        #     print("Sorry ! I did'nt get that.")

    if "continue" in voice_data:
        speak("What is the filename?")
        file_name = record_audio("What is the filename?") + ".txt"
        file = file_name

        # Get the list of all files and directories
        # path = "C://Users//user//Desktop//speechGenie"/
        path = ".//"
        dir_list = os.listdir(path)

        print("Files and directories in '", path, "' :")

        # prints all files
        # print(dir_list)

        for i in dir_list:
            if i == file:
                speak("What would you like me to write down ?")
                note_text_again = record_audio(
                    "What would you like me to write down ?")
                with open(file, "a") as f:
                    f.write(" " + note_text_again)
                subprocess.Popen(
                    ["C:\\Users\\user\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", file])

        print("No such File exists.")
        speak("No such File exists.")

    if "write the code" in voice_data:
        speak("What Programming language do you prefer ?")
        lang = record_audio("What Programming language do you prefer ?")
        extension = {
            "python": ".py",
            "C language": ".c",
            "CPP": ".cpp",
            "Java": ".java",
            "PHP": ".php"
        }

        for i in extension:
            if i == lang:
                # file_name = record_audio(
                #     "What is the filename?") + extension[i]
                # code_text = record_audio(
                #     "What would you like me to write down ?")
                # vscode(code_text)
                # print("I've made a note of it.")

                try:
                    speak(
                        "What is the filename?")
                    file_name = record_audio(
                        "What is the filename?") + extension[i]
                    r.phrase_threshold = 1
                    speak("What is the code ?")
                    code_text = record_audio(
                        "What is the code ?")
                    file = vscode(code_text, file_name)
                    # print(file)
                    print("I've made a note of it.")
                except sr.UnknownValueError:
                    print("Sorry ! I did'nt get that.")
                    speak("Sorry ! I did'nt get that.")

    if 'open youtube' in voice_data:
        url = "https://www.youtube.com"
        webbrowser.get().open(url)

    # if "search in youtube" in voice_data:
    #     # searchYoutube = record_audio("What do you want to search for ?")
    #     # urlYt = "https://www.youtube.com/results?search_query" + searchYoutube
    #     # webbrowser.get().open(urlYt)
    #     # print("Here it what I found for "+searchYoutube)

    #     # The search query for the YouTube video
    #     search_query = record_audio("What do you want to search for ?")

    #     # Search for the video and get the first result
    #     video = YouTube().search(search_query)[0]

    #     # Open the video in the default web browser
    #     video.url

    if 'search in youtube' in voice_data:
        # webbrowser.open ( "www.youtube.com" )
        print("what should i search:")
        speak("what should i search:")
        cn = record_audio()
        webbrowser.open(f"https://www.youtube.com/results?search_query={cn}")

    if "exit" in voice_data:
        exit()

class MainWindow(QMainWindow):
    def _init_(self):
        super()._init_()

        # Create the sidebar widget
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        # Create the left button and text field
        left_label = QLabel("Train")
        left_button = QPushButton("Speak to Genie")
        left_label1 = QLabel("Train")
        left_button1 = QPushButton("Record")
        left_text = QTextEdit()
        bt1=QPushButton("SET")
        sidebar_layout.addWidget(left_label)
        sidebar_layout.addWidget(left_button)
        sidebar_layout.addWidget(left_text)
        sidebar_layout.addWidget(left_label1)
        #left_label1.clicked.connect(test)
        sidebar_layout.addWidget(left_button1)
        left_button1.clicked.connect(record_audio)
        left_button.clicked.connect(test)

        # Create the right button and text field
        right_label = QLabel("Voice Assistant")
        right_button = QPushButton("Train")
        right_text = QTextEdit()
        sidebar_layout.addWidget(right_label)
        sidebar_layout.addWidget(right_button)
        sidebar_layout.addWidget(right_text)
        right_button.clicked.connect(test)

        # Create the main layout and add the sidebar to it
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar)

        # Set the main layout as the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Set the window properties
        self.setWindowTitle("Speech Genie")
        self.show()
        
def main():
    time.sleep(1)
    print("How can I help you ?")
    speak("How can I help you ?")

    while 1:
        voice_data = record_audio().lower()
        respond(voice_data)


#Nural Import
app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())