import pyaudio  
import wave

def play_wav_file(file_path, output_device_index=8):
    CHUNK = 1024
    try:
        # Open the WAV file
        with wave.open(file_path, "rb") as wav_file:
            # Instantiate PyAudio
            audio_player = pyaudio.PyAudio()
            # Open the audio stream with the specified output device
            stream = audio_player.open(format=audio_player.get_format_from_width(wav_file.getsampwidth()),
                                       channels=wav_file.getnchannels(),
                                       rate=wav_file.getframerate(),
                                       output=True,
                                       output_device_index=output_device_index)
            # Read and play the audio data in chunks
            data = wav_file.readframes(CHUNK)
            while data:
                stream.write(data)
                data = wav_file.readframes(CHUNK)

            # Clean up: Close the stream and terminate PyAudio
            stream.stop_stream()
            stream.close()
            audio_player.terminate()
            print('Speech finished\n')

    except FileNotFoundError:
        print("Error: File not found.")
    except wave.Error:
        print("Error: Invalid WAV file.")
    except Exception as e:
        print("An error occurred:", str(e))

def show_available_output_devices():
    audio = pyaudio.PyAudio()
    print("Available output devices:")
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info["maxOutputChannels"] > 0:
            print(f"Device {i}: {device_info['name']}")
    audio.terminate()

if __name__ == '__main__':
    show_available_output_devices()
    index = input("> ")
    play_wav_file('audioResponse.wav', int(index))