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

# hippodromes
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[1]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[1]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[1]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[4]/div[1]

# start_times (<div class="subTabs__tab selected">16:42</div>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[2]/div[1]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[2]/div[8]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[2]/div[1]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[4]/div[2]/div[1]

# racing_names (<span class="event__title--name" title="AUTEUIL: H.de Navailles Hurdle">AUTEUIL: H.de Navailles Hurdle</span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[1]/div[2]/div/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[1]/div[2]/div/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[1]/div[2]/div/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[4]/div[3]/div/div/div[1]/div[2]/div/span




# year_groups (<span>7yo+</span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[2]/span[1]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[2]/span[1]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[4]/div[3]/div/div/div[2]/span[1]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[5]/div[3]/div/div/div[2]/span[1]

# distances (<span title="Miles: 2, Furlongs: 7, Yards: 181">2m 7f 181y</span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[2]/span[1] see: year_groups
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[2]/span[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[2]/span[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[4]/div[3]/div/div/div[2]/span[2]

# winnings (<span>Winner: 2566.0 GBP</span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[2]/span[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[2]/span[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[2]/span[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[4]/div[3]/div/div/div[2]/span[3]

# goings (<span>Going: Standard</span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[2]/span[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[2]/span[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[4]/div[3]/div/div/div[2]/span[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[5]/div[3]/div/div/div[2]/span[4]




# countries (<span class="flag fl_77" title="France"></span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[3]/span
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[3]/span


# horses (<div class="event__participantName"><span class="flag fl_77" title="France"></span>Adrien Du Pont</div>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[3]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[3]
# ...


# jockeys_trainers (<div class="event__participantTeam">Maxwell M. D./Nicholls P. F.</div>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[4]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[4]
# ...


# ages (<div class="event__center event__result--age event__result--grey">10</div>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[5]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[5]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[5]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[5]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[5]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[5]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[5]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[5]
# ...


# weights (<div class="event__center event__result--weight event__result--grey">12-6</div>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[6]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[6]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[6]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[6]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[6]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[6]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[6]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[6]
# ...


# traveled_distances (<div class="event__center event__result--distance">29</div>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[7]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[7]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[7]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[7]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[7]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[7]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[7]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[7]
# ...


# each_way_bets (<div class="event__odd--odd1 kx no-odds no-odds--each_way null null odds__odd icon icon--arrow">-</div>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[8]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[8]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[8]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[8]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[8]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[8]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[8]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[8]
# ...


# winners (<div class="event__odd--odd2 kx no-odds no-odds--winner null null odds__odd icon icon--arrow">-</div>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[9]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[9]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[9]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[9]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[9]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[9]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[9]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[9]
# ...