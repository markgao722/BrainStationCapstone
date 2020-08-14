import WebScrape
import EnergyAPI
import CleanHTML


"""
Mark Gao - Capstone Project 2020.
Module X of X.
SUBMISSION SAMPLE. This is the order in which all functions should be run by someone seeking to
replicate the experiment for the first time on your own machine. Please remember to adjust constants
on this page as needed.
"""


# === Constants ===============================================================
root = "C:/Users/Mark/Documents/BS-CAPSTONE/BrainStationCapstone"

htmlfiles = ["data-FT",
             "data-Twitter",
             ]

classes = ["bull", "bear", "neutral"]
# =============================================================================


samples = CleanHTML.associate_dates(root, htmlfiles, classes)
sample = samples['10-Oil-Forces-US-Drilling-Giant-To-File-For-Bankruptcy.html']
print(type(sample))
print(sample)



#links = WebScrape.scrape_oilprice(pgs=54)
#WebScrape.download_links(links, "C:/Users/Mark/Desktop/test-data")
# Last download:
if __name__ == '__main__':
	pass
