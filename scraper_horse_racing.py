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
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup
import pandas as pd

def firefoxdriver(my_url):
    """
    Preparing of the Tor browser for the work and adding the headers 
    to the browser.
    """
    # Preparing of the Tor browser for the work.
    # for my laptop
    # torexe = os.popen(\
    #    r'C:\Users\Oliver\Desktop\Tor Browser\Browser\firefox.exe')
    # for my mainframe
    torexe = os.popen(\
        r'C:\Users\olive\OneDrive\Pulpit\Tor Browser\Browser\firefox.exe')
    # for my laptop
    # profile = FirefoxProfile(\
    #     r'C:\Users\Oliver\Desktop\Tor Browser\Browser\TorBrowser\Data\'+
    #     'Browser\profile.default')
    # for my mainframe
    profile = FirefoxProfile(\
        r'C:\Users\olive\OneDrive\Pulpit\Tor Browser\Browser\TorBrowser\Data'+
            '\Browser\profile.default')
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9150)
    profile.set_preference('network.proxy.socks_remote_dns', False)
    profile.update_preferences()
    firefox_options = Options()
    driver = Firefox(firefox_profile=profile, options=firefox_options)

    # # Adding the headers to the browser.
    _addingheaders(my_url)

    return driver

def _addingheaders(my_url):
    """Adding the headers to the browser."""
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64;'+
    ' rv:97.0) Gecko/20100101 Firefox/97.0', 'Accept': 'text/html,application'+
    '/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}
    req = session.get(my_url, headers=headers)

