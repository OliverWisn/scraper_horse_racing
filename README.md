# Scraper to scrap the web page https://www.horseracing24.com/ .

## Motivation:
Scraping of the website.

## Requirements: 
- python 3.10 
- Tor Browser installed (https://www.torproject.org/). You also need to validate the paths in the torexe variable and the profile variable.
- Firefox and geckodriver installed. Add the path for Firefox and geckodriver to the PATH in windows, if they are not there. (https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers).
- rest in requirements.txt .

## Remarks:
- I made this script so that the master branch had always 
  the functioning code. 
- To run the script you must run the file "horse_racing.py". 
- The scraper only scrapes the data from the main page 
  https://www.horseracing24.com/

## Script Summary:
After you run the script, you must wait for the programm to finish. In 
the directory where the script file is located, a csv file with a name 
will appear, e.g. "horseracing20220111-10.27.30". In the file 
horseracing20220111-10.27.30.csv the exact date and time of the scraping 
is saved in the name. When you load the data from the csv file into 
Excel 2019, the following data layout appears:

## Version:
This is version 1.00 of the scraper.
