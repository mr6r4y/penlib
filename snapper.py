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

from pwn import *


CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = os.path.expanduser('~/.local/bin/chromedriver')
WINDOW_SIZE = "1920,1080"


def make_screenshot(driver, url, snapshot_file):
    driver.get(url)
    driver.save_screenshot(snapshot_file)


def get_args():
    parser = argparse.ArgumentParser(description="Make snapshot of a number of sites")
    parser.add_argument("-d", "--dir", help="Directory to save the snapshots")
    parser.add_argument("-j", "--json-file", help="JSON file with the list of domains to snap")
    parser.add_argument("-p", "--uri-path", default="", help="Add path to every URI")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    save_dir = os.path.abspath(args.dir)
    domains = json.load(open(args.json_file, "r"))
    uri_path = args.uri_path

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        chrome_options=chrome_options
    )

    for d in domains:
        u_http = "http://%s/%s" % (d, uri_path)
        f_http = os.path.join(save_dir, "http_%s.png" % d)
        u_https = "https://%s/%s" % (d, uri_path)
        f_https = os.path.join(save_dir, "https_%s.png" % d)

        log.info("Save %s" % f_http)
        make_screenshot(driver, u_http, f_http)
        log.info("Save %s" % f_https)
        make_screenshot(driver, u_https, f_https)

    driver.close()


if __name__ == '__main__':
    main()
