import requests
import urllib.request as url3request
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


def scrape_oilprice(url="https://oilprice.com/Latest-Energy-News/World-News/", pgs: int=1)-> list:
    """
    Scrapes several pages of oilprice.com's news section to give a list of urls that can be accessed later.
    Note the output is a list of urls (str), and not a bs4 or requests object, so a parser of some sort will be needed
        to access the html at some later point.
    :param url: str, web address to oilprice.com's news section.
    :param pgs: int, maximum number of pages to collect. Default 1; keep low when doing test scrapes.
    :return:    list, of links to web pages
    """
    print(f"Scraping oilprice.com news section...")
    files_scanned = 0
    files_downloaded = 0
    links = []

    # Loop through each page of the website's news section...
    for pg in range(1, pgs+1):
        if pg == 1:
            response = requests.get(url)
        else:
            response = requests.get(url + f"Page-{pg}.html")

        # Approx 20 articles per page are found under the categoryArticle class.
        soup = BeautifulSoup(response.text)
        titles = soup.find_all('div', class_='categoryArticle__content')
        # NOTE TO SELF: titles is bs4.element.Tag object but functions like soup (bs4.BeautifulSoup object)

        # Saves each article url into links as string.
        for t in titles:
            links.append(t.find('a')['href'])

        print(f"Articles on this page ({pg}): {len(titles)}")
        files_scanned += len(titles)

    print(f"Scraping complete! {pgs} pg(s) scraped, and {files_scanned} files scanned")

    return links
    # NOTE TO SELF: we know the page format is /World-News/Page-12.html so a general pagination function wasn't made


def scrape_worldoil(url="https://www.worldoil.com/topics/production", pgs=1)-> list:
    """
    Scrapes several pages of worldoil.com's news section to give a list of urls that can be accessed later.
    Note the output is a list of urls (str), and not a bs4 or requests object, so a parser of some sort will be needed
        to access the html at some later point.
    :param url: str, web address to worldoil.com's news section.
    :param pgs: int, maximum number of pages to collect. Default 1; keep low when doing test scrapes.
    :return:    list, of links to web pages
    """
    response = requests.get(url)

    for pg in range(1, pgs+1):
        pass

    # ---> refer to pages as ?page=2

    return []


def download_links(links: list, dir: str)-> None:
    """
    Using a list of urls to access web pages, download each page as an html file into the specified directory on the
    computer. The result will likely have no CSS but can be parsed using Python libraries.
    :param links:   list, containing url links to all the web pages to be downloaded.
    :param dir:     str, the path to the directory all html files will be downloaded to.
    :return:        None.
    """
    if dir[-1] == "/":
        print("Please input target dir without trailing / character.")
        return None

    # Open each web page...
    for url in links:
        response = url3request.urlopen(url)
        html = response.read()

        # Save the web page by writing all of its html content into a file of similar name at the target directory.
        name = url.replace("https://oilprice.com/Latest-Energy-News/World-News/", "")
        with open(dir + "/" + name, 'wb') as file:
            file.write(html)
            # NOTE TO SELF: overwrites if existing; won't create duplicates/errors

    print(f"Download complete! {len(links)} files downloaded at {dir}")

    return None
