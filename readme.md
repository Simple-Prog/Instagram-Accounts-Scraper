## Script To Scrape Instagram & Facebook Account URLs From Given Sites

The script contains the main `scraper.py` that scrapes data from 30k+ sites using multithreaded requests.

The URLs to the sites from which the data is to be scraped are in `instagram_charities.xlsx` which is an excel file with multiple sheets.

Multiple routes of a single site are checked in case the account urls are not found on the home page.
