import yaml
import os
from models.FileData import FileData
from clients.TvdbClient import TVDBClient
from clients.OpenSubtitles import OpenSubtitlesClient
import os
import pathlib
import utils
import sys
config = {}
# read config file
with open("config.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("Error reading config file: ", exc)
        exit(1)


def print_logo():
    print("DDM v0.1")


def process_pending_files():
    source_folder = config['sourceFolder']
    for root, _, files in os.walk(source_folder):
        for file in files:
            process_file(root, file)


def process_file(root, file):
    _, ext = os.path.splitext(file)
    if ext not in config['videoExts']:
        return
    file_path = os.path.join(root, file)
    file_data = FileData(file_path)
    if not file_data.is_serie:
        print("movie moving is not implemented")
        return

    new_path = os.path.join(
        config["targetFolder"], get_serie_new_path(file_data))
    print("moving {0} to {1}".format(file_data.path, new_path))
    if not config["testMode"]:
        # create new folder
        pathlib.Path(os.path.dirname(new_path)).mkdir(
            parents=True, exist_ok=True)
        os.rename(file_data.path, new_path)
        subtitle(new_path)


def get_serie_new_path(file_data):
    serie_name = _get_tvdbclient().get_serie_name(file_data.name)
    if serie_name == None:
        serie_name = file_data.name
    episode_name = _get_tvdbclient().get_episode_name(
        file_data.name, file_data.season, file_data.episode)
    _, ext = os.path.splitext(file_data.path)
    new_path = None
    if episode_name == None:
        new_path = "{0}/Season {1:02d}/{0} - S{1:02d}E{2:02d}{3}".format(
            serie_name, file_data.season, file_data.episode, ext)
    else:
        new_path = "{0}/Season {1:02d}/{0} - S{1:02d}E{2:02d} - {3}{4}".format(
            serie_name, file_data.season, file_data.episode, episode_name, ext)

    return utils.safe_name(new_path)


tvdb_client = None


def _get_tvdbclient():
    global tvdb_client
    if tvdb_client == None:
        tvdb_client = TVDBClient()
    return tvdb_client


osub_client = None


def _get_osub_client():
    global osub_client
    if osub_client == None:
        osub_client = OpenSubtitlesClient(config)
    return osub_client


def subtitle(path):
    _get_osub_client().download_subtitle(path)


def process_subtitles():
    targer_folder = config['targetFolder']
    for root, _, files in os.walk(targer_folder):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext not in config['videoExts']:
                return
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
            else:
                print("unrecognized option {}".format(arg))
