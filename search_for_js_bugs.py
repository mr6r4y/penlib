#!/usr/bin/env python

import argparse
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from distutils.spawn import find_executable
from selenium.common.exceptions import TimeoutException
from pwn import *


CHROME_PATH = find_executable('google-chrome')
CHROMEDRIVER_PATH = find_executable('chromedriver')
WINDOW_SIZE = "1920,1080"


def get_args():
    parser = argparse.ArgumentParser(description=("Tests for JS/NETWORK bugs in browser console through a list "
                                                  "of URLs. Uses Chrome and Proxy"))
    parser.add_argument("-u", "--urls-file", help="JSON with list of URLs to check")

    args = parser.parse_args()

    return args


def check_javascript(brws_log):
    return any(map(lambda a: True if a["source"] == "javascript" else False, brws_log))


def check_network(brws_log):
    return any(map(lambda a: True if a["source"] == "network" else False, brws_log))


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

    driver.set_page_load_timeout(30)

    urls = open(args.urls_file, "r")

    all_urls = set()
    netw_errors = []
    js_errors = []
    for n, url in enumerate(map(lambda u: u.strip().strip("/"), urls)):
        if url in all_urls:
            continue

        if n % 50 == 0:
            json.dump(js_errors, open("js_errors.json", "w"), indent=2)
            json.dump(netw_errors, open("netw_errors.json", "w"), indent=2)

        try:
            driver.get(url)
            log.info("Get URL: %s" % url)
        except TimeoutException:
            log.warn("Timeout: %s" % url)

        bl = driver.get_log('browser')
        if check_javascript(bl):
            js_errors.append(url)
            log.info("JS issue: %s" % url)
        if check_network(bl):
            netw_errors.append(url)
            log.info("NETW issue: %s" % url)
        all_urls.add(url)

    json.dump(js_errors, open("js_errors.json", "w"), indent=2)
    json.dump(netw_errors, open("netw_errors.json", "w"), indent=2)

    driver.close()


if __name__ == '__main__':
    main()
