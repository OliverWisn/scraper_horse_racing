# scraper_horse_racing.py

import time

from selenium.webdriver import Firefox
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
    Preparing of the browser for the work and adding the headers to 
    the browser.
    """
    # Preparing of the Tor browser for the work.
    options = Options()
    options.add_argument("--headless")
    driver = Firefox(options=options)

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
dict_races = {}

# Preparation of lists with scraped data.
lst_hippodromes = []
start_times = []
names_data = []
ratings = []
countries = []
horses = []
jockeys_trainers = []
lst_age = []
weights = []
traveled_distances = []
bet_comments = []
each_way_bets = []
winner_comments = []
winners = []

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
        lst_hippodromes.append(hippodrom)
        lst_hippodromes.append('')
        lst_hippodromes.append('')
        # Inserting of the empty fields as many as participants in 
        # the race.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(1, (count_iterations-1)):
            lst_hippodromes.append('')

    # Scraping of the selected start times.
    for ind in range(1, (len(hippodromes)+1)):
        start_times.append('')
        start_times.append(selected_times[(ind-1)].get_text())
        start_times.append('')
        # Inserting of the empty fields as many as participants in 
        # the race.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(1, (count_iterations-1)):
            start_times.append('')

    # Scraping of the racing names and the additional race data.
    for ind in range(1, (len(hippodromes)+1)):
        names_data.append('')
        # Scraping of the racing names.
        racing_name = driver.find_element(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[1]/div[2]/div/span').text
        names_data.append(racing_name)
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
            names_data.append(string_of_racing_data)
        except:
            racing_data_6 = ''
            string_of_racing_data = string_of_racing_data + racing_data_6
            string_of_racing_data.strip()
            names_data.append(string_of_racing_data)
        # Inserting of the empty fields as many as participants in 
        # the race.
        count_iterations = len(driver.find_elements(By.XPATH,
            '//div[@class="container__livetable"]/div[2]/div/section/div['
            +str(ind)+']/div[3]/div/div/div[*]/div[3]'))
        for i in range(1, (count_iterations-1)):
            names_data.append('')

    # Scraping of the ratings.
    end_xpath_ratings = ']/div[2]'
    scrapingitems(driver, hippodromes, ratings, end_xpath_ratings)

    # Scraping of the countries.
    for ind in range(1, (len(hippodromes)+1)):
        countries.append('')
        countries.append('')
        countries.append('')
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
                country = country_string.get_attribute('title')
                countries.append(country)
            except:
                countries.append('')

    # Scraping of the horse names.
    end_xpath_horses = ']/div[3]'
    scrapingitems(driver, hippodromes, horses, end_xpath_horses)

    # Scraping of the names of the jockeys and the trainers.
    end_xpath_jockeys_trainers = ']/div[4]'
    scrapingitems(driver, hippodromes, jockeys_trainers, 
        end_xpath_jockeys_trainers)

    # Scraping of the age.
    end_xpath_age = ']/div[5]'
    scrapingitems(driver, hippodromes, lst_age, end_xpath_age)

    # Scraping of the weights.
    end_xpath_weights = ']/div[6]'
    scrapingitems(driver, hippodromes, weights, end_xpath_weights)

    # Scraping of the traveled distances.
    end_xpath_traveled_distances = ']/div[7]'
    scrapingitems(driver, hippodromes, traveled_distances, 
        end_xpath_traveled_distances)

    # Scraping of the comments about the each way bets.
    for ind in range(1, (len(hippodromes)+1)):
        bet_comments.append('')
        bet_comments.append('')
        bet_comments.append('')
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
                str_comments = (bet_comment_1 + '    ')
            except:
                bet_comment_1 = ''
                str_comments = (bet_comment_1 + '    ')
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
                str_comments = str_comments + bet_comment_2
                str_comments.strip()
                bet_comments.append(str_comments)
            except:
                bet_comment_2 = ''
                str_comments = str_comments + bet_comment_2
                str_comments.strip()
                bet_comments.append(str_comments)

    # Scraping of the each way bets.
    end_xpath_each_way_bets = ']/div[8]/span'
    scrapingitems(driver, hippodromes, each_way_bets, end_xpath_each_way_bets)

    # Scraping of the comments about the winners.
    for ind in range(1, (len(hippodromes)+1)):
        winner_comments.append('')
        winner_comments.append('')
        winner_comments.append('')
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
                str_winner_comments = (winner_comment_1 + '    ')
            except:
                winner_comment_1 = ''
                str_winner_comments = (winner_comment_1 + '    ')
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
                str_winner_comments = str_winner_comments +\
                    winner_comment_2
                str_winner_comments.strip()
                winner_comments.append(str_winner_comments)
            except:
                winner_comment_2 = ''
                str_winner_comments = str_winner_comments +\
                    winner_comment_2
                str_winner_comments.strip()
                winner_comments.append(str_winner_comments)

    # Scraping of the winners.
    end_xpath_winners = ']/div[9]/span'
    scrapingitems(driver, hippodromes, winners, end_xpath_winners)

    # Add lists with the scraped data to the dictionary in the correct 
    # order.
    dict_races['Hippodrome'] = lst_hippodromes
    dict_races['Start time'] = start_times
    dict_races['Racing name and data'] = names_data
    dict_races['Rating'] = ratings
    dict_races['Country'] = countries
    dict_races['Horse'] = horses
    dict_races['Jockey/Trainer'] = jockeys_trainers
    dict_races['Age'] = lst_age
    dict_races['Weight'] = weights
    dict_races['Traveled distance'] = traveled_distances
    dict_races['Bet comment'] = bet_comments
    dict_races['Each way bet'] = each_way_bets
    dict_races['Winner comment'] = winner_comments
    dict_races['Winner'] = winners

    # Creating of the frame for the data.
    df_res = pd.DataFrame(dict_races)

    # Saving of the properly formatted data to the csv file. The date 
    # and the time of the scraping are hidden in the file name.
    name_of_file = lambda: "horseracing{}.csv".format(time.strftime(\
        "%Y%m%d-%H.%M.%S"))
    df_res.to_csv(name_of_file(), encoding="utf-8")

finally:
    driver.quit()