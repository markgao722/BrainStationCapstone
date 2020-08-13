#import os
#from NLP import root, htmlfiles, classes
import WebScrape

links = WebScrape.scrape_oilprice(pgs=1)
WebScrape.download_links(links, "C:/Users/Mark/Desktop/test-data")
