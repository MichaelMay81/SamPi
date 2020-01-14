import os
from typing import List


class Files:
    def __init__(self, files_location: str):
        self.files_location = files_location
        self.audio_exts = [".mp3", ".ogg"]

        if not os.path.exists(files_location):
            print("ERROR: {} does not exist".format(files_location))
        elif not os.path.isdir(files_location):
            print("ERROR: {} is not a directory".format(files_location))

    def get_tag_dirs(self):
        items = os.listdir(self.files_location)
        return [i for i in items if os.path.isdir(os.path.join(self.files_location, i))]

    def get_audio_files(self, tag: str) -> List[str]:
        abs_dir = os.path.join(self.files_location, tag)
        if not os.path.exists(abs_dir):
            print("ERROR: {} does not exist".format(abs_dir))
            return []
        elif not os.path.isdir(abs_dir):
            print("ERROR: {} is not a directory".format(abs_dir))
            return []
        else:
            files = [os.path.join(root, file)
                     for root, dirs, files in os.walk(abs_dir)
                     for file in files]

            audio_files = list(filter(lambda f: any([f.endswith(ext) for ext in self.audio_exts]), files))

            #for file in audio_files:
            #    print(file)

            return audio_files
