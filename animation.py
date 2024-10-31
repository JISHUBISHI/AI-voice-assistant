import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from threading import Thread
import spacy
import time
import cv2  # For video handling

# Assuming the 'messages' and 'speak' methods are defined in their respective modules.
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load spacy language model
nlp = spacy.load("en_core_web_sm")

# UI Colors and Fonts
BG_COLOR = "#000000"  # Black background
BUTTON_COLOR = "#1f8ef1"  # Bright blue for buttons
BUTTON_HOVER_COLOR = "#0e68a8"  # Darker blue for hover effect
TEXT_COLOR = "#FFFFFF"  # White text
BUTTON_FONT = ("Helvetica Neue", 16, "bold")  # Modern bold font for buttons
HEADING_FONT = ("Helvetica Neue", 28, "bold")  # Bold header font
INSTRUCTION_FONT = ("Helvetica Neue", 14)
TAGLINE_FONT = ("Helvetica Neue", 12, "italic")  # Font for tagline

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set default voice

stop_flag = False

def listen_commands():
    """Listen for commands from the user."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError as e:
            speak("There was an error with the voice recognition service.")
            return None

def process_commands(command):
    """Process user commands."""
    if command:
        if "hello" in command.lower():
            speak("Hello! How can I assist you today?")
        elif "time" in command.lower():
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}.")
        elif "stop" in command.lower():
            stop_voice_assistant()
        else:
            messages(command)

def start_melody():
    """Start listening for commands after detecting the wake word."""
    speak("Melody Assistant is ready. Please say 'Melody', 'Hey Melody', or 'Ok Melody' to start.")
    while not stop_flag:
        command = listen_commands()
        if command and command.lower() in ["melody", "hey melody", "ok melody"]:
            speak("How may I assist you?")
            process_commands(listen_commands())

def stop_voice_assistant():
    """Stop the voice assistant."""
    global stop_flag
    speak("Stopping the Voice Assistant.")
    stop_flag = True

def start_voice_assistant():
    """Start the voice assistant."""
    global stop_flag
    stop_flag = False
    Thread(target=start_melody, daemon=True).start()

def play_video(label, video_path, width, height):
    """Play a video in a tkinter label."""
    cap = cv2.VideoCapture(video_path)
    
    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (width, height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            label.config(image=img)
            label.image = img  # Keep a reference to avoid garbage collection
            label.after(33, update_frame)  # Adjust frame rate to ~30fps (1000ms / 30 = 33)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
            update_frame()
    
    update_frame()

def fade_in(widget):
    """Create a fade-in effect for a widget."""
    for i in range(0, 255, 5):  # Increase opacity
        widget.attributes('-alpha', i / 255)  # Set opacity
        widget.update()
        time.sleep(0.01)

def setup_ui(root):
    """Setup the UI components."""
    # Video Animation Label
    video_label = ttk.Label(root)
    video_label.place(relx=0.5, rely=0.4, anchor="center")  # Position the video above the buttons
    play_video(video_label, "C:/Users/dell/OneDrive/Desktop/1023(1).mp4", 300, 300)  # Update with the correct path

    # Headline label
    heading_label = ttk.Label(root, text="Melody Voice Assistant", font=HEADING_FONT, background=BG_COLOR, foreground=TEXT_COLOR)
    heading_label.place(relx=0.5, rely=0.1, anchor="center") 

    # Tagline label
    tagline_label = ttk.Label(root, text="Your Personal Voice Assistant", font=TAGLINE_FONT, background=BG_COLOR, foreground=TEXT_COLOR)
    tagline_label.place(relx=0.5, rely=0.2, anchor="center")

    # Instruction label
    instruction_label = ttk.Label(root, text="Click the button below to start the Melody Assistant.",
                                   font=INSTRUCTION_FONT, background=BG_COLOR, foreground=TEXT_COLOR)
    instruction_label.place(relx=0.5, rely=0.3, anchor="center")

    # Start button
    start_button = ttk.Button(root, text="Start Melody Assistant", command=start_voice_assistant,
                              style="VoiceAssistant.TButton")
    start_button.place(relx=0.5, rely=0.75, anchor="center") 

    # Stop button
    stop_button = ttk.Button(root, text="Stop Melody Assistant", command=stop_voice_assistant,
                             style="VoiceAssistant.TButton")
    stop_button.place(relx=0.5, rely=0.85, anchor="center") 

    # Settings button
    settings_button = ttk.Button(root, text="Settings", command=open_settings,
                                  style="VoiceAssistant.TButton")
    settings_button.place(relx=0.5, rely=0.95, anchor="center")

    # Button styles
    style = ttk.Style(root)
    style.configure("VoiceAssistant.TButton", font=BUTTON_FONT, background=BUTTON_COLOR, foreground=TEXT_COLOR, borderwidth=1)
    style.map("VoiceAssistant.TButton", background=[("active", BUTTON_HOVER_COLOR)])  # Darker blue when active

def open_settings():
    """Open the settings panel for voice selection."""
    settings_window = tk.Toplevel()
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    settings_window.configure(bg=BG_COLOR)

    # Voice selection
    voice_label = ttk.Label(settings_window, text="Select Voice:", font=INSTRUCTION_FONT, background=BG_COLOR, foreground=TEXT_COLOR)
    voice_label.pack(pady=10)

    voice_combo = ttk.Combobox(settings_window, values=[voice.name for voice in voices], state="readonly")
    voice_combo.pack(pady=10)
    voice_combo.current(0)  # Set default to the first voice

    def apply_voice_selection():
        """Apply selected voice to the TTS engine."""
        selected_voice = voice_combo.get()
        for voice in voices:
            if voice.name == selected_voice:
                engine.setProperty('voice', voice.id)
                speak(f"Voice changed to {selected_voice}.")
                settings_window.destroy()
                break

    apply_button = ttk.Button(settings_window, text="Apply", command=apply_voice_selection)
    apply_button.pack(pady=20)

def main():
    """Main function to run the application."""
    root = tk.Tk()
    root.title("Melody Voice Assistant")
    root.attributes("-fullscreen", True)
    root.configure(bg=BG_COLOR)

    # Fade-in effect for the main window
    fade_in(root)

    # Setup UI
    setup_ui(root)

    root.mainloop()

if __name__ == "__main__":
    main()
