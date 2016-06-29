#-*- coding: utf-8 -*-


__all__ = [
    "mixed_content_check",
    "mixed_content_itercheck"
]


import re
from selenium.webdriver import PhantomJS
from logging import warning


def mixed_content_check(wd, url, auth=None):
    if auth is not None:
        user, passwd = auth
        url = re.sub("(https?)" + re.escape("://"), "\\1" + re.escape("%s:%s@" % (user, passwd)), url)
    wd.get(url)
    a = wd.get_log("browser")
    for m in a:
        if "insecure content" in m["message"].lower():
            return True
    return False


def mixed_content_itercheck(url_items):
    service_args = [
        '--ignore-ssl-errors=true'
        # '--proxy=127.0.0.1:8080'
        ]

    for url, auth in url_items:
        try:
            wd = PhantomJS(service_args=service_args)
            if mixed_content_check(wd, url, auth):
                yield url, auth
            wd.close()
        except Exception, e:
            warning("Could not check %s: %s" % (url, str(e)))
