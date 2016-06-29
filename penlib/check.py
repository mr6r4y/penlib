#-*- coding: utf-8 -*-


__all__ = [
    "frameable_response_check",
    "frameable_response_itercheck"
]


import requests


def frameable_response_check(url, auth=None):
    r = requests.get(url, auth=auth, verify=False)
    return not (("x-frame-options" in r.headers) and (r.headers["x-frame-options"] == "SAMEORIGIN"))


def frameable_response_itercheck(url_items):
    for url, auth in url_items:
        if frameable_response_check(url, auth=auth):
            yield (url, auth)
