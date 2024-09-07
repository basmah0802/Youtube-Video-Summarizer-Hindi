import os
import time
import assemblyai as aai
from yt_dlp import YoutubeDL
from pydub import AudioSegment

# Ensure the "uploads" directory exists
uploads_dir = 'uploads'
os.makedirs(uploads_dir, exist_ok=True)

# Set your AssemblyAI API key
aai.settings.api_key = "81085b1a0f7445868571375bffc4f7e9"

def transcribe_youtube_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(uploads_dir, 'audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    audio_file = os.path.join(uploads_dir, 'audio.mp3')

    # Convert audio to wav with correct sample rate
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000)  # Set sample rate to 16 kHz
    audio_file_wav = os.path.join(uploads_dir, 'audio.wav')
    audio.export(audio_file_wav, format="wav")

    # Transcribe audio using AssemblyAI
    config = aai.TranscriptionConfig(language_code="hi")
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(audio_file_wav)

    # Polling for the transcription result
    while transcript.status not in ("completed", "failed"):
        time.sleep(5)
        transcript = transcriber.get_transcription(transcript.id)

    if transcript.status == "failed":
        raise Exception("Transcription failed")

    text = transcript.text

    # Clean up the downloaded audio files
    os.remove(audio_file)
    os.remove(audio_file_wav)

    # Save the transcribed text to a file
    transcription_file = 'transcription.txt'
    with open(transcription_file, 'w', encoding='utf-8') as file:
        file.write(text)
    
    return transcription_file

if __name__ == "__main__":
    import sys
    youtube_url = sys.argv[1]
    try:
        transcribe_youtube_audio(youtube_url)
    except Exception as e:
        print(f"Error: {str(e)}")