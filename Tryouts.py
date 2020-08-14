import WebScrape
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
print(samples['Shipbroker Clarkson boosted by rush to store cheap oil _ Financial Times.html'])

#links = WebScrape.scrape_oilprice(pgs=54)
#WebScrape.download_links(links, "C:/Users/Mark/Desktop/test-data")
# Last download:
if __name__ == '__main__':
	pass
