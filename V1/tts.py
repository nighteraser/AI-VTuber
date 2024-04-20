# play_wav_file(file_path, output_device_index=Device)
# Device 6: 耳機 (Realtek(R) Audio)
# Device 7: 喇叭 (Realtek(R) Audio)
# Device 8: CABLE Input (VB-Audio Virtual Cable)

from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import torch
import pyaudio  
import wave

WAV_FILE_PATH = 'output.wav'

def load_model():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler_tts_mini_v0.1").to(device)
    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1", use_fast=False)
    print('Model and Tokenizer ready')
    return (device, model, tokenizer)

device, model, tokenizer = load_model()

def text2speech(text):
    prompt = text
    description = "A young girl speaker with a slightly low-pitched voice delivers her words quite expressively, in a very confined sounding environment with clear audio quality. She speaks very fast."

    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    try:
        generation = model.generate(input_ids=input_ids, 
                                    prompt_input_ids=prompt_input_ids, 
                                    max_new_tokens=2500)
    except:
        pass
    audio_arr = generation.cpu().numpy().squeeze()
    sf.write(WAV_FILE_PATH, audio_arr, model.config.sampling_rate)
    
    play_wav_file(WAV_FILE_PATH)


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

# Call the function to show available output devices
# show_available_output_devices()



if __name__ == "__main__":
    # Call the function to show available output devices
    # # show_available_output_devices()
    # init_model()
    # text2speech("hello, every")
    play_wav_file('output.wav')
