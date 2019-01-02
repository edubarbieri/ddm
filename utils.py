import os
import hashlib


def safe_name(path):
    if not os.path.exists(path):
        return path

    dir = os.path.dirname(path)
    name, ext = os.path.splitext(os.path.basename(path))

    i = 1
    while True:
        new_path = os.path.join(dir, name + " " + str(i) + ext)
        if not os.path.exists(new_path):
            return new_path
        i += 1


def file_md5(file_name):
    md5_hash = hashlib.md5()
    with open(file_name, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

