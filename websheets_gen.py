#!/usr/bin/env python
# coding: utf-8

# In[10]:


#!/usr/bin/env python
# coding: utf-8
"""
This script aims to work for creation of a lowdefy yaml from excel sheet
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


# script defaults
EXCEL_LOCAL_NAME = "websheets.xlsx"

# default WebSheet to get values from, if GOOGLE_SHEETS_URL env is not set
DEFAULT_EXCEL_URL = "https://drive.google.com/file/d/1B3Ij5E1oboOphkFOB_lFF8rMUF-T_-Sj/"

# gets GOOGLE_SHEETS_URL env variable or defaults to the above LINK
URL_TO_DOWNLOAD = os.getenv("GOOGLE_SHEETS_URL", DEFAULT_EXCEL_URL)

# root folder for all templates
TEMPLATES_DIR = "templates/"

# root folder for all Lowdefy YAML's
# or
# dir for all YAML's generated from this script
OUTPUT_DIR = "output/"

# change
LOWDEFY_VERSION = "3.18.0"

# all items in "lower" case
VERTICAL_MENUS = ["layout", "menuitems", "social"]


def get_jinja_dict(
        excel_loc="",
        xl_engine="openpyxl",
        vertical_menus=False,
        sheet="Layout"):
    """
    converts given excel sheet into dict/json
    groups content for Layout
    """
    data_frame = pd.read_excel(
        excel_loc,
        engine=xl_engine,
        sheet_name=sheet)
    # if it is a layout file, return as it is
    # else, read the rows and map to them as a dictionary
    if vertical_menus:
        ret_obj = {}
        for index, row in data_frame.iterrows():
            #             print(row)
            try:
                ret_obj.update({str(row[0]).strip(): str(row[1]).strip()})
            except Exception as error:
                print(index, error)
        return ret_obj
    else:
        # rename Pandas columns to lower case
        data_frame.columns = data_frame.columns.str.lower()
        return data_frame.to_dict(orient='records')


def make_lowdefy_pages(templates_dir, output_dir, excel_loc):
    """
    generates Lowdefy pages, all but the homepage.
    """
    #   get dict for making lowdefy layout
    all_layout_config = get_jinja_dict(
        excel_loc, sheet="Home", vertical_menus=True)

    #   placeholder for all featured posts
    all_featured = {}

    #   update footer with time
    all_layout_config["footer_note"] = "Updated at " + \
        str(datetime.now(timezone('UTC'))).split(".")[0] + "  UTC"

#     pprint(get_jinja_dict(
#         excel_loc, sheet="Menu", vertical_menus= True))
    # being read from a different sheet but put into old
    all_layout_config["menuitem"] = get_jinja_dict(
        excel_loc, sheet="Menu", vertical_menus=True)

    all_layout_config["social"] = get_jinja_dict(
        excel_loc, sheet="Social", vertical_menus=True)

    pprint(all_layout_config)

    for page in all_layout_config["menuitem"].keys():
        try:
            posts = get_jinja_dict(
                excel_loc, sheet=page.capitalize())
            featured = []
            pinned = []
            count = 0
            all_posts_without_pinned = []
            for post in posts:
                count += 1
                abouts = {}
                for keys_about in post.keys():
                    if "extra_" in keys_about:
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
                pprint(post)
            all_featured.update({page.capitalize(): featured})

            with open(r'{}/post.yaml'.format(templates_dir)) as file:
                home_list = file.read()
                print("reading file")
                j2_template = Environment(
                    loader=FileSystemLoader("templates/")).from_string(home_list)
                open("{}/{}.yaml".format(output_dir,
                                         page),
                     "w+").write(j2_template.render(title=page,
                                                    all_layout_config=all_layout_config,
                                                    posts=all_posts_without_pinned,
                                                    pinned=pinned))

        except Exception as error_generic:
            print(
                "Error",
                error_generic,
                "\nDid you forget to include a page which is mentioned in the `menuitems` ?")
            open("{}/{}.yaml".format(OUTPUT_DIR, page), "w+")
#     pprint(all_featured)
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
        gdown.download(url, output, quiet=False)

    except Exception as error_generic:
        print(
            "Could not download the file. Please recheck the file/connection/url\n",
            error_generic)


try:
    download_excel(URL_TO_DOWNLOAD, EXCEL_LOCAL_NAME)
    make_lowdefy_pages(TEMPLATES_DIR, OUTPUT_DIR, EXCEL_LOCAL_NAME)

except Exception as error_generic:
    print("Unexpected error occured", error_generic)
    sys.exit(0)


# In[ ]:


# In[ ]:


# In[ ]:
