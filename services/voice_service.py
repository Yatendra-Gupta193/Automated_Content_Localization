import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import uuid
import os
from langdetect import detect, LangDetectException

LANGUAGE_MAP = {
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "English": "en",
    "Chinese (Simplified)": "zh",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Korean": "ko",
    "Italian": "it",
    "Dutch": "nl",
    "Turkish": "tr",
    "Indonesian": "id"
}

# -------- Speech To Text --------
def speech_to_text(audio_path):

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)

    except Exception as e:
        print("STT Error:", e)
        return "Could not transcribe audio.", None

    try:
        lang_code = detect(text)

    except LangDetectException:
        lang_code = None

    except Exception:
        lang_code = None

    return text, lang_code


# -------- Text To Speech --------
def text_to_speech(text, speaker_sample_path, target_language):

    lang_code = LANGUAGE_MAP.get(target_language, "en")

    output_filename = f"output_{uuid.uuid4().hex}.mp3"
    output_path = os.path.join("static", output_filename)

    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(output_path)

        return output_path

    except Exception as e:
        print("TTS Error:", e)
        raise


# -------- Convert Audio To WAV --------
def convert_to_wav(input_path):

    output_path = f"temp_converted_{uuid.uuid4().hex}.wav"

    try:
        audio = AudioSegment.from_file(input_path)

        audio = audio.set_channels(1).set_frame_rate(22050)

        audio.export(output_path, format="wav")

        print(f"Successfully converted {input_path} to {output_path}")

        return output_path

    except Exception as e:
        print(f"Error converting audio: {str(e)}")
        raise