#!/usr/bin/env python

import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from distutils.spawn import find_executable
from pwn import *


CHROME_PATH = find_executable('google-chrome')
CHROMEDRIVER_PATH = find_executable('chromedriver')
WINDOW_SIZE = "1920,1080"


def print_browser_log(url, brws_log):
    l = "\n\n".join([("""        source: %s
        message: [%s]
        level: %s""" % (line["source"], line["message"], line["level"])) for line in brws_log])

    log.info("""Browser log:
        URL: %s

%s
    """ % (url, l))


def get_args():
    parser = argparse.ArgumentParser(description="Prints the browser log for given URL")
    parser.add_argument("-u", "--url", help="URL to print browser log for")
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

    url = args.url

    driver.get(url)
    print_browser_log(url, driver.get_log('browser'))

    driver.close()


if __name__ == '__main__':
    main()
