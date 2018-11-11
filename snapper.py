#!/usr/bin/env python

"""Makes www snapshots of a list of domains

You must have google-chrome and `chromedriver` installed.

Example:

    snapper.py -d ./snaps -j domains.josn

References:
    * http://chromedriver.chromium.org/

"""

import argparse
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from distutils.spawn import find_executable
from pwn import *


CHROME_PATH = find_executable('google-chrome')
CHROMEDRIVER_PATH = find_executable('chromedriver')
WINDOW_SIZE = "1920,1080"


def make_screenshot(driver, url, snapshot_file):
    driver.get(url)
    driver.save_screenshot(snapshot_file)


def get_args():
    parser = argparse.ArgumentParser(description="Make snapshot of a number of sites")
    parser.add_argument("-d", "--dir", help="Directory to save the snapshots")
    parser.add_argument("-j", "--json-file", help="JSON file with the list of domains to snap")
    parser.add_argument("-p", "--uri-path", default="", help="Add path to every URI")
    parser.add_argument("-t", "--httpauth-creds", help="Set user and password for HTTP Authenticated pages")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    save_dir = os.path.abspath(args.dir)
    domains = json.load(open(args.json_file, "r"))
    uri_path = args.uri_path
    httpauth_creds = args.httpauth_creds.split("::") if args.httpauth_creds else None

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        chrome_options=chrome_options
    )

    if httpauth_creds:
        u, p = httpauth_creds
        u_http_ptrn = "http://" + u + ":" + p + "@%s/%s"
        u_https_ptrn = "https://" + u + ":" + p + "@%s/%s"
    else:
        u_http_ptrn = "http://%s/%s"
        u_https_ptrn = "https://%s/%s"

    for d in domains:
        u_http = u_http_ptrn % (d, uri_path)
        f_http = os.path.join(save_dir, "http_%s.png" % d)
        u_https = u_https_ptrn % (d, uri_path)
        f_https = os.path.join(save_dir, "https_%s.png" % d)

        log.info("Save %s" % f_http)
        make_screenshot(driver, u_http, f_http)
        log.info("Save %s" % f_https)
        log.info("uri: %s" % u_https)
        make_screenshot(driver, u_https, f_https)

    driver.close()


if __name__ == '__main__':
    main()
