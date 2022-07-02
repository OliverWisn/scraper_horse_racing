# Scraper to scrap the web page https://www.horseracing24.com/ .

## Motivation:
Scraping of the website.

## Requirements: 
- python 3.10 
- For the usage of the script "scraper_horse_racing_tor.py" you must 
  have to install the Tor Browser (https://www.torproject.org/). You 
  also need to validate the paths in the torexe variable and 
  the profile variable.
- Firefox and geckodriver installed. Add the path for Firefox and 
  geckodriver to the PATH in windows, if they are not there.   (https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers).
- rest in requirements.txt .

## Remarks:
- I made this script so that the master branch had always 
  the functioning code. 
- To run the script you must run the file 
  "scraper_horse_racing_tor.py" or "scraper_horse_racing.py". 
  Both scripts do the same. The only difference is their coding style 
  and the support for Firefox instead of Tor.
- The scrapers only scrape the data from the main page 
  https://www.horseracing24.com/  .
- While the script "scraper_horse_racing_tor.py" is running, two tor 
  browser windows are opened. The first is with the tor network open 
  browser. The second one downloads the scraped website. The script 
  itself closes the window with the scrapped website, but does not 
  close the first window by itself. The first window must be closed 
  manually to complete the script execution.
- The script "scraper_horse_racing.py" is written in the functioning 
  style without using the tor network. It operates Firefox completely 
  automatically without user interaction. The browser is opened in 
  the headless mode, which means that the user cannot see its opening.
- Due to the behavior of the website, it is sometimes necessary to 
  run the program several times to fully scrape the website.

## Script Summary:
After you run the script, you must wait for the programm to finish. In 
the directory where the script file is located, a csv file with a name 
will appear, e.g. "horseracing20220111-10.27.30". In the file 
horseracing20220111-10.27.30.csv the exact date and time of the scraping 
is saved in the name. When you load the data from the csv file into 
Excel 2019, the following data layout appears:

<img src="https://github.com/OliverWisn/scraper_horse_racing/blob/master/image/demo_1.jpg" width=1000>

## Version:
This is version 2.00 of the scraper.
