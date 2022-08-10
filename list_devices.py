from pygame import mixer
import pygame._sdl2.audio as sdl2_audio

mixer.init()
devices = sdl2_audio.get_audio_device_names(0)
mixer.quit()

print("The available audio are the following")
for device in devices:
    print(f"- {device}")
