#!/usr/bin/env python

import argparse
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from distutils.spawn import find_executable
from pwn import *
from selenium.common.exceptions import TimeoutException


CHROME_PATH = find_executable('google-chrome')
CHROMEDRIVER_PATH = find_executable('chromedriver')
WINDOW_SIZE = "1920,1080"


def get_args():
    parser = argparse.ArgumentParser(description="Visits a list of domains on HTTPS through Chrome and Proxy")
    parser.add_argument("-t", "--target-file", help="JSON with list of Domains to check")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--proxy-server=127.0.0.1:8080")
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        chrome_options=chrome_options
    )

    targets = json.load(open(args.target_file))

    for t in targets:
        u = "https://%s/" % t
        log.info("Get %s" % u)
        try:
            driver.get(u)
        except TimeoutException:
            log.warn("Timeout: %s" % u)

    driver.close()


if __name__ == '__main__':
    main()
