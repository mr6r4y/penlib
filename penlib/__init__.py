#-*- coding: utf-8 -*-


__all__ = [
    "try_as_b64",
    "sh",
    "str2hex",
    "dumphex",
    "get_dw_samples",
    "session",
    "url_enc",
    "url_dec"
]


import os
import requests
import base64
import urllib
import re


def try_as_b64(txt):
    """Desperately trying to interpret something as base64 encoded value"""

    t = [i.strip() for i in re.split(u"[^\w]|[-_]", txt) if i.strip()]
    ft = []
    for k in t:
        for i in range(3):
            try:
                bt = base64.b64decode(k+(u"="*i))
                break
            except TypeError:
                bt = u""
        ft.append("".join([i for i in bt]))

    return "".join(ft)


def sh(command):
    os.system(command)


def str2hex(s, delim="", pref="\\x"):
    """String to hexadecimal values"""

    return delim.join([(pref + "%0.2X" % ord(i)) for i in s])


def dumphex(s, word_len=4, words_in_row=4, base=0):
    """Special function that prints out hex representation in a pretty format"""

    rows = []
    word = []
    row = []
    for n, i in enumerate([i for i in s]):
        if(n % word_len == 0 and n != 0):
            row.append(word)
            word = []
        word.append(i)
        if(len(row) >= words_in_row):
            rows.append(row)
            row = []
    if(word):
        row.append(word)
    if(row):
        rows.append(row)

    print "\n".join([("%0.8X:   %s  ||      %s" % (base+n*word_len*words_in_row,
                                                   "   ".join([" ".join(["%0.2X" % ord(b) for b in d]) for d in r]).ljust(word_len*words_in_row*3 + 8 + 4),
                                                   " ".join(["".join([(("%s" % b) if (ord(b) >= 32 and ord(b) <= 126) else ".")
                                                            for b in d]) for d in r]))) for n, r in enumerate(rows)])


def session(auth=(), burp_proxy=False):
    """Helper function to produce requests sessions

    Sets automatically User-Agent and Accept headers to look like a Chrome browser

    auth - sets the basic auth pair
    burp_proxy - if True turns the session object to use localhost:8080 proxy
    """

    s = requests.Session()
    s.verify = False
    s.auth = auth

    ## Default Chrome headers
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


def url_enc(s):
    return urllib.quote(s, safe="")


def url_dec(s):
    return urllib.unquote(s)


if __name__ == "__main__":
    pass
