#!/usr/bin/env python3

import argparse
import os
import Menu
from Files import Files
from queue import Queue
import Audio


def main(music_folder: str, disable_menu: bool, enable_rfid: bool):
    music_folder = os.path.expanduser(music_folder)
    files = Files(music_folder)
    audio_files = []
    queue = Queue()
    t = Menu.start_kbd_listener_thread(queue, music_folder)

    # main loop
    loop = True
    while loop:
        if audio_files:
            audio_files = Audio.play(audio_files)
        if not queue.empty():
            key = queue.get()
            if key == "q":
                print("The End")
                t.join()
                loop = False
            else:
                print("{} was selected".format(key))
                Audio.stop()
                audio_files = files.get_audio_files(key)
                audio_files = Audio.play(audio_files)


# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--musicFolder', type=str, help="enables RFID reading", default="~\\Music\\SamPi\\")
parser.add_argument('--disableMenu', action='store_true', help="disables console menu")
parser.add_argument('--enableRfid', action='store_true', help="enables RFID reading")
args = parser.parse_args()

main(args.musicFolder, args.disableMenu, args.enableRfid)