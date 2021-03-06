from json import load as jsload
from os.path import abspath, dirname, join

with open(join(dirname(abspath(__file__)), "../settings.json")) as settings_file:
    settings = jsload(settings_file)

adminIds = settings["admins"]


def isAdmin(chatId: int=-1):
    if chatId > 0:
        return chatId in adminIds
    else:
        return adminIds


def getLink(msg):
    if "entities" in msg:
        links = [x for x in msg["entities"] if x["type"] == "url"]
        if links:
            link = links[0]
            return msg["text"][link["offset"]:(link["offset"]+link["length"])].strip()
    return None


def short(url):
    from requests import utils, post

    escaped = url
    if "https://" not in url and "http://" not in url:
        escaped = "http://" + url
    escaped = escaped.replace("it-m.banggood.com", "banggood.com")
    escaped = escaped.replace("m.banggood.com", "banggood.com")

    headers = {
        "Authorization": settings["bitlyToken"],
        "Content-Type": "application/json"
    }
    params = {
        "long_url": utils.requote_uri(escaped)
    }

    try:
        response = post("https://api-ssl.bitly.com/v4/shorten", json=params, headers=headers)
        data = response.json()
        linkId = data["id"].replace("amzn.to/", "").replace("bit.ly/", "")
        return linkId
    except Exception:
        if url.startswith("http://bit.ly/") or url.startswith("https://bit.ly/") or url.startswith("bit.ly/") \
            or url.startswith("http://amzn.to/") or url.startswith("https://amzn.to/") or url.startswith("amzn.to/"):
            return url.split("/")[-1]
        return None
