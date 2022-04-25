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
# torexe = os.popen(\
#    r"C:\Users\Oliver\Desktop\Tor Browser\Browser\firefox.exe")
# for my mainframe
torexe = os.popen(\
    r"C:\Users\olive\OneDrive\Pulpit\Tor Browser\Browser\firefox.exe")
# for my laptop
# profile = FirefoxProfile(\
#     r"C:\Users\Oliver\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser"+\
#     "\profile.default")
# for my mainframe
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
list_of_names_data = []
list_of_ratings = []
list_of_countries = []
list_of_horses = []
list_of_jockeys_trainers = []
list_of_age = []
list_of_weights = []
list_of_traveled_distances = []
list_of_bet_comments = []
list_of_each_way_bets = []
list_of_winner_comments = []
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
            racing_data_2 = racing_length.get_attribute("title")
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
            string_of_racing_data = string_of_racing_data + (racing_data_5 +\
             "        ")
        except:
            racing_data_5 = ""
            string_of_racing_data = string_of_racing_data + (racing_data_5 +\
             "        ")
        # Scraping of the status data (e.g. Finished).
        try:
            racing_data_6 = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div[1]/div[3]').text
            string_of_racing_data = string_of_racing_data + racing_data_6
            string_of_racing_data.strip()
            list_of_names_data.append(string_of_racing_data)
        except:
            racing_data_6 = ""
            string_of_racing_data = string_of_racing_data + racing_data_6
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
            except:
                list_of_countries.append("")

    # Scraping of the horse names.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_horses.append("")
        list_of_horses.append("")
        list_of_horses.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                horse = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[3]').text
                list_of_horses.append(horse)
            except:
                list_of_horses.append("")

    # Scraping of the names of the jockeys and the trainers.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_jockeys_trainers.append("")
        list_of_jockeys_trainers.append("")
        list_of_jockeys_trainers.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                jockey_trainer = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[4]').text
                list_of_jockeys_trainers.append(jockey_trainer)
            except:
                list_of_jockeys_trainers.append("")

    # Scraping of the age.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_age.append("")
        list_of_age.append("")
        list_of_age.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                age = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[5]').text
                list_of_age.append(age)
            except:
                list_of_age.append("")

    # Scraping of the weights.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_weights.append("")
        list_of_weights.append("")
        list_of_weights.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                weight = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[6]').text
                list_of_weights.append(weight)
            except:
                list_of_weights.append("")

    # Scraping of the traveled_distances.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_traveled_distances.append("")
        list_of_traveled_distances.append("")
        list_of_traveled_distances.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                traveled_distance = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[7]').text
                list_of_traveled_distances.append(traveled_distance)
            except:
                list_of_traveled_distances.append("")

    # Scraping of the comments about the each way bets.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_bet_comments.append("")
        list_of_bet_comments.append("")
        list_of_bet_comments.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            # Scraping of the comments about the each way bets.
            try:
                comment = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[8]/span')
                bet_comment_1 = comment.get_attribute("class")
                string_of_comments = (bet_comment_1 + "    ")
            except:
                bet_comment_1 = ""
                string_of_comments = (bet_comment_1 + "    ")
            try:
                comment = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[8]/span')
                bet_comment_2 = comment.get_attribute("alt")
                text_in_one_row = bet_comment_2.split()
                bet_comment_2 = " ".join(text_in_one_row)
                bet_comment_2 = bet_comment_2.replace("[d]", " » ")
                bet_comment_2 = bet_comment_2.replace("[u]", " » ")
                string_of_comments = string_of_comments + bet_comment_2
                string_of_comments.strip()
                list_of_bet_comments.append(string_of_comments)
            except:
                bet_comment_2 = ""
                string_of_comments = string_of_comments + bet_comment_2
                string_of_comments.strip()
                list_of_bet_comments.append(string_of_comments)

    # Scraping of the each way bets.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_each_way_bets.append("")
        list_of_each_way_bets.append("")
        list_of_each_way_bets.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                each_way_bet = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[8]/span').text
                list_of_each_way_bets.append(each_way_bet)
            except:
                list_of_each_way_bets.append("")

    # Scraping of the comments about the winners.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_winner_comments.append("")
        list_of_winner_comments.append("")
        list_of_winner_comments.append("")
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,\
             '//div[@class="container__livetable"]/div[2]/div/section/div['\
             +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            # Scraping of the comments about the winners.
            try:
                comment = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[9]/span')
                winner_comment_1 = comment.get_attribute("class")
                string_of_winner_comments = (winner_comment_1 + "    ")
            except:
                winner_comment_1 = ""
                string_of_winner_comments = (winner_comment_1 + "    ")
            try:
                comment = driver.find_element(By.XPATH ,\
                '//div[@class="container__livetable"]/div[2]/div/section/div['\
                +str(ind)+']/div[3]/div/div/div['+str(i)+']/div[9]/span')
                winner_comment_2 = comment.get_attribute("alt")
                winner_text_in_one_row = winner_comment_2.split()
                winner_comment_2 = " ".join(winner_text_in_one_row)
                winner_comment_2 = winner_comment_2.replace("[d]", " » ")
                winner_comment_2 = winner_comment_2.replace("[u]", " » ")
                string_of_winner_comments = string_of_winner_comments +\
                 winner_comment_2
                string_of_winner_comments.strip()
                list_of_winner_comments.append(string_of_winner_comments)
                print(string_of_winner_comments)
            except:
                winner_comment_2 = ""
                string_of_winner_comments = string_of_winner_comments +\
                 winner_comment_2
                string_of_winner_comments.strip()
                list_of_winner_comments.append(string_of_winner_comments)
                print(string_of_winner_comments)


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


