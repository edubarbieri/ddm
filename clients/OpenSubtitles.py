from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import requests
import os
import gzip
import shutil
import utils

class OpenSubtitlesClient:
    _ost = None
    _token = None

    def __init__(self, config):
        self._ost = OpenSubtitles()
        self._token = self._ost.login(config["username"], config["password"])

    def download_subtitle(self, path):
        if(self.subtitle_exists(path)):
            print("Subtitle already exists for file {}".format(path))
            return
        #search subtitle
        print("Searching subtitle for file {}".format(path))
        file_info = File(path)
        data = self._ost.search_subtitles([{
            'sublanguageid': 'pob', 
            'moviehash': file_info.get_hash(), 
            'moviebytesize': file_info.size
        }])
        if len(data) == 0:
            print("Subtitle not found for file {}", path)
            return
        sub_link = data[0].get('SubDownloadLink')
        self._dowload_file(path, sub_link)
    
    def _dowload_file(self, path, sub_link):
        str_file = utils.safe_name(self._subtitle_name(path))
        resp = requests.get(sub_link, allow_redirects=True)
        gz_file = str_file + ".gz"
        with open(gz_file, 'wb') as gz_stream:
            gz_stream.write(resp.content)
        with gzip.open(gz_file, 'rb') as f_in:
            with open(str_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(gz_file)
    
    def _subtitle_name(self, path):
        dir = os.path.dirname(path)
        name, _ = os.path.splitext(os.path.basename(path))
        return os.path.join(dir, name + ".srt")
    
    def subtitle_exists(self, path):
        sub_file = self._subtitle_name(path)
        return os.path.exists(sub_file)