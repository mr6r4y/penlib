import requests


__all__ = [
    "session"
]


def session(auth=(), burp_proxy=False):
    """Helper function to produce requests sessions

    Sets automatically User-Agent and Accept headers to look like a Chrome browser

    auth - sets the basic auth pair
    burp_proxy - if True turns the session object to use localhost:8080 proxy
    """

    s = requests.Session()
    s.verify = False
    s.auth = auth

    # Default Chrome headers
    s.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537"
    s.headers["Accept-Encoding"] = "gzip, deflate, sdch"
    s.headers["Accept-Language"] = "en-US,en;q=0.8"

    burp_proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }

    if burp_proxy:
        s.proxies = burp_proxies

    return s