# winners (<span class="" alt="8.00">8.00</span>)
# (<span class="down" alt="2.37[d]2.20">2.20</span>)
# (<span class="" alt="3.00">3.00</span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[4]/div[9]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[5]/div[9]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[6]/div[9]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[7]/div[9]/span
# ...



    # Add lists with the scraped data to the dictionary in the correct 
    # order.
    dictionary_of_races["Hippodrome"] = list_of_hippodromes
    dictionary_of_races["Start time"] = list_of_start_times
    dictionary_of_races["Racing name and data"] = list_of_names_data
    dictionary_of_races["Rating"] = list_of_ratings
    dictionary_of_races["Country"] = list_of_countries
    dictionary_of_races["Horse"] = list_of_horses
    dictionary_of_races["Jockey/Trainer"] = list_of_jockeys_trainers
    dictionary_of_races["Age"] = list_of_age
    dictionary_of_races["Weight"] = list_of_weights
    dictionary_of_races["Traveled distance"] = list_of_traveled_distances
    dictionary_of_races["Bet comment"] = list_of_bet_comments
    dictionary_of_races["Each way bet"] = list_of_each_way_bets

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

# status_data (<div class="event__startTime">Start time: 25.04. 17:20</div>)
# (<div class="event__startTime">Finished</div>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[1]/div[3]/div/div/div[1]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[2]/div[3]/div/div/div[1]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[3]/div[3]/div/div/div[1]/div[3]
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[13]/div[3]/div/div/div[1]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[14]/div[3]/div/div/div[1]/div[3]
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[15]/div[3]/div/div/div[1]/div[3]
# ...




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


# each_way_bets (<span class="down" alt="17.00[d]7.50">7.50</span>)
# (<span class="up" alt="2.25[u]2.62">2.62</span>)
# (<span class="" alt="13.00">13.00</span>)
# (<span class="up not-published" alt="15.00[u]17.00 Odds removed by bookmaker.">17.00</span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[7]/div[3]/div/div/div[4]/div[8]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[7]/div[3]/div/div/div[5]/div[8]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[7]/div[3]/div/div/div[6]/div[8]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[7]/div[3]/div/div/div[13]/div[8]/span
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[8]/div[3]/div/div/div[4]/div[8]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[8]/div[3]/div/div/div[5]/div[8]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[8]/div[3]/div/div/div[6]/div[8]/span
# ...
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[4]/div[8]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[5]/div[8]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[6]/div[8]/span
# ...


# winners (<span class="" alt="8.00">8.00</span>)
# (<span class="down" alt="2.37[d]2.20">2.20</span>)
# (<span class="" alt="3.00">3.00</span>)
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[4]/div[9]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[5]/div[9]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[6]/div[9]/span
# /html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/section/div[9]/div[3]/div/div/div[7]/div[9]/span
# ...

