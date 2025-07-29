import os
import whisper

def transcribe_audio_files(input_folder, output_folder):
    """
    Transcribes all MP3 files in the specified folder and writes the formatted output to individual text files.

    :param input_folder: Path to the folder containing MP3 files.
    :param output_folder: Path to the folder where formatted text files will be saved.
    """
    # Initialize the Whisper model
    model = whisper.load_model("base")

    # Loop through all files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".mp3"):
            file_path = os.path.join(input_folder, file_name)
            print(f"Transcribing {file_path}...")

            # Transcribe the audio file using the Whisper model
            result = model.transcribe(file_path)

            # Get the transcription text
            transcription = result['text']

            # Remove the sentence that begins with "Transcription for" and ends with "mp3: "
            if transcription.startswith("Transcription for") and "mp3: " in transcription:
                transcription = transcription.split("mp3: ", 1)[1].strip()

            # Format the transcription to be on a single line
            formatted_transcription = transcription.replace('\n', '').replace('\r', '')

            # Write the formatted transcription to the output file
            output_file = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.txt")
            with open(output_file, 'w') as f:
                f.write(formatted_transcription)

if __name__ == "__main__":
    # Define the input folder containing the MP3 files
    input_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "MP3-Files-Pre22"))
    # Define the output folder where formatted text files will be saved
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "Transcriptions-Pre22"))
    os.makedirs(output_folder, exist_ok=True)

    # Call the transcribe_audio_files function with the specified input and output folders
    transcribe_audio_files(input_folder, output_folder)