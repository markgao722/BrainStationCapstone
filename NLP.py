import CleanHTML

from sklearn.feature_extraction.text import CountVectorizer


"""
Mark Gao - Capstone Project 2020.
Module 3 of X.
Use this module to fit an NLP model.
"""


# === Constants ===============================================================
root = "C:/Users/Mark/Documents/BS-CAPSTONE/BrainStationCapstone"

htmlfiles = ["data-FT",
             "data-Twitter",
             ]

classes = ["bull", "bear", "neutral"]
# =============================================================================


text_collection = CleanHTML.main(root, htmlfiles, classes)

words = CountVectorizer()
word_vector = words.fit_transform(text_collection)
print(word_vector)

