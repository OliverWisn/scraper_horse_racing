# scraper_horse_racing.py
# -*- coding: utf-8 -*-

import os
import time

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Variable with the URL of the website.
my_url = "https://www.horseracing24.com/"

# Preparing of the Tor browser for the work.
# for my laptop
torexe = os.popen(\
    r"C:\Users\Oliver\Desktop\Tor Browser\Browser\firefox.exe")
# for my mainframe
# torexe = os.popen(\
#    r"C:\Users\olive\OneDrive\Pulpit\Tor Browser\Browser\firefox.exe")
# for my laptop
profile = FirefoxProfile(\
    r"C:\Users\Oliver\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser"+\
    "\profile.default")
# for my mainframe
# profile = FirefoxProfile(\
#   r"C:\Users\olive\OneDrive\Pulpit\Tor Browser\Browser\TorBrowser\Data"+\
#    "\Browser\profile.default")
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
list_of_names_data = []
list_of_ratings = []
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

    # Determining the number of the hippodromes.
    hippodromes = bsObj.find_all("div", {"class":\
    "subTabs subTabs--label"})

    # Building the list with the selected times.
    selected_times = bsObj.find_all("div", {"class":\
    "subTabs__tab selected"})

    print(len(hippodromes))

    # Scraping of the hippodromes.
    for ind in range(1, (len(hippodromes)+1)):
        hippodrom = driver.find_element(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[1]').text
        list_of_hippodromes.append(hippodrom)
        list_of_hippodromes.append("")
        list_of_hippodromes.append("")
        # Inserting of the empty fields as many as participants in 
        # the race.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(1, (count_iterations-1)):
            list_of_hippodromes.append("")

    # Scraping of the selected start times.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_start_times.append("")
        list_of_start_times.append(selected_times[(ind-1)].get_text())
        list_of_start_times.append("")
        # Inserting of the empty fields as many as participants in 
        # the race.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(1, (count_iterations-1)):
            list_of_start_times.append("")

        print(selected_times[(ind-1)].get_text())
        print(count_iterations)

    # Scraping of the racing names and the additional race data.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_names_data.append("")
        # Scraping of the racing names.
        racing_name = driver.find_element(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[1]/div[2]/div/span').text
        list_of_names_data.append(racing_name)
        # Scraping of the additional race data.
        try:
            racing_data_1 = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div[2]/span[1]').text
            string_of_racing_data = (racing_data_1 + "    ")
        except:
            racing_data_1 = ""
            string_of_racing_data = (racing_data_1 + "    ")
        try:
            racing_length = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div[2]/span[2]')
            racing_data_2=racing_length.get_attribute("title")
            string_of_racing_data = string_of_racing_data + (racing_data_2 +\
             "    ")
        except:
            racing_data_2 = ""
            string_of_racing_data = string_of_racing_data + (racing_data_2 +\
             "    ")
        try:
            racing_data_3 = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div[2]/span[3]').text
            string_of_racing_data = string_of_racing_data + (racing_data_3 +\
             "    ")
        except:
            racing_data_3 = ""
            string_of_racing_data = string_of_racing_data + (racing_data_3 +\
             "    ")
        try:
            racing_data_4 = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div[2]/span[4]').text
            string_of_racing_data = string_of_racing_data + (racing_data_4 +\
             "    ")
        except:
            racing_data_4 = ""
            string_of_racing_data = string_of_racing_data + (racing_data_4 +\
             "    ")
        try:
            racing_data_5 = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div[2]/span[5]').text
            string_of_racing_data = string_of_racing_data + racing_data_5
            string_of_racing_data.strip()
            list_of_names_data.append(string_of_racing_data)
        except:
            racing_data_5 = ""
            string_of_racing_data = string_of_racing_data + racing_data_5
            string_of_racing_data.strip()
            list_of_names_data.append(string_of_racing_data)
        # Inserting of the empty fields as many as participants in 
        # the race.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(1, (count_iterations-1)):
            list_of_names_data.append("")

    # Scraping of the ratings.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_ratings.append("")
        list_of_ratings.append("")
        list_of_ratings.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                rating = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[2]').text
                list_of_ratings.append(rating)
            except:
                list_of_ratings.append("")

    # Scraping of the countries.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_countries.append("")
        list_of_countries.append("")
        list_of_countries.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                country_string = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[3]/span')
                country=country_string.get_attribute("title")
                list_of_countries.append(country)
                print(country)
            except:
                list_of_countries.append("")
                print("")


    # Scraping of the additional race data.
    # for ind in range(1, (len(hippodromes)+1)):
    #     list_of_racing_data.append("")
        


        # list_of_racing_names.append(racing_name)
        # list_of_racing_names.append("")
        # count_iterations = len(driver.find_elements(By.XPATH ,\
        #      '//div[@class="container__livetable"]/div[2]/div/section/div['\
        #      +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        # for i in range(1, (count_iterations-1)):
        #     list_of_racing_names.append("")

# countries (<span class="flag fl_77" title="France"></span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]  (<div class="container__livetable">)
# //*[@id="fsbody"]
# //*[@id="live-table"]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section (<section class="event">)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div (<div class="sportName horse-racing">)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[3]/span
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[3]/span


# countries (<span class="flag fl_77" title="France"></span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]  (<div class="container__livetable">)
# //*[@id="fsbody"]
# //*[@id="live-table"]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section (<section class="event">)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div (<div class="sportName horse-racing">)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[3]/span
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[3]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[3]/span


    # Add lists with the scraped data to the dictionary in the correct 
    # order.
    dictionary_of_races["Hippodrome"] = list_of_hippodromes
    dictionary_of_races["Start time"] = list_of_start_times
    dictionary_of_races["Racing name and data"] = list_of_names_data
    dictionary_of_races["Ratings"] = list_of_ratings
    dictionary_of_races["Countries"] = list_of_countries

    # Creating of the frame for the data.
    df_res = pd.DataFrame(dictionary_of_races)

    # Saving of the properly formatted data to the csv file. The date 
    # and the time of the scraping are hidden in the file name.
    name_of_file = lambda: "horseracing{}.csv".format(time.strftime(\
        "%Y%m%d-%H.%M.%S"))
    df_res.to_csv(name_of_file(), encoding="utf-8")


    driver.quit()




# hippodromes

# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section   
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

# class (<span>Class: 4</span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[6]/div[3]/div/div/div[2]/span[3]

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
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[6]/div[3]/div/div/div[2]/span[5]




# Rating
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[4]/div[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[5]/div[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[6]/div[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[12]/div[2]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[4]/div[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[5]/div[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[6]/div[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[19]/div[2]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[4]/div[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[5]/div[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[6]/div[2]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[21]/div[2]
# ...


# countries (<span class="flag fl_77" title="France"></span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]  (<div class="container__livetable">)
# //*[@id="fsbody"]
# //*[@id="live-table"]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section (<section class="event">)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div (<div class="sportName horse-racing">)
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