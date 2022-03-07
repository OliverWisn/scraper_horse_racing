# scraper_horse_racing.py
# -*- coding: utf-8 -*-

import os

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
import requests
from bs4 import BeautifulSoup

# Variable with the URL of the website.
my_url = "https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending"

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

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}
req = session.get(my_url, headers=headers)
# bsObj = BeautifulSoup(req.text, "lxml")
# print(bsObj.find("table", {"class": "table-striped"}).get_text)

driver.get(my_url)





# driver.close()