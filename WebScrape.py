import requests

from bs4 import BeautifulSoup

"""
Mark Gao - Capstone Project 2020.
Module 1 of X.
This module scrapes selected websites and saves relevant webpages as html files.
"""


sites = ["https://www.investing.com/commodities/crude-oil-news/",  # unknown max pgs (BANNED FROM SCRAPING)
         "https://oilprice.com/Latest-Energy-News/World-News/",  # 577 pgs dating to 2011
         "https://www.worldoil.com/topics/production",  # unknown max pgs
         ]


def scrape_oilprice(url="https://oilprice.com/Latest-Energy-News/World-News/", pgs: int=3, dl=False, dir: str=None)-> None:
    """

    :param url: str, web address to oilprice.com's news section.
    :param pgs: int, maximum number of pages to collect. Default 3; keep low when doing test scrapes.
    :param dl:  bool, set to true to actually download all html files into dir.
    :param dir: str, the directory to download all html files into.
    :return:
    """
    print(f"Scraping oilprice.com news section...")
    files_scanned = 0
    files_downloaded = 0
    links = []

    # Loops through each page of the website's news section.
    for pg in range(1, pgs+1):

        if pg == 1:
            response = requests.get(url)
        else:
            response = requests.get(url + f"Page-{pg}.html")

        soup = BeautifulSoup(response.text)
        titles = soup.find_all('div', class_='categoryArticle__content')
        # NOTE TO SELF: bs4.element.Tag object but functions like soup (bs4.BeautifulSoup object)

        print(f"Articles on this page ({pg}): {len(titles)}")
        files_scanned += len(titles)

        # Saves each article url into links as string.
        for t in titles:
            links.append(t.find('a')['href'])

    print(f"Scraping complete! {pgs} pg(s) scraped, and {files_scanned} files scanned")

    if dl:
        pass

    return None
    # NOTE TO SELF: we know the page format is /World-News/Page-12.html so a general pagination function wasn't made.
