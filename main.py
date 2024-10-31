import streamlit as st
import speech_recognition as sr
from shared import speak
from processCommand import messages
import spacy

# Load the SpaCy language model
nlp = spacy.load("en_core_web_sm")

# Set up page configuration
st.set_page_config(page_title="Melody Voice Assistant", layout="wide")

# CSS for styling the page, including animation and layout
def set_page_style():
    st.markdown("""
        <style>
        /* Style for body */
        body {
            background-color: #f0f4ff; /* Soft background color */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Top-right corner links */
        .top-right {
            position: absolute;
            top: 10px;
            right: 10px;
            display: flex;
            flex-direction: column;
        }
        .top-right a {
            color: #007BFF; /* Link color */
            text-decoration: none;
            margin-bottom: 10px;
            transition: color 0.3s;
        }
        .top-right a:hover {
            color: #0056b3; /* Darker link color on hover */
        }

        /* Central animation for voice listening */
        .pulse-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FF4081, #FF80AB); /* Gradient background */
            position: relative;
            margin: 0 auto;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% {
                transform: scale(0.9);
                opacity: 0.7;
            }
            70% {
                transform: scale(1);
                opacity: 0.3;
            }
            100% {
                transform: scale(0.9);
                opacity: 0.7;
            }
        }

        /* Response box styling */
        .response-box {
            margin: 20px auto;
            padding: 20px;
            max-width: 600px;
            background-color: #ffffff; /* White background for response */
            border-radius: 12px; /* Rounded corners */
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1); /* Softer shadow */
            font-size: 18px;
            color: #333;
            transition: transform 0.3s; /* Animation on hover */
        }
        .response-box:hover {
            transform: scale(1.02); /* Slightly enlarge on hover */
        }

        /* Button styling */
        .start-button, .stop-button {
            background-color: #007BFF; /* Primary button color */
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        .start-button:hover {
            background-color: #0056b3; /* Darker on hover */
        }
        .stop-button {
            background-color: #dc3545; /* Danger color for stop */
        }
        .stop-button:hover {
            background-color: #c82333; /* Darker on hover */
        }
        </style>
    """, unsafe_allow_html=True)

# Function to listen to voice commands
def listen_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for a command...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand what you said."
        except sr.RequestError as e:
            return f"Sorry, there was an error with the request: {e}"

# Process additional commands after "Melody" wake word
def process_commands():
    while st.session_state['is_running']:
        command = listen_commands()
        if command:
            st.session_state['response'] = messages(command)
        else:
            speak("I didn't understand that command. Please try again.")

# Main function for the Streamlit interface
def melody_assistant():
    set_page_style()

    # Top-right corner links
    st.markdown("""
    <div class="top-right">
        <a href="#">About</a>
        <a href="#">Documentation</a>
    </div>
    """, unsafe_allow_html=True)

    # Title and instructions
    st.title("🎶 Melody Voice Assistant")

    # Animation for voice listening in the middle
    st.markdown("""<div class="pulse-circle"></div>""", unsafe_allow_html=True)

    # Display the response in a nicely styled box
    if 'response' in st.session_state and st.session_state['response']:
        st.markdown(f"""
        <div class="response-box">
            {st.session_state['response']}
        </div>
        """, unsafe_allow_html=True)

    # Start/Stop Button Controls
    if 'is_running' not in st.session_state:
        st.session_state['is_running'] = False  # Assistant not running initially
        st.session_state['response'] = ""

    col1, col2 = st.columns(2)  # Create two columns for buttons

    with col1:
        if st.button("Start Assistant", key="start", className="start-button"):
            st.session_state['is_running'] = True
            speak("Melody is ready. Please say 'Melody', 'Hey Melody', 'Hi Melody', or 'Ok Melody' to start.")
            while st.session_state['is_running']:
                new_command = listen_commands()
                if new_command and new_command.lower() in ["melody", "hey melody", "hi melody", "ok melody"]:
                    speak("How may I assist you?")
                    process_commands()
                else:
                    speak("I didn't catch the wake word. Please try again.")
    
    with col2:
        if st.button("Stop Assistant", key="stop", className="stop-button"):
            st.session_state['is_running'] = False
            speak("Assistant stopped.")
            st.write("Assistant has been stopped.")

# Streamlit app entry point
if __name__ == '__main__':
    melody_assistant()
