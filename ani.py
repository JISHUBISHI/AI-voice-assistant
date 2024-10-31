import tkinter as tk
from tkinter import ttk

class VoiceAssistantUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Safari-like Voice Assistant")
        self.geometry("400x500")
        self.configure(bg="#F5F5F5")

        # Create the frame with rounded corners (Safari-like style)
        self.main_frame = tk.Frame(self, bg="white", bd=2, relief="solid")
        self.main_frame.place(relx=0.5, rely=0.4, anchor="center", width=300, height=400)

        # Title label with tagline
        self.title_label = tk.Label(self.main_frame, text="Voice Assistant", font=("Arial", 20), bg="white")
        self.title_label.pack(pady=20)

        self.tagline_label = tk.Label(self.main_frame, text="Your personalized AI companion", font=("Arial", 10), bg="white", fg="grey")
        self.tagline_label.pack()

        # Create microphone button
        self.mic_button = tk.Button(self.main_frame, text="🎤", font=("Arial", 30), bg="white", fg="black", bd=0, command=self.animate_mic)
        self.mic_button.pack(pady=50)

        # Button hover effects (Safari-like UX)
        self.mic_button.bind("<Enter>", self.on_hover)
        self.mic_button.bind("<Leave>", self.off_hover)

        self.is_listening = False

    def on_hover(self, event):
        self.mic_button.config(bg="#E0E0E0")  # Button hover effect

    def off_hover(self, event):
        self.mic_button.config(bg="white")

    def animate_mic(self):
        # Start/Stop animation for listening
        self.is_listening = not self.is_listening
        if self.is_listening:
            self.pulsate_mic()
        else:
            self.mic_button.config(font=("Arial", 30))  # Reset size when stopped

    def pulsate_mic(self):
        if self.is_listening:
            current_size = self.mic_button.cget("font")[1]
            new_size = current_size + 1 if current_size < 35 else 30
            self.mic_button.config(font=("Arial", new_size))

            # Call the function recursively to animate
            self.after(100, self.pulsate_mic)

if __name__ == "__main__":
    app = VoiceAssistantUI()
    app.mainloop()
