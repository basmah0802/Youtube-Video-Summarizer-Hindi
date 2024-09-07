import os
import threadpoolctl

# Set environment variables
os.environ['KMP_INIT_AT_FORK'] = 'FALSE'
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Control the OpenMP libraries with threadpoolctl
threadpoolctl.threadpool_limits(limits=1, user_api='openmp')

from googletrans import Translator
from summarizer import Summarizer

def translate_and_summarize(transcription_file):
    if not os.path.exists(transcription_file):
        raise FileNotFoundError(f"{transcription_file} not found.")

    with open(transcription_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Translate the transcribed text to English
    try:
        transcriber_translator = Translator()
        translated_text = transcriber_translator.translate(text, src='hi', dest='en').text
    except Exception as e:
        raise RuntimeError(f"Translation failed: {str(e)}")

    # Summarize the translated text using BERT Extractive Summarizer
    try:
        summarizer = Summarizer()
        summary = summarizer(translated_text, num_sentences=8, min_length=60)
    except Exception as e:
        raise RuntimeError(f"Summarization failed: {str(e)}")

    # Translate the summary back to Hindi
    try:
        summary_translator = Translator()
        translated_summary = summary_translator.translate(summary, src='en', dest='hi').text
    except Exception as e:
        raise RuntimeError(f"Summary translation failed: {str(e)}")

    # Save the translated summary to a file
    summary_file = 'translated_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as file:
        file.write(translated_summary)

    return summary_file

if __name__ == "__main__":
    transcription_file = 'transcription.txt'
    try:
        translate_and_summarize(transcription_file)
        print("Translation and summarization completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")