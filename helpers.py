from os import listdir
from os.path import isfile, join

import settings


def csv_files():
    return [f for f in listdir(settings.MODEL_DIR) if
            isfile(join(settings.MODEL_DIR, f)) and f.endswith(settings.FILE_EXTENTION)]



def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
