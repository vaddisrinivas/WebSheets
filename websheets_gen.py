#!/usr/bin/env python
# coding: utf-8
"""
This is a sample doc string
"""


# import json
import os
import sys
from datetime import datetime
from pprint import pprint

from pytz import timezone
from jinja2 import Environment, FileSystemLoader

import pandas as pd
import gdown
# import requests


# script defaults
# excel_location = "Book1.xlsx"
EXCEL_LOCAL_NAME = "websheets.xlsx"
URL_TO_DOWNLOAD = os.environ["GOOGLE_SHEETS_URL"]
TEMPLATES_DIR = "templates/"
OUTPUT_DIR = "output/"


def get_jinja_dict(
        excel_loc="",
        xl_engine="openpyxl",
        filter_keys=[],
        sheet="Layout"):
    """
    converts given excel sheet into dict/json
    groups content for Layout
    """
    data_frame = pd.read_excel(excel_loc, engine=xl_engine, sheet_name=sheet)
    if sheet == "Layout":
        ret_obj = {}
        for word in filter_keys:
            ret_obj.update({word: {}})
        for index, row in data_frame.iterrows():
            if any(word in str(row[0]).strip() for word in filter_keys):
                for word in filter_keys:
                    if word in str(row[0]).strip():
                        ret_obj[word].update(
                            {str(row[0]).strip(): str(row[1]).strip()})
                        break
            else:
                ret_obj.update({str(row[0]).strip(): str(row[1]).strip()})
        return ret_obj
    else:
        # rename Pandas columns to lower case
        data_frame.columns = data_frame.columns.str.lower()
        return data_frame.to_dict(orient='records')


def make_lowdefy(templates_dir, output_dir, excel_loc):
    """
    generates all Lowdefy pages
    """
    #   get dict for making lowdefy layout
    all_layout_config = get_jinja_dict(
        excel_loc, sheet="Layout", filter_keys=[
            "social", "menuitem"])

    #   placeholder for all featured posts
    all_featured = {}

    #   update footer with time
    all_layout_config["footer_note"] = "Updated at " + \
        str(datetime.now(timezone('UTC'))).split(".")[0] + "  UTC"
    for page in all_layout_config["menuitem"].keys():
        try:
            print("Generating menuitem ", page.split("_")[1].capitalize())

            posts = get_jinja_dict(
                excel_loc, sheet=page.split("_")[1].capitalize())
            pprint(posts)
            featured = []
            pinned = []
            count = 0
            all_posts_without_pinned = []
            for post in posts:
                count += 1
                abouts = {}
                for keys_about in post.keys():
                    if "about_" in keys_about:
                        abouts.update(
                            {keys_about.split("_")[1]: post[keys_about]})
                    else:
                        continue
                post.update({"abouts": abouts})
                if str(post["featured"]).strip().lower() == "yes":
                    featured.append(post)
                if str(post["pinned"]).strip().lower() == "yes":
                    pinned.append(post)
                else:
                    all_posts_without_pinned.append(post)
            all_featured.update({page.split("_")[1].capitalize(): featured})

            with open(r'{}/post.yaml'.format(templates_dir)) as file:
                home_list = file.read()
                print("reading file")
                j2_template = Environment(
                    loader=FileSystemLoader("templates/")).from_string(home_list)
                open("{}/{}.yaml".format(output_dir,
                                         page.split("_")[1]),
                     "w+").write(j2_template.render(title=page.split("_")[1],
                                                    all_layout_config=all_layout_config,
                                                    posts=all_posts_without_pinned,
                                                    pinned=pinned))

        except Exception as error_generic:
            print(
                "Error",
                error_generic,
                "\nDid you forget to include a page which is mentioned in the `menuitems` ?")
            open("{}/{}.yaml".format(OUTPUT_DIR, page.split("_")[1]), "w+")
    pprint(all_featured)
    with open(r'templates/home.yaml') as file:
        home_list = file.read()
        j2_template = Environment(loader=FileSystemLoader(
            "templates/")).from_string(home_list)
        open("{}/lowdefy.yaml".format(output_dir),
             "w+").write(j2_template.render(all_layout_config=all_layout_config,
                                            all_featured=all_featured))


def download_excel(url_input, output):
    """
    Downloads excel from google
    """
    try:
        url = 'https://drive.google.com/uc?id={}'.format(
            url_input.split("/")[-2])
#         output = 'book_excel_download.xlsx'
        gdown.download(url, output, quiet=False)

    except Exception as error_generic:
        print(
            "Could not download the file. Please recheck the file/connection/url\n",
            error_generic)


try:
    download_excel(URL_TO_DOWNLOAD, EXCEL_LOCAL_NAME)
    make_lowdefy(TEMPLATES_DIR, OUTPUT_DIR, EXCEL_LOCAL_NAME)

except Exception as error_generic:
    print("Unexpected error occured", error_generic)
    sys.exit(0)
