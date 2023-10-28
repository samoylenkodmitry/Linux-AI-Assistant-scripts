import sounddevice as sd
import numpy as np
import wave
import subprocess
import pyperclip
import time
import os
import threading
import sys
import psutil


FIFO_PATH = "/tmp/stop_recording_signal"
sys.stdout = open('script_log.txt', 'w')
sys.stderr = open('script_error.txt', 'w')

def notify_user(message):
    """Send a notification to the user."""
    subprocess.run(["notify-send", message])

def bytes_to_human_readable(size_in_bytes):
    """Convert bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f} PB"

def record_until_signal(samplerate=16000):
    """Record audio until a signal is received in the named pipe."""
    notify_user("Recording started")
    print("Recording... Press F4 to stop recording or send a signal to the named pipe.")

    stop_signal_received = threading.Event()
    audio_data = []

    def listen_to_pipe():
        with open(FIFO_PATH, 'r') as fifo:
            fifo.read()
        stop_signal_received.set()

    threading.Thread(target=listen_to_pipe, daemon=True).start()

    with sd.InputStream(samplerate=samplerate, channels=1, dtype=np.int16) as stream:
        seconds_recorded = 0
        about_to_stop = False
        total_bytes_recorded = 0
        while about_to_stop is False:
            if stop_signal_received.is_set():
                about_to_stop = True
            audio_chunk, overflowed = stream.read(samplerate)
            audio_data.append(audio_chunk)

            # Calculate size in bytes for the current chunk and update total
            current_bytes = np.prod(audio_chunk.shape) * audio_chunk.itemsize
            total_bytes_recorded += current_bytes

            # Get available memory using psutil and convert to human readable format
            available_memory = bytes_to_human_readable(psutil.virtual_memory().available)

            seconds_recorded += 1
            notify_message = (f"Recording... {seconds_recorded}s elapsed, "
                              f"{bytes_to_human_readable(total_bytes_recorded)} recorded, "
                              f"Available memory: {available_memory}")
            notify_user(notify_message)
            print(notify_message)

            if seconds_recorded % 30 == 0:
                hint_message = "Recording... To stop, press F4 or send a signal using 'echo 1 > /tmp/stop_recording_signal'."
                print(hint_message)
                notify_user(hint_message)

            time.sleep(1)

    return np.concatenate(audio_data, axis=0).flatten(), samplerate

def save_audio(filename, audio_data, samplerate):
    """Save audio data to a WAV file."""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

def get_whisper_path():
    try:
        result = subprocess.run(['which', 'whisper'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def recognize_and_copy_to_memory(audio_filename, model_type):
    """Recognize the audio and copy the result to memory."""
    whisper_path = get_whisper_path()
    if not whisper_path:
        print("Could not find the path to 'whisper'")
        whisper_path = "/home/s/.local/bin/whisper" # you need to change this for your installation path

    #cmd = [whisper_path, audio_filename, "--output_format", "txt", "--verbose", "False"] # uncomment to use OpenAI whisper
    model_filename = f"/media/huge/whisper/whisper.cpp/models/ggml-{model_type}.bin"
    print(f"Using model: {model_filename}")
    cmd = ["/media/huge/whisper/whisper.cpp/main", "-f", audio_filename, "-m", model_filename, "-otxt"] # this is where my whisper.cpp 
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error during transcription.")
        return
    #base_name = os.path.splitext(audio_filename)[0]  # uncomment to use OpenAI whisper
    txt_output_filename = f"{audio_filename}.txt"
    # Construct the path to the TXT result file
    #txt_output_filename = f"{base_name}.txt" # uncomment to use OpenAI whisper


    with open(txt_output_filename, 'r') as f:
        recognized_text = f.read().strip()

    # Optional: Delete the TXT result file after reading
    os.remove(txt_output_filename)
#    recognized_text = result.stdout
    print(f"Recognized Text:\n{recognized_text}")
    pyperclip.copy(recognized_text)
    subprocess.run(["xclip"], input=recognized_text.encode('utf-8'))
    notify_user("Transcription complete! Result copied to clipboard.")
    notify_user(recognized_text)

def main():
    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)
    else:
        print(f"Named pipe {FIFO_PATH} already exists.")
        with open(FIFO_PATH, 'w') as fifo:
            fifo.write('stop')
        os.remove(FIFO_PATH)
        notify_user("Stopped recording.")
        exit(0)
    # Check if there are any command-line arguments
    print(f"Command-line arguments: {sys.argv}")
    if len(sys.argv) > 1:
        model_type = sys.argv[1]

    try:
        audio_filename = "recording.wav"
        audio_data, samplerate = record_until_signal()
        save_audio(audio_filename, audio_data, samplerate)
        print(f"Audio saved as {audio_filename}. Size: {len(audio_data) * 2} bytes.")
        recognize_and_copy_to_memory(audio_filename, model_type)
    finally:
        os.remove(FIFO_PATH)

if __name__ == "__main__":
    main()
