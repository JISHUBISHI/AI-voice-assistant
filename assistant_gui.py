from PIL import Image, ImageTk
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import speech_recognition as sr
import spacy
import time
from shared import speak
from processCommand import messages

nlp = spacy.load("en_core_web_sm")

# Function to recognize and process voice commands
def listen_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_conversation("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            update_conversation(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            update_conversation("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError as e:
            update_conversation(f"Sorry, there was an error with the request: {e}")
            return None

def process_commands():
    while True:
        command = listen_commands() 
        if command:
            messages(command)
        else:
            speak("I didn't understand that command. Please try again.")

def melody_listen_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_conversation("Listening for 'Melody' commands...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            update_conversation(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            update_conversation("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError as e:
            update_conversation(f"Sorry, there was an error with the request: {e}")
            return None

def start_assistant():
    update_conversation("Melody Assistant is ready. Please say 'Melody', 'Hey Melody', 'Hi Melody', or 'Ok Melody' to start listening.")
    while True:  
        new_command = melody_listen_commands() 
        if new_command and new_command.lower() in ["melody", "hey melody", "hi melody", "ok melody"]:
            speak("How may I assist you, sir?")
            update_conversation("How may I assist you, sir?")
            process_commands()

# Function to run assistant in a separate thread
def run_assistant_thread():
    assistant_thread = Thread(target=start_assistant)
    assistant_thread.daemon = True
    assistant_thread.start()

# Update the conversation in the GUI
def update_conversation(message):
    conversation_box.config(state=tk.NORMAL)
    conversation_box.insert(tk.END, message + "\n")
    conversation_box.config(state=tk.DISABLED)
    conversation_box.yview(tk.END)

# GUI setup
root = tk.Tk()
root.title("Melody Voice Assistant")

# Load and set the icon using Pillow for .jpg files
icon_img = Image.open("E:\\onedrive\\OneDrive - INSTITUTE OF ENGINEERING & MANAGEMENT\\Desktop\\voiceAssistant\\melody_assistant.png")
icon = ImageTk.PhotoImage(icon_img)
root.iconphoto(False, icon)

root.geometry("500x400")

# Scrolled text box to show the conversation
conversation_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
conversation_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Button to start the assistant
start_button = tk.Button(root, text="Start Melody Assistant", font=("Arial", 12), bg="lightblue", command=run_assistant_thread)
start_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
