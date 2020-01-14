import threading
from queue import Queue
from Files import Files
import os
import Audio
from typing import List, Tuple


def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def print_menu(options: List[Tuple[int, str]]):
    print(30 * "-" , "MENU" , 30 * "-")
    for (i, o) in enumerate(options):
        print("{}. {}".format(i+1, o))
    print("q. Exit")
    print(67 * "-")


def kbd_listener(q: Queue, music_folder: str):
    files = Files(os.path.expanduser(music_folder))
    loop = True
    while loop:
        tags = files.get_tag_dirs()

        print_menu(tags)

        kbd_input = ""
        while kbd_input == "":
            kbd_input = input("> ")

        if kbd_input == "q":
            print("Stopping kbd_listener")
            loop = False
            q.put(kbd_input)
        elif is_int(kbd_input) and 0 < int(kbd_input) <= len(tags):
            q.put(tags[int(kbd_input) - 1])


def main():
    music_folder = os.path.expanduser("~\\Music\\SamPi\\")
    files = Files(music_folder)
    audio_files = []
    queue = Queue()
    t = threading.Thread(target=kbd_listener, args=(queue, music_folder))
    t.start()

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

main()
