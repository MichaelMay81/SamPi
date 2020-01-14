#!/usr/bin/env python3

from Files import Files
import os
import Audio
print("import time, GPIO, mfrc522")
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def main():
    music_folder = os.path.expanduser("~/Music/SamPi/")
    files = Files(music_folder)
    audio_files = []
    print("init MFRC522")
    reader = SimpleMFRC522()
    playing = None
    none_counter = 0

    while True:
        # read tag
        id = reader.read_id_no_block()

        # no tag
        if not id:
            none_counter += 1
            if none_counter > 1 and playing:
                print("stopping playback")
                playing = None
                Audio.stop()

        else:
            none_counter = 0

            # new tag detected
            if playing != id:
                none_counter = 0
                Audio.stop()
                audio_files = files.get_audio_files(str(id))
                audio_files.sort()

                if audio_files:
                    print("playing {}".format(id))
                    playing = id
                    audio_files = Audio.play(audio_files)
                else:
                    print("unknown tag:", id)

            # continue playback
            elif audio_files:
                audio_files = Audio.play(audio_files)


try:
    main()
except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()
