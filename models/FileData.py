import os, re
class FileData:
    path = ''
    name = ''
    season = None
    episode = None
    is_serie = False

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
