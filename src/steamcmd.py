from os import rmdir
from os.path import abspath
from subprocess import Popen, PIPE
from shutil import which, make_archive


def download_workshop(game_id: int, content_id: int) -> bool:
    try:
        proc = Popen([
            which("steamcmd"),
            "+force_install_dir", abspath("downloads/"),
            "+login", "anonymous",
            "+workshop_download_item", f"{game_id}", f"{content_id}",
            "+quit"
            ],
            stdout=PIPE)

        out, _ = proc.communicate()  # timeout?

        print("\n[DEBUG] ###########################")
        print(out.decode()) #.replace(b'\\r\\n', b'\n'))
        print("[DEBUG] ###########################\n")

        return out.split(b'\r\n')[8].startswith(b"Success")
    except IndexError:
        raise Exception("unexpected or invalid steamcmd output")
    except Exception as e:
        raise e


def compress_content(game_id: int, content_id: int) -> str:
    root_dir = f"downloads/steamapps/workshop/content/{game_id}/"
    archive_loc = f"archives/{content_id}"

    return make_archive(archive_loc, 'zip', root_dir=root_dir, base_dir=f"{content_id}")
