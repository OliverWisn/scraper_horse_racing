# scraper_horse_racing.py
# -*- coding: utf-8 -*-

import os

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options

# Variable with the URL of the website.
my_url = "http://check.torproject.org"

# Preparing of the Tor browser for the work.
torexe = os.popen(\
    r"C:\Users\olive\OneDrive\Pulpit\Tor Browser\Browser\firefox.exe")
profile = FirefoxProfile(\
    r"C:\Users\olive\OneDrive\Pulpit\Tor Browser\Browser\TorBrowser\Data"+\
    "\Browser\profile.default")
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "127.0.0.1")
profile.set_preference("network.proxy.socks_port", 9150)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.update_preferences()
firefox_options = Options()
driver = Firefox(firefox_profile= profile, options = firefox_options)
driver.get(my_url)





# driver.close()