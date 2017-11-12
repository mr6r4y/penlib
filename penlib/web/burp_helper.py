#-*- coding: utf-8 -*-


__all__ = [
    "setcookie_to_cookie"
]


def setcookie_to_cookie(setcookie_txt):
    return "Cookie: "+"; ".join([i.replace("Set-Cookie: ", "").split(";")[0] for i in setcookie_txt.split("\n")])
