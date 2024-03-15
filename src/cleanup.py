from shutil import rmtree
from threading import Thread
from time import time, sleep
from os import listdir, path, remove


_AGE_LIMIT = 3600  # in seconds, files this age or older are removed
_ARCHIVE_DIR = path.abspath("archives/") + '/'
_CONTENT_DIR = path.abspath("downloads/steamapps/workshop/content/") + '/'


def _remove(file_loc: str):
    if (time() - path.getctime(file_loc)) >= _AGE_LIMIT:
        try:
            if path.isfile(file_loc):
                remove(file_loc)

            if path.isdir(file_loc):
                rmtree(file_loc)

        except Exception as e:
            print(f"[ERROR] (cleanup._remove) {e}")


def _cleanup_archives():
    if path.exists(_ARCHIVE_DIR) is False: return

    for file_loc in listdir(_ARCHIVE_DIR):
        if file_loc == 'README.txt': continue
        _remove(_ARCHIVE_DIR + file_loc)


def _cleanup_content():
    if path.exists(_CONTENT_DIR) is False: return

    for dir in listdir(_CONTENT_DIR):
        if path.isdir(_CONTENT_DIR + dir) is False: continue

        for content_loc in listdir(_CONTENT_DIR + dir):
            _remove(_CONTENT_DIR + dir + "/" + content_loc)


def _background():
    while True:
        # run cleanup first for any leftover files from last run
        _cleanup_archives()
        _cleanup_content()
        sleep(60)


def run_background():
    Thread(target=_background, daemon=True).start()
