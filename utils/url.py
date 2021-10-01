from utils.log import log
def safe_url(url):
    if url is None:
        return None
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://"+url
    if not url.endswith("/"):
        url = url + "/"
    return url