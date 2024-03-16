from requests import RequestException, get as http_get
from re import IGNORECASE, compile as re_compile


_BASE_URL = "https://steamcommunity.com/sharedfiles/filedetails/?id={}"
_USER_AGENT = "SteamCMD Workshop Content Downloader"

_RE_GAME_ID = re_compile(r'https://steamcommunity\.com/app/([0-9]{3,10})', flags=IGNORECASE)
_RE_GAME_NAME = re_compile(r'<div class=\"apphub_AppName ellipsis\">([\S ]+)</div>', flags=IGNORECASE)
_RE_CONTENT_NAME = re_compile(r'<title>Steam Workshop::([\S ]+)</title>', flags=IGNORECASE)
_RE_VALID_URL = re_compile(r"^(?:https://){0,1}steamcommunity\.com/sharedfiles/filedetails/\?id=([0-9]+)(?:&searchtext=.*){0,1}$", flags=IGNORECASE)


class WorkshopContent(object):
    def __init__(self, game_id, game_name, content_id, content_name):
        self.game_id = game_id
        self.game_name = game_name
        self.content_id = content_id
        self.content_name = content_name


def get_content(content_id: int) -> WorkshopContent:
    """
    Makes request to steamcommunity workshop content page and parses HTML for information.

    Errors are expected to be handled by the caller.
    """

    content = WorkshopContent(game_id=0, game_name='', content_id=content_id, content_name='')

    try:
        req = http_get(_BASE_URL.format(content_id), headers={'User-Agent': _USER_AGENT})
        if req.status_code != 200:
            raise Exception("non 200 status code returned")

        content.game_id = int(_RE_GAME_ID.search(req.text).group(1))
        content.game_name = _RE_GAME_NAME.search(req.text).group(1)
        content.content_name = _RE_CONTENT_NAME.search(req.text).group(1)

    except (IndexError, AttributeError):
        raise Exception("could not parse response from steam")
    except ValueError as e:
        # shouldn't ever happen, but just in case
        raise e
    except RequestException as e:
        raise e

    return content
