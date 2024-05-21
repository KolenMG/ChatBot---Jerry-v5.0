import tkinter as tk
from tkinter import scrolledtext, ttk
import os
import random
import time
from chatbot import ChatBot  # Assuming ChatBot is implemented in chatbot.py
from gif_handler import GIFHandler  # Assuming GIFHandler is implemented in gif_handler.py

class ChatAppGUI:
    def __init__(self, master):
        self.master = master
        master.title("Jerry v5 - Chatbot by KolenMG")
        master.configure(bg='black')  # Set background to black

        # Placeholder image setup (if needed)
        placeholder_path = os.path.join(os.path.dirname(__file__), 'placeholder.gif')
        self.placeholder_image = tk.PhotoImage(file=placeholder_path)

        self.image_frame = tk.Frame(master, bg='black')
        self.image_frame.grid(row=0, column=0, padx=10, pady=10)

        self.image_label = tk.Label(self.image_frame, image=self.placeholder_image, bg='black')
        self.image_label.pack(padx=10, pady=10)

        # GIF handler and ChatBot initialization
        self.gif_handler = GIFHandler(self.image_label)
        self.chatbot = ChatBot(self.update_chat_history, self.gif_handler)
        self.gif_handler.load_idle_sequence()

        # Introductory text above chat history
        self.intro_label = tk.Label(master, text="Try saying 'Hello'", bg='black', fg='#cccccc', font=('Arial', 12, 'italic'))
        self.intro_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # Chat history area with darker background and matched scroll bar color
        self.chat_history = scrolledtext.ScrolledText(master, width=60, height=20, bg='#222222', fg='white',
                                                      font=('Arial', 11), wrap=tk.WORD, relief=tk.FLAT, bd=0)
        self.chat_history.grid(row=2, column=0, padx=10, pady=(20, 10), sticky='w')
        self.chat_history['yscrollcommand'] = lambda *args: self.chat_history.yview_moveto(1)  # Match scroll bar color

        # User input area with darker background
        self.user_input = tk.Entry(master, width=60, bg='#222222', fg='white', font=('Arial', 11), relief=tk.FLAT, bd=0)
        self.user_input.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Send button with style
        self.send_button = tk.Button(master, text="Send", command=self.send_message, bg='#0084ff', fg='white',
                                     font=('Arial', 11, 'bold'), relief=tk.FLAT, bd=0, cursor='hand2')
        self.send_button.grid(row=3, column=0, padx=(470, 10), pady=10, sticky='e')

        # TTS toggle button with style
        self.tts_active = False
        self.style = ttk.Style()
        self.style.configure('TButton', background='#0084ff', foreground='#e0e0e0', font=('Arial', 11, 'bold'))

        self.tts_toggle_button = tk.Button(master, text="Activate TTS", command=self.toggle_tts, bg='#0084ff', fg='white',
                                           font=('Arial', 11, 'bold'), relief=tk.FLAT, bd=0, cursor='hand2')
        self.tts_toggle_button.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        # Initialize tips list
        self.tips = [
            "Say: 'Tell me something interesting.'",
            "Ask: 'What's the weather like?'",
            "Try: 'Tell me a joke.'",
            # Add more tips as desired
        ]

        def show_next_tip():
            tip = random.choice(self.tips)
            self.update_chat_history(f"\n>> {tip}", tag="tip_tag")
            self.master.after(120000, show_next_tip)  # Schedule next tip after 120 seconds

        # Start showing tips
        show_next_tip()

    def send_message(self):
        user_input = self.user_input.get()
        self.user_input.delete(0, 'end')
        self.update_chat_history(f"\nYou: {user_input}", tag="user_tag")
        self.gif_handler.load_search_sequence()  # Trigger search sequence
        self.chatbot.generate_response(user_input)

    def update_chat_history(self, text, tag):
        cleaned_text = self.clean_text(text)
        if tag == "generated_tag":
            # Only show the generated response without user input
            self.chat_history.configure(state='normal')
            self.chat_history.insert(tk.END, f"{cleaned_text}\n", tag)
            self.chat_history.configure(state='disabled')
            self.chat_history.yview(tk.END)
            self.gif_handler.load_idle_sequence()
        else:
            # For other tags like "user_tag" or "tip_tag", show full text
            self.chat_history.configure(state='normal')
            self.chat_history.insert(tk.END, f"{cleaned_text}\n", tag)
            self.chat_history.configure(state='disabled')
            self.chat_history.yview(tk.END)

    def clean_text(self, text):
        cleaned_text = text.replace("You: ", "")
        return cleaned_text

    def toggle_tts(self):
        if self.tts_active:
            self.chatbot.deactivate_tts()
            self.tts_active = False
            self.tts_toggle_button.configure(text="Activate TTS", bg='#0084ff', fg='white')
        else:
            self.chatbot.activate_tts()
            self.tts_active = True
            self.tts_toggle_button.configure(text="Deactivate TTS", bg='#ff4444', fg='white')

    def update_tts_button(self):
        if self.tts_active:
            self.tts_toggle_button.configure(text="Deactivate TTS", bg='#ff4444', fg='white')
        else:
            self.tts_toggle_button.configure(text="Activate TTS", bg='#0084ff', fg='white')

def main():
    root = tk.Tk()
    app = ChatAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
