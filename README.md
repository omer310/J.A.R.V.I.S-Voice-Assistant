# J.A.R.V.I.S Voice Assistant

J.A.R.V.I.S (Just A Rather Very Intelligent System) is a voice assistant project that utilizes the Google Cloud Speech-to-Text and Text-to-Speech APIs along with OpenAI's GPT-3 for generating code and any other questions asked based on voice input. The application is built using Python and Tkinter for the graphical user interface.

## Features
- Transcribes voice input using the Google Cloud Speech-to-Text API
- Synthesizes voice responses using the Google Cloud Text-to-Speech API
- Generates a reponse based on your question(ex..Essays, general inforamation...)
- Generates code using OpenAI's GPT-3 engine based on voice input
- Saves the generated code to a file with the appropriate file extension

## Installation

1. Install the required Python packages:

```sh
pip install google-cloud-speech google-cloud-texttospeech python-dotenv openai pyaudio tkinter
```

2. Set up a [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) and enable the Google Cloud Speech-to-Text and Text-to-Speech APIs. Download the JSON key file for your service account and set the path to this file in the `os.environ["GOOGLE_APPLICATION_CREDENTIALS"]` variable in the script.

3. Sign up for an [OpenAI account](https://beta.openai.com/signup) and obtain an API key. Save the key in a `.env` file as `OPENAI_API_KEY`.

## Usage

Run the script:

```sh
python jarvis_voice_assistant.py
```

A graphical interface will appear. Press the "Speak" button and provide a voice input. J.A.R.V.I.S will transcribe the input, process it, and respond with synthesized voice output. If the input is a code generation request, the generated code will be saved to a file with the appropriate extension.

Example request: "Generate Python code to reverse a string"

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update the tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)



