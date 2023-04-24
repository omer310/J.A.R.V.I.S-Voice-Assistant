import os
import re
from dotenv import load_dotenv
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech_v1 as texttospeech
import openai


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR_GOOGLE_CREDENTIALS"

speech_client = speech.SpeechClient()

tts_client = texttospeech.TextToSpeechClient()

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def transcribe_audio(audio_data):
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = speech_client.recognize(config=config, audio=audio)
    if response.results:
        return response.results[0].alternatives[0].transcript
    else:
        return None


def synthesize_text(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = tts_client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    return response.audio_content


def is_code_generation_request(text):
    return "generate" in text.lower() and ("code" in text.lower() or "program" in text.lower())


def generate_response(prompt):
    if is_name_request(prompt):
        return "My name is JARVIS.", False

    code_generation = is_code_generation_request(prompt)
    if code_generation:
        prompt = f"Generate code: {prompt}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip(), code_generation


def write_code_to_file(code, filename):
    with open(filename, "w") as f:
        f.write(code)


def is_name_request(text):
    name_related_phrases = ["your name", "who are you",
                            "what's your name", "what is your name"]
    return any(phrase in text.lower() for phrase in name_related_phrases)


def save_code_to_file(language, code):
    file_extension = {
        "python": ".py",
        "c++": ".cpp",
        "java": ".java",
        "javascript": ".js",
        "ruby": ".rb",
        "c#": ".cs",
        "php": ".php",
        "swift": ".swift",
        "go": ".go",
        "kotlin": ".kt",
        "rust": ".rs",
    }

    if language.lower() in file_extension:
        file_name = f"generated_code_{language.lower()}{file_extension[language.lower()]}"
    else:
        file_name = f"generated_code_{language.lower()}.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Code saved to {file_name}")


def on_click():
    def process_audio():
        try:
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000
            RECORD_SECONDS = 5

            p = pyaudio.PyAudio()

            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            print("Recording...")

            frames = []

            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("Done recording.")

            stream.stop_stream()
            stream.close()
            p.terminate()

            audio_data = b''.join(frames)
            text = transcribe_audio(audio_data)
            if text:
                print(f"User: {text}")
                chat_history.configure(state="normal")
                chat_history.insert(tk.END, f"User: {text}\n")
                chat_history.configure(state="disabled")

                response, code_output = generate_response(text)
                print(f"Assistant: {response}")
                chat_history.configure(state="normal")
                chat_history.insert(tk.END, f"Assistant: {response}\n")
                chat_history.configure(state="disabled")
                chat_history.see(tk.END)

                if code_output:
                    save_code_to_file(code_output)

                audio_response = synthesize_text(response)

                p = pyaudio.PyAudio()

                stream = p.open(format=p.get_format_from_width(2),
                                channels=1,
                                rate=24000,
                                output=True)

                stream.write(audio_response)

                stream.stop_stream()
                stream.close()
                p.terminate()

            else:
                messagebox.showerror(
                    "Error", "Unable to transcribe the audio. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    threading.Thread(target=process_audio).start()


root = tk.Tk()
root.title("J.A.R.V.I.S Voice Assistant")
root.geometry("400x600")

chat_history = tk.Text(root, wrap=tk.WORD, bg="#F5F5F5", state="disabled")
chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_input = ttk.Entry(root)
user_input.pack(padx=10, pady=10, fill=tk.X, expand=True)

speak_button = ttk.Button(root, text="Speak", command=on_click)
speak_button.pack(padx=10, pady=10)

root.mainloop()
