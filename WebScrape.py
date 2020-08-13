import requests

from bs4 import BeautifulSoup

"""
Mark Gao - Capstone Project 2020.
Module 1 of X.
This module scrapes selected websites and saves relevant webpages as html files.
"""


sites = ["https://www.investing.com/commodities/crude-oil-news/",  # unknown max pgs
         "https://oilprice.com/Latest-Energy-News/World-News/",  # 577 pgs dating to 2011
         "https://www.worldoil.com/topics/production",  # unknown max pgs
         ]

url = "https://oilprice.com/Latest-Energy-News/World-News/"

response = requests.get(url)
soup = BeautifulSoup(response.text)
titles = soup.find_all('div', class_='categoryArticle__content')

print(len(titles))
