# ChatBot---Jerry-v5.0
# Virtual AI friend

The Virtual AI Assistant project is a Python-based application that utilizes natural language processing (NLP) and machine learning (ML) techniques to create an interactive chatbot capable of engaging in conversations with users. It incorporates modern AI models and tools to deliver intelligent responses and perform tasks based on user input. It uses [Blenderbot-400M-distill](https://huggingface.co/facebook/blenderbot-400M-distill). The chatbot can be used totally offline.

## Features

- **Natural Language Understanding**: Utilizes Transformers-based models to comprehend and generate human-like responses.
- **Predefined Responses**: Includes a set of predefined responses for common queries and commands.
- **Text-to-Speech (TTS) Capability**: Converts text responses to speech using the gTTS library for enhanced user interaction.
- **Graphical User Interface (GUI)**: Implements a simple GUI using Tkinter to provide a user-friendly interface for interaction.
- **Multithreaded Response Generation**: Uses threading to ensure responsiveness and efficiency during response generation.
- **Local Model Execution**: Enables offline functionality by loading AI models and data locally without requiring internet connectivity.
- **GIF Animation Handling**: Integrates GIFHandler module to display animated responses or status indicators.

## Technologies Used

- **Python**: Core programming language used for development.
- **PyTorch**: Framework for implementing machine learning models and computations.
- **Hugging Face Transformers**: Library for state-of-the-art natural language processing models.
- **Google Translate API**: Used for language detection and translation capabilities.
- **gTTS (Google Text-to-Speech)**: Converts text responses into spoken audio.
- **Tkinter**: Python's de-facto standard GUI library for creating graphical user interfaces.

## Getting Started

To get started with the ChatBot:

1. Clone the repository to your local machine.
2. Install the necessary dependencies listed in `requirements.txt` by using:

    ```sh
    pip install -r requirements.txt
    ```

3. Unzip the sequences archive.
4. Download all files from [Blenderbot-400M-distill](https://huggingface.co/facebook/blenderbot-400M-distill).

The project directory should look like below:

```plaintext
Project Folder Name
├── models
│   └── HuggingFaceBotModel400M
│       ├── config.json
│       ├── pytorch_model.bin
│       ├── added_tokens.json
│       ├── flax_model.msgpack
│       ├── generation_config.json
│       ├── tokenizer_config.json
│       ├── tokenizer.json
│       ├── vocab.txt
│       ├── special_tokens_map.json
│       └── tf_model.h5
├── chatbot.py
├── main.py
├── other files...

```
Run `main.py` to launch the application. Start interacting with Jerry through the GUI.

## Contributions

Contributions to the Virtual AI Assistant project are welcome! Feel free to fork the repository, make improvements, and submit pull requests for review. Please let me know if you are using this project. I'm so curious about what can you develop with it. :)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
