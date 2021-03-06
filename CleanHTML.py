import os
import re
from bs4 import BeautifulSoup
from datetime import datetime


"""
Mark Gao - Capstone Project 2020.
Module 3 of 5.
This module defines helper functions to gather files from your project directory and prepare them into Python objects.
"""


def main(root: str, data: list, classes: list)-> dict:
    """
    Transforms every file (typically HTML) within the file structure given to strings.
    The resulting strings, each representing a file, are loaded into a dictionary where the key is the filename.
    :param root:    str, the top-level folder containing the data folders. If only one data source exists (e.g. Twitter
                    data), then let this be one level up from working directory.
    :param folders: list(str), the folder or a list of folders which will contain a folder for each class type.
    :param classes: list(str), the list of folders, each which contains data of a certain class.
    :return:        dict, with keys: file name and values: string-representation of HTML
    """
    output = {}

    # Construct a path to a single html file with a triple for loop. Adjust your folder structure if NOT in 3 layers.
    for data_folder in data:
        for data_class in classes:
            print(f"Files in /{data_folder}/{data_class}: {len(os.listdir(root + '/' + data_folder + '/' + data_class))}")

            files = os.listdir(root + "/" + data_folder + "/" + data_class)

            for data_item in files:
                print(f"Parsing file: {data_item}...")

                # At this level of the for loop, each html file is accessed as filename (str).
                filename = root + '/' + data_folder + '/' + data_class + '/' + data_item

                # Open each html and parse with Beautifulsoup.
                file = open(filename, 'r', encoding='utf8')
                html = file.read()
                soup = BeautifulSoup(html)
                tag_instances = soup.find_all('p')

                # Note soup.find_all() returns a list of strings, but the html tagging such as <p> or <div> remain.
                # Access the .text attribute to exclude this.
                textblob = ""
                for tag in tag_instances:
                    textblob += tag.text

                output[data_item] = textblob

    return output


def associate_dates(root: str, data: list, classes: list):
    """
    For each file in the given directory, find the date of publication within the HTML and use it as the value in the
        output dictionary. The output dictionary's keys are the file names.
    :param root:    str, the top-level folder containing the data folders. If only one data source exists (e.g. Twitter data),
                    then let this be one level up from working directory.
    :param data:    list(str), the folder or a list of folders which will contain a folder for each class type.
    :param classes: list(str), the list of folders, each which contains data of a certain class.
    :return:        dict, with keys: file name (str) and values: published date (datetime obj)
    """
    output = {}

    # Construct a path to a single html file with a triple for loop. Adjust your folder structure if NOT in 3 layers.
    for data_folder in data:
        for data_class in classes:
            print(
                f"Files in /{data_folder}/{data_class}: {len(os.listdir(root + '/' + data_folder + '/' + data_class))}")

            files = os.listdir(root + "/" + data_folder + "/" + data_class)

            for data_item in files:
                print(f"Parsing file: {data_item}...")

                # At this level of the for loop, each html file is accessed as filename (str).
                filename = root + '/' + data_folder + '/' + data_class + '/' + data_item

                # Open each html and parse with Beautifulsoup.
                file = open(filename, 'r', encoding='utf8')
                html = file.read()
                soup = BeautifulSoup(html)
                content = soup.find_all('span', class_="article_byline")
                span = content[0]

                # Manipulate the text to get a standardized date format
                string = span.text.split(' - ')[1]  # ---> not sure if this will work for every article!!
                string2 = re.search("[A-z]+\s[0-9]+,\s[0-9]{4}", string)
                string3 = string2.group(0)

                date = datetime.strptime(string3, "%b %d, %Y").date()

                output[data_item] = date
    return output
