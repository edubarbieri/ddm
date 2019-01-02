import requests
import os
import gzip
import shutil
import utils
import struct


def get_hash(path):
    '''Original from: http://goo.gl/qqfM0
        https://github.com/agonzalezro/python-opensubtitles
    '''
    longlongformat = 'q'  # long long
    bytesize = struct.calcsize(longlongformat)
    size = os.path.getsize(path)
    try:
        f = open(path, "rb")
    except(IOError):
        return "IOError"

    hash = size

    if size < 65536 * 2:
        return "SizeError"

    for _ in range(65536 // bytesize):
        buffer = f.read(bytesize)
        (l_value, ) = struct.unpack(longlongformat, buffer)
        hash += l_value
        hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

    f.seek(max(0, int(size) - 65536), 0)
    for x in range(65536 // bytesize):
        buffer = f.read(bytesize)
        (l_value, ) = struct.unpack(longlongformat, buffer)
        hash += l_value
        hash = hash & 0xFFFFFFFFFFFFFFFF

    f.close()
    returnedhash = "%016x" % hash
    return str(returnedhash)


def subtitle_exists(path):
    sub_file = subtitle_name(path)
    return os.path.exists(sub_file)

def subtitle_name(path):
    dir = os.path.dirname(path)
    name, _ = os.path.splitext(os.path.basename(path))
    return os.path.join(dir, name + ".srt")

def _dowload_file(path, sub_link):
    str_file = utils.safe_name(subtitle_name(path))
    resp = requests.get(sub_link, allow_redirects=True)
    gz_file = str_file + ".gz"
    with open(gz_file, 'wb') as gz_stream:
        gz_stream.write(resp.content)
    with gzip.open(gz_file, 'rb') as f_in:
        with open(str_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(gz_file)

def search_subtitles(path, language = "pob"):
    hash = get_hash(path)
    size = os.path.getsize(path)
    url = f"https://rest.opensubtitles.org/search/sublanguageid-{language}/moviehash-{hash}/moviebytesize-{size}"
    resp = requests.get(url, headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "DudaDownloadManager",
    })
    if resp.status_code != 200 or len(resp.json()) == 0:
        print("Could not find subtitle for file {}".format(path))
        return
    for sub in resp.json():
        _dowload_file(path, sub["SubDownloadLink"])
    







