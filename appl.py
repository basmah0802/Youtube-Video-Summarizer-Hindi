from flask import Flask, request, render_template, send_from_directory
import os
import subprocess 

app = Flask(__name__)

# Ensure the "transcriptions" directory exists
transcriptions_dir = os.path.join(app.static_folder, 'transcriptions')
os.makedirs(transcriptions_dir, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    youtube_url = request.form['youtube_url']
    try:
        # Absolute paths to the virtual environments and Python scripts
        venv_assembly_path = 'c:/Users/basma/OneDrive/Desktop/PROJECT main/project2/venv_assembly/Scripts/python.exe'
        venv_googletrans_path = 'c:/Users/basma/OneDrive/Desktop/PROJECT main/project2/venv_googletrans/Scripts/python.exe'
        transcribe_script_path = 'c:/Users/basma/OneDrive/Desktop/PROJECT main/project2/transcribe.py'
        translate_script_path = 'c:/Users/basma/OneDrive/Desktop/PROJECT main/project2/translate.py'
        
        # Commands to run
        transcribe_command = [venv_assembly_path, transcribe_script_path, youtube_url]
        translate_command = [venv_googletrans_path, translate_script_path]
        
        # Print paths and commands for debugging
        print(f"Transcription command: {transcribe_command}")
        print(f"Translation command: {translate_command}")
        
        # Run the transcription script and capture the output
        transcribe_result = subprocess.run(transcribe_command, capture_output=True, text=True)
        
        if transcribe_result.returncode != 0:
            raise Exception(f"Transcription script failed with error: {transcribe_result.stderr}")
        
        # Run the translation and summarization script and capture the output
        translate_result = subprocess.run(translate_command, capture_output=True, text=True)
        
        if translate_result.returncode != 0:
            raise Exception(f"Translation script failed with error: {translate_result.stderr}")

        # Path to the final summary file
        summary_file_path = os.path.join(transcriptions_dir, 'translated_summary.txt')

        # Debug: Check if the file exists before renaming
        if os.path.exists('translated_summary.txt'):
            print("Translated summary file exists before renaming.")
        else:
            raise FileNotFoundError("Translated summary file not found before renaming.")

        # Check if the destination directory exists
        if not os.path.exists(transcriptions_dir):
            os.makedirs(transcriptions_dir, exist_ok=True)
        
        # Check if the destination file exists and remove it
        if os.path.exists(summary_file_path):
            os.remove(summary_file_path)
        
        # Move the new summary file to the destination directory
        os.rename('translated_summary.txt', summary_file_path)
        
        # Debug: Check if the file exists after renaming
        if os.path.exists(summary_file_path):
            print("Translated summary file exists after renaming.")
        else:
            raise FileNotFoundError("Translated summary file not found after renaming.")

        with open(summary_file_path, 'r', encoding='utf-8') as file:
            translated_summary = file.read()

        return render_template('results.html', text=translated_summary, text_file_path=summary_file_path)

    except Exception as e:
        return str(e)



@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(transcriptions_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)