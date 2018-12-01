"""Selenium wrapper
"""


def make_screenshot(driver, url, snapshot_file):
    driver.get(url)
    driver.save_screenshot(snapshot_file)
