# gif_handler.py

import os
from PIL import Image, ImageTk

class GIFHandler:
    def __init__(self, image_label):
        self.image_label = image_label
        self.current_sequence = None
        self.current_frame = 0
        self.gif_frames = []
        self.gif_index = 0

    def load_idle_sequence(self):
        self.current_sequence = 'idle'
        self.load_sequence('idle')

    def load_search_sequence(self):
        self.current_sequence = 'search'
        self.load_sequence('search')

    def load_send_sequence(self):
        self.current_sequence = 'send'
        self.load_sequence('send')

    def load_sequence(self, sequence_name):
        gif_path = os.path.join(os.path.dirname(__file__), 'sequences', sequence_name, f'{sequence_name}.gif')
        self.gif_image = Image.open(gif_path)
        self.gif_frames = []
        self.gif_index = 0

        try:
            while True:
                self.gif_frames.append(ImageTk.PhotoImage(self.gif_image.copy()))
                self.gif_index += 1
                self.gif_image.seek(self.gif_index)
        except EOFError:
            pass

        self.gif_index = 0
        if self.gif_frames:
            self.image_label.config(image=self.gif_frames[0])
            self.animate_next_frame()

    def animate_next_frame(self):
        if self.gif_frames:
            self.image_label.config(image=self.gif_frames[self.gif_index % len(self.gif_frames)])
            self.gif_index += 1

            if self.current_sequence == 'idle':
                self.image_label.after(80, self.animate_next_frame)
            elif self.current_sequence == 'search':
                self.image_label.after(50, self.animate_next_frame)
            elif self.current_sequence == 'send':
                self.image_label.after(50, self.animate_next_frame)
