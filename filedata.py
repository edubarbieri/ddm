import os, re
import tvdb
import utils

class FileData:
    path = ''
    name = ''
    season = None
    episode = None
    is_serie = False
    _new_path = None
    serie_name = None

    def __init__(self, path):
        self.path = path
        base_name = os.path.basename(path)
        rex = re.search("(.*)[sS](\\d{2})[eE](\\d{2})", base_name)
        if rex is None or len(rex.groups()) < 3:
            print("File {} isn't a serie episode".format(path))
        else:
            self.is_serie = True
            self.name = rex.group(1).replace(".", " ").strip()
            self.season = int(rex.group(2))
            self.episode = int(rex.group(3))
    
    def __str__(self):
        return "path: {}, name: {}, season: {}, episode: {}, is_serie: {}".format(self.path, self.name, self.season, self.episode, self.is_serie)

    def get_new_path(self):
        if self._new_path != None:
            return self._new_path
        self.serie_name = tvdb.get_serie_name(self.name)
        if self.serie_name == None:
            self.serie_name = self.name
        self.episode_name = tvdb.get_episode_name(self.name, self.season, self.episode)
        _, ext = os.path.splitext(self.path)
        new_path = None
        if self.episode_name == None:
            new_path = "{0}/Season {1:02d}/{0} - S{1:02d}E{2:02d}{3}".format(
                self.serie_name, self.season, self.episode, ext)
        else:
            new_path = "{0}/Season {1:02d}/{0} - S{1:02d}E{2:02d} - {3}{4}".format(
                self.serie_name, self.season, self.episode, self.episode_name, ext)
        self._new_path = utils.safe_name(new_path)
        return self._new_path