# Melody Voice Assistant

## Description

Melody Voice Assistant is a Streamlit-based application that allows users to interact with a voice assistant using speech recognition and natural language processing. The assistant listens for a wake word ("Melody", "Hey Melody", "Hi Melody", or "Ok Melody") and then processes voice commands to provide responses. The interface features custom CSS styling, animations, and a modern design to enhance user experience.

## Features

- **Voice Command Recognition:**  
  Uses the `speech_recognition` library to capture and transcribe voice commands via a microphone.
  
- **Natural Language Processing:**  
  Integrates SpaCy's `en_core_web_sm` model for processing and understanding commands.
  
- **Custom UI with Streamlit:**  
  - Animated "pulse" effect indicating active listening.
  - Stylish response boxes and button controls.
  - Top-right corner links for About and Documentation.
  
- **Interactive Voice Feedback:**  
  The assistant uses the `speak` function (from an external module) to provide audible feedback.
  
- **Session State Management:**  
  Maintains running state and displays responses using Streamlit's session state.

## Requirements

- Python 3.7+
- [Streamlit](https://streamlit.io/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [SpaCy](https://spacy.io/) and the language model `en_core_web_sm`
- Custom modules:
  - `shared` (for the `speak` function)
  - `processCommand` (for processing commands with a `messages` function)
  
*Note: Ensure that you have a working microphone and an active internet connection for speech recognition (Google Web Speech API).*

## Installation

1. **Clone the Repository**
   git clone https://https://github.com/JISHUBISHI/AI-voice-assistant
   cd melody-voice-assistant

## Install Dependencies
pip install -r requirements.txt
Download the SpaCy Language Model

Download and install the en_core_web_sm model:

## bash
python -m spacy download en_core_web_sm
Ensure Custom Modules are Available

Make sure that the custom modules shared (with a speak function) and processCommand (with a messages function) are present in your project directory.

## How It Works
User Interface & Styling:
The application uses Streamlit to render a web interface with custom CSS for background colors, fonts, animations (pulse effect), and styled buttons.

## Voice Command Listening:
The listen_commands() function uses the speech_recognition library to capture audio from the microphone and convert it to text using the Google Web Speech API.

## Wake Word Detection:
The assistant waits for specific wake words (e.g., "Melody"). Once detected, it prompts the user to provide further instructions.

## Processing Commands:
Upon detecting the wake word, the assistant processes additional voice commands by passing the command text to the messages function (from the processCommand module) and updating the UI with responses.

## Audible Feedback:
The speak function (from the shared module) is used throughout the process to provide audible prompts and feedback to the user.

## Running the Application
After completing the installation and setup, run the application using:

### bash

streamlit run main.py
Replace main.py with the name of your Python script containing the provided code. The application will open in your default web browser.

## Usage
Start the Assistant:
Click the Start Assistant button. The assistant will prompt you to say one of the wake words ("Melody", "Hey Melody", "Hi Melody", or "Ok Melody").

## Speak Your Command:
Once the wake word is detected, follow the audible prompt and speak your command. The command will be processed and the response will be displayed in the response box.

## Stop the Assistant:
Click the Stop Assistant button to terminate the listening loop and stop the assistant.

## Author
Agnik Bishi
Parthib Karak
---Developers Behind Melody Voice Assistant.
