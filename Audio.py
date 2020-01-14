from typing import List

print("import pygame")
from pygame import mixer
import pygame
print("init Mixer")
mixer.init()


def _play(file: str):
    try:
        mixer.music.load(file)
        mixer.music.play()

    except pygame.error as e:
        print("Error: {} with file {}".format(e, file))


def play(files: List[str]) -> List[str]:
    if mixer.music.get_busy():
        return files
    else:
        _play(files[0])
        return files[1:]


def stop():
    mixer.music.stop()
