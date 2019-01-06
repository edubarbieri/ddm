import yaml
import os
from filedata import FileData
import os
import pathlib
import utils
import sys
import subtitles
import tvdb
import feed
import config

def print_logo():
    print("DDM v0.1")


def process_pending_files():
    source_folder = config.get_config()['sourceFolder']
    for root, _, files in os.walk(source_folder):
        for file in files:
            process_file(root, file)


def process_file(root, file):
    _, ext = os.path.splitext(file)
    if ext not in config.get_config()['videoExts']:
        return
    file_path = os.path.join(root, file)
    file_data = FileData(file_path)
    if not file_data.is_serie:
        print("movie moving is not implemented")
        return

    new_path = os.path.join(config.get_config()["targetFolder"], file_data.get_new_path())
    print("moving {0} to {1}".format(file_data.path, new_path))
    if not config.get_config()["testMode"]:
        # create new folder
        pathlib.Path(os.path.dirname(new_path)).mkdir(
            parents=True, exist_ok=True)
        os.rename(file_data.path, new_path)
        subtitle(new_path)



def subtitle(path):
    if subtitles.subtitle_exists(path):
        return
    subtitles.search_subtitles(path)


def process_subtitles():
    targer_folder = config.get_config()['targetFolder']
    for root, _, files in os.walk(targer_folder):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in config.get_config()['videoExts']:
                subtitle(os.path.join(root, file))


if __name__ == '__main__':
    print_logo()
    if len(sys.argv) == 1:
        process_pending_files()
        process_subtitles()
    else:
        for arg in sys.argv[1:]:
            if arg == "subtitle" or arg == "subtitles":
                process_subtitles()
            elif arg == "move" or arg == "organize":
                process_pending_files()
            elif arg == "feed":
                feed.process()
            else:
                print("unrecognized option {}".format(arg))
