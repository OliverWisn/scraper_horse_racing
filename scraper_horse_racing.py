# scraper_horse_racing.py
# -*- coding: utf-8 -*-

import os

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

# Variable with the URL of the website.
my_url = "https://www.horseracing24.com/"

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
driver = Firefox(firefox_profile=profile, options=firefox_options)

# Adding the headers to the browser
session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0)"+\
" Gecko/20100101 Firefox/97.0", "Accept": "text/html,application"+\
"/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}
req = session.get(my_url, headers=headers)

# Loads the website code as the Selenium object.
driver.get(my_url)

# Prepare the blank dictionary to fill in for pandas.
dictionary_of_races = {}

# Preparation of lists with scraped data.
list_of_hippodromes = []
list_of_start_times = []
list_of_racing_names = []
list_of_year_groups = []
list_of_distances = []
list_of_winnings = []
list_of_goings = []
list_of_countries = []
list_of_horses = []
list_of_jockeys_trainers = []
list_of_ages = []
list_of_weights = []
list_of_traveled_distances = []
list_of_each_way_bets = []
list_of_winners = []

# Wait for page to fully render
try:
    element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CLASS_NAME, \
            "boxOverContent__bannerLink")))
finally:
    # Loads the website code as the BeautifulSoup object.
    pageSource = driver.page_source
    bsObj = BeautifulSoup(pageSource, "lxml")

    # Determining the number of items to be scraped with the help of 
    # the BeautifulSoup.
    hippodromes = bsObj.find_all("div", {"class":\
    "subTabs subTabs--label"})

    print(len(hippodromes))

    driver.quit()