def scrapingitems(driver, hippodromes, my_list, end_xpath):
        """
        Create appropriate lists of the data for the pandas library.
        """
        for ind in range(1, (len(hippodromes)+1)):
            my_list.append('')
            my_list.append('')
            my_list.append('')
            # Enumeration of the race participants for the iteration.
            count_iterations = len(driver.find_elements(By.XPATH,
                '//div[@class="container__livetable"]/div[2]/div/section/div['
                +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
            for i in range(4, (count_iterations+2)):
                try:
                    my_elements_to_scrap = driver.find_element(By.XPATH,
                        '//div[@class="container__livetable"]/div[2]/div/'+
                        'section/div['+str(ind)+']/div[3]/div/div/div['+str(i)
                        +end_xpath).text
                    my_list.append(my_elements_to_scrap)
                except:
                    my_list.append('')

# Variable with the URL of the website.
my_url = 'https://www.horseracing24.com/'

# Preparing of the Tor browser for the work and adding the headers 
# to the browser.
driver = firefoxdriver(my_url)

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
        EC.presence_of_element_located((By.CLASS_NAME,
        'boxOverContent__bannerLink')))
except TimeoutException:
    print("Loading took too much time!. Please rerun the script.")
except Exception as e:
    print(str(e))
else:
    # Loads the website code as the BeautifulSoup object.
    pageSource = driver.page_source
    bsObj = BeautifulSoup(pageSource, 'lxml')

    # Determining the number of the hippodromes.
    hippodromes = bsObj.find_all('div', {'class':
        'subTabs subTabs--label'})

    # Building the list with the selected times.
    selected_times = bsObj.find_all('div', {'class':
        'subTabs__tab selected'})

    # Scraping of the hippodromes.
    for ind in range(1, (len(hippodromes)+1)):
        hippodrom = driver.find_element(By.XPATH ,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[1]').text
        list_of_hippodromes.append(hippodrom)
        list_of_hippodromes.append('')
        list_of_hippodromes.append('')
        # Inserting of the empty fields as many as participants in 
        # the race.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(1, (count_iterations-1)):
            list_of_hippodromes.append('')

    # Scraping of the selected start times.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_start_times.append('')
        list_of_start_times.append(selected_times[(ind-1)].get_text())
        list_of_start_times.append('')
        # Inserting of the empty fields as many as participants in 
        # the race.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(1, (count_iterations-1)):
            list_of_start_times.append('')

    # Scraping of the racing names and the additional race data.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_names_data.append('')
        # Scraping of the racing names.
        racing_name = driver.find_element(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[1]/div[2]/div/span').text
        list_of_names_data.append(racing_name)
        # Scraping of the additional race data.
        try:
            racing_data_1 = driver.find_element(By.XPATH,
                '//div[@class="container__livetable"]/div[2]/div/section/div['
                +str(ind)+']/div[3]/div/div/div[2]/span[1]').text
            string_of_racing_data = (racing_data_1 + '    ')
        except:
            racing_data_1 = ''
            string_of_racing_data = (racing_data_1 + '    ')
        try:
            racing_length = driver.find_element(By.XPATH,
                '//div[@class="container__livetable"]/div[2]/div/section/div['
                +str(ind)+']/div[3]/div/div/div[2]/span[2]')
            racing_data_2 = racing_length.get_attribute("title")
            string_of_racing_data = string_of_racing_data + (racing_data_2 +
                '    ')
        except:
            racing_data_2 = ''
            string_of_racing_data = string_of_racing_data + (racing_data_2 +
                '    ')
        try:
            racing_data_3 = driver.find_element(By.XPATH,
                '//div[@class="container__livetable"]/div[2]/div/section/div['
                +str(ind)+']/div[3]/div/div/div[2]/span[3]').text
            string_of_racing_data = string_of_racing_data + (racing_data_3 +
                '    ')
        except:
            racing_data_3 = ''
            string_of_racing_data = string_of_racing_data + (racing_data_3 +
                '    ')
        try:
            racing_data_4 = driver.find_element(By.XPATH,
                '//div[@class="container__livetable"]/div[2]/div/section/div['
                +str(ind)+']/div[3]/div/div/div[2]/span[4]').text
            string_of_racing_data = string_of_racing_data + (racing_data_4 +
                '    ')
        except:
            racing_data_4 = ''
            string_of_racing_data = string_of_racing_data + (racing_data_4 +
                '    ')
        try:
            racing_data_5 = driver.find_element(By.XPATH,
                '//div[@class="container__livetable"]/div[2]/div/section/div['
                +str(ind)+']/div[3]/div/div/div[2]/span[5]').text
            string_of_racing_data = string_of_racing_data + (racing_data_5 +
                '        ')
        except:
            racing_data_5 = ''
            string_of_racing_data = string_of_racing_data + (racing_data_5 +
                '        ')
        # Scraping of the status data (e.g. Finished).
        try:
            racing_data_6 = driver.find_element(By.XPATH,
                '//div[@class="container__livetable"]/div[2]/div/section/div['
                +str(ind)+']/div[3]/div/div/div[1]/div[3]').text
            string_of_racing_data = string_of_racing_data + racing_data_6
            string_of_racing_data.strip()
            list_of_names_data.append(string_of_racing_data)
        except:
            racing_data_6 = ''
            string_of_racing_data = string_of_racing_data + racing_data_6
            string_of_racing_data.strip()
            list_of_names_data.append(string_of_racing_data)
        # Inserting of the empty fields as many as participants in 
        # the race.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(1, (count_iterations-1)):
            list_of_names_data.append('')

    # Scraping of the ratings.
    end_xpath_ratings = ']/div[2]'
    scrapingitems(driver, hippodromes, list_of_ratings, end_xpath_ratings)
    # for ind in range(1, (len(hippodromes)+1)):
    #     list_of_ratings.append('')
    #     list_of_ratings.append('')
    #     list_of_ratings.append('')
    #     # Enumeration of the race participants for the iteration.
    #     count_iterations = len(driver.find_elements(By.XPATH,
    #         '//div[@class="container__livetable"]/div[2]/div/section/div['
    #         +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
    #     for i in range(4, (count_iterations+2)):
    #         try:
    #             rating = driver.find_element(By.XPATH,
    #                 '//div[@class="container__livetable"]/div[2]/div/section/'
    #                 +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
    #                 +'[2]').text
    #             list_of_ratings.append(rating)
    #         except:
    #             list_of_ratings.append('')

    # Scraping of the countries.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_countries.append('')
        list_of_countries.append('')
        list_of_countries.append('')
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                country_string = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[3]/span')
                country=country_string.get_attribute('title')
                list_of_countries.append(country)
            except:
                list_of_countries.append('')

    # Scraping of the horse names.
    end_xpath_horses = ']/div[3]'
    scrapingitems(driver, hippodromes, list_of_horses, end_xpath_horses)
    # for ind in range(1, (len(hippodromes)+1)):
    #     list_of_horses.append('')
    #     list_of_horses.append('')
    #     list_of_horses.append('')
    #     # Enumeration of the race participants for the iteration.
    #     count_iterations = len(driver.find_elements(By.XPATH,
    #         '//div[@class="container__livetable"]/div[2]/div/section/div['
    #         +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
    #     for i in range(4, (count_iterations+2)):
    #         try:
    #             horse = driver.find_element(By.XPATH,
    #                 '//div[@class="container__livetable"]/div[2]/div/section/'
    #                 +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
    #                 +'[3]').text
    #             list_of_horses.append(horse)
    #         except:
    #             list_of_horses.append('')

    # Scraping of the names of the jockeys and the trainers.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_jockeys_trainers.append('')
        list_of_jockeys_trainers.append('')
        list_of_jockeys_trainers.append('')
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                jockey_trainer = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[4]').text
                list_of_jockeys_trainers.append(jockey_trainer)
            except:
                list_of_jockeys_trainers.append('')

    # Scraping of the age.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_age.append('')
        list_of_age.append('')
        list_of_age.append('')
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                age = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[5]').text
                list_of_age.append(age)
            except:
                list_of_age.append('')

    # Scraping of the weights.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_weights.append('')
        list_of_weights.append('')
        list_of_weights.append('')
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                weight = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[6]').text
                list_of_weights.append(weight)
            except:
                list_of_weights.append('')

    # Scraping of the traveled_distances.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_traveled_distances.append('')
        list_of_traveled_distances.append('')
        list_of_traveled_distances.append('')
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                traveled_distance = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[7]').text
                list_of_traveled_distances.append(traveled_distance)
            except:
                list_of_traveled_distances.append('')

    # Scraping of the comments about the each way bets.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_bet_comments.append('')
        list_of_bet_comments.append('')
        list_of_bet_comments.append('')
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            # Scraping of the comments about the each way bets.
            try:
                comment = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[8]/span')
                bet_comment_1 = comment.get_attribute("class")
                string_of_comments = (bet_comment_1 + '    ')
            except:
                bet_comment_1 = ''
                string_of_comments = (bet_comment_1 + '    ')
            try:
                comment = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[8]/span')
                bet_comment_2 = comment.get_attribute('alt')
                text_in_one_row = bet_comment_2.split()
                bet_comment_2 = " ".join(text_in_one_row)
                bet_comment_2 = bet_comment_2.replace('[d]', ' » ')
                bet_comment_2 = bet_comment_2.replace('[u]', ' » ')
                string_of_comments = string_of_comments + bet_comment_2
                string_of_comments.strip()
                list_of_bet_comments.append(string_of_comments)
            except:
                bet_comment_2 = ''
                string_of_comments = string_of_comments + bet_comment_2
                string_of_comments.strip()
                list_of_bet_comments.append(string_of_comments)

    # Scraping of the each way bets.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_each_way_bets.append('')
        list_of_each_way_bets.append('')
        list_of_each_way_bets.append('')
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                each_way_bet = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[8]/span').text
                list_of_each_way_bets.append(each_way_bet)
            except:
                list_of_each_way_bets.append('')

    # Scraping of the comments about the winners.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_winner_comments.append('')
        list_of_winner_comments.append('')
        list_of_winner_comments.append('')
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH ,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            # Scraping of the comments about the winners.
            try:
                comment = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[9]/span')
                winner_comment_1 = comment.get_attribute("class")
                string_of_winner_comments = (winner_comment_1 + '    ')
            except:
                winner_comment_1 = ''
                string_of_winner_comments = (winner_comment_1 + '    ')
            try:
                comment = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[9]/span')
                winner_comment_2 = comment.get_attribute('alt')
                winner_text_in_one_row = winner_comment_2.split()
                winner_comment_2 = " ".join(winner_text_in_one_row)
                winner_comment_2 = winner_comment_2.replace('[d]', ' » ')
                winner_comment_2 = winner_comment_2.replace('[u]', ' » ')
                string_of_winner_comments = string_of_winner_comments +\
                    winner_comment_2
                string_of_winner_comments.strip()
                list_of_winner_comments.append(string_of_winner_comments)
            except:
                winner_comment_2 = ''
                string_of_winner_comments = string_of_winner_comments +\
                    winner_comment_2
                string_of_winner_comments.strip()
                list_of_winner_comments.append(string_of_winner_comments)

    # Scraping of the winners.
    for ind in range(1, (len(hippodromes)+1)):
        list_of_winners.append('')
        list_of_winners.append('')
        list_of_winners.append('')
        # Enumeration of the race participants for the iteration.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(4, (count_iterations+2)):
            try:
                winner = driver.find_element(By.XPATH,
                    '//div[@class="container__livetable"]/div[2]/div/section/'
                    +'div['+str(ind)+']/div[3]/div/div/div['+str(i)+']/div'
                    +'[9]/span').text
                list_of_winners.append(winner)
            except:
                list_of_winners.append("")

    # Add lists with the scraped data to the dictionary in the correct 
    # order.
    dictionary_of_races['Hippodrome'] = list_of_hippodromes
    dictionary_of_races['Start time'] = list_of_start_times
    dictionary_of_races['Racing name and data'] = list_of_names_data
    dictionary_of_races['Rating'] = list_of_ratings
    dictionary_of_races['Country'] = list_of_countries
    dictionary_of_races['Horse'] = list_of_horses
    dictionary_of_races['Jockey/Trainer'] = list_of_jockeys_trainers
    dictionary_of_races['Age'] = list_of_age
    dictionary_of_races['Weight'] = list_of_weights
    dictionary_of_races['Traveled distance'] = list_of_traveled_distances
    dictionary_of_races['Bet comment'] = list_of_bet_comments
    dictionary_of_races['Each way bet'] = list_of_each_way_bets
    dictionary_of_races['Winner comment'] = list_of_winner_comments
    dictionary_of_races['Winner'] = list_of_winners

    # Creating of the frame for the data.
    df_res = pd.DataFrame(dictionary_of_races)

    # Saving of the properly formatted data to the csv file. The date 
    # and the time of the scraping are hidden in the file name.
    name_of_file = lambda: "horseracing{}.csv".format(time.strftime(\
        "%Y%m%d-%H.%M.%S"))
    df_res.to_csv(name_of_file(), encoding="utf-8")

finally:
    driver.quit()