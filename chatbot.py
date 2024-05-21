import os
import torch
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import re
import threading
import socket
from predefined_responses import predefined_responses
from gtts import gTTS
from contextlib import contextmanager

class ChatBot:
    def __init__(self, update_chat_history=None, gif_handler=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.update_chat_history = update_chat_history
        self.gif_handler = gif_handler
        self.chat_history_clean = []  # Initialize clean chat history list
        self.tts_active = False  # Initialize TTS as inactive
        self.load_model()

        # Backup the original getaddrinfo function
        self.original_getaddrinfo = socket.getaddrinfo

    @contextmanager
    def disable_internet(self):
        def guard(*args, **kwargs):
            raise OSError("Internet access is disabled")

        # Backup the original socket.getaddrinfo
        original_getaddrinfo = socket.getaddrinfo
        try:
            # Override the socket.getaddrinfo to disable internet
            socket.getaddrinfo = guard
            yield
        finally:
            # Restore the original socket.getaddrinfo
            socket.getaddrinfo = original_getaddrinfo

    def load_model(self):
        try:
            # Define the path to your local model directory
            model_path = r"A:\VirtualAIAssistantprojects\v5\models\HuggingFaceBotModel400M"

            # Load tokenizer and model from the local directory
            self.tokenizer = BlenderbotTokenizer.from_pretrained(model_path, local_files_only=True)
            self.model = BlenderbotForConditionalGeneration.from_pretrained(model_path, local_files_only=True).to(self.device)
            print("BlenderBot model loaded successfully from local files.")
        except Exception as e:
            print(f"Error loading model: {e}")

    def generate_response(self, user_input):
        threading.Thread(target=self._generate_response, args=(user_input,)).start()

    def _generate_response(self, user_input):
        try:
            print(f"Generating response for: {user_input}")

            with self.disable_internet():
                predefined_response = self.get_predefined_response(user_input)
                if predefined_response:
                    response = predefined_response
                    tag = "predefined_tag"
                else:
                    inputs = self.tokenizer([user_input], return_tensors='pt').to(self.device)
                    reply_ids = self.model.generate(**inputs)
                    response = self.tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]

                    filtered_response = self.filter_response(response)

                    # Assuming all responses are in English, skip detection and translation
                    response = filtered_response
                    tag = "generated_tag"

            print(f"Generated response: {response}")

            if self.update_chat_history:
                self.update_chat_history(f"\nJerry: {response}\n", tag=tag)
                self.update_clean_chat_history(f"{response}\n")

            if self.tts_active:
                self.speak_response(response)

            if tag == "generated_tag" and self.gif_handler:
                self.gif_handler.load_idle_sequence()
                self.gif_handler.animate_next_frame()

        except Exception as e:
            error_message = f"Error generating response: {e}"
            print(error_message)

    def speak_response(self, response):
        try:
            cleaned_response = re.sub(r"(User:|GPT-\d+:)", "", response)
            tts = gTTS(text=cleaned_response, lang='en')
            audio_file = os.path.join(os.path.dirname(__file__), 'generated_response.mp3')
            tts.save(audio_file)
            os.system(f"start {audio_file}")
        except Exception as e:
            print(f"Error speaking response: {e}")

    def get_predefined_response(self, user_input):
        cleaned_input = user_input.lower().strip()
        if cleaned_input in predefined_responses:
            return predefined_responses[cleaned_input]
        else:
            return None

    def filter_response(self, response):
        response = self.clean_response(response)
        sentences = re.split(r"[.!?]", response)
        filtered_sentences = [sentence.strip() for sentence in sentences if sentence.strip() and len(sentence.split()) > 3]
        filtered_response = ". ".join(filtered_sentences[:2]) + "."
        return filtered_response.strip()

    def clean_response(self, response):
        response = re.sub(r"\[.*?\]", "", response)
        response = re.sub(r"\n", " ", response)
        response = re.sub(r"\s+", " ", response)
        return response.strip()

    def detect_language(self, text):
        # Remove language detection
        return 'en'

    def translate_response(self, text):
        # Remove translation
        return text

    def exit_bot(self):
        pass  # No session to reset in the new implementation

    def update_clean_chat_history(self, text):
        cleaned_text = re.sub(r"(User:|GPT-\d+:)", "", text)
        self.chat_history_clean.append(cleaned_text)

    def get_clean_chat_history(self):
        return "".join(self.chat_history_clean)

    def activate_tts(self):
        self.tts_active = True
        print("TTS activated")

    def deactivate_tts(self):
        self.tts_active = False
        print("TTS deactivated")
