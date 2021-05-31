#!/usr/bin/env python
# coding: utf-8

# In[11]:


# import yaml
from jinja2 import Environment, BaseLoader,FileSystemLoader
import json
import os
import subprocess
import pandas as pd
from pprint import pprint
from jinja2 import Template
from pytz import timezone
from datetime import datetime
import gdown
import requests


# script defaults
# excel_location = "Book1.xlsx"
excel_download_name = "websheets.xlsx"
url_to_download = os.environ["GOOGLE_SHEETS_URL"]
templates_dir="templates/"
output_dir="output/"

def get_jinja_dict(excel_loc="",xl_engine="openpyxl",filter_keys=[], split_word="_", sheet="Layout"):   
    """
    converts given excel sheet into dict/json 
    groups content for Layout
    """
    df = pd.read_excel(excel_loc,engine=xl_engine,sheet_name=sheet)
    if sheet=="Layout":
        ret_obj={}
        for word in filter_keys:
            ret_obj.update({word:{}})
        for index, row in df.iterrows():
            if any(word in str(row[0]).strip() for word in filter_keys):
                for word in filter_keys:
                    if word in str(row[0]).strip():
                        ret_obj[word].update({str(row[0]).strip():str(row[1]).strip()})
                        break
            else:
                ret_obj.update({str(row[0]).strip():str(row[1]).strip()})
        return ret_obj
    else:
        # rename Pandas columns to lower case
        df.columns= df.columns.str.lower()
        return df.to_dict(orient='records')
        
def make_lowdefy(templates_dir,output_dir,excel_loc):
    """
    generates all Lowdefy pages
    """
    #   get dict for making lowdefy layout 
    all_layout_config=get_jinja_dict(excel_loc,sheet="Layout", filter_keys=["social","menuitem"])

    #   placeholder for all featured posts
    all_featured={}

    #   update footer with time    
    all_layout_config["footer_note"]="Updated at "+str(datetime.now(timezone('UTC'))).split(".")[0]+"  UTC"

    for page in all_layout_config["menuitem"].keys():
        try:
            print("Generating menuitem ",page.split("_")[1].capitalize())

            posts=get_jinja_dict(excel_loc,sheet=page.split("_")[1].capitalize())
            featured=[]
            
            for post in posts:
                abouts={}
                if str(post["featured"]).strip().lower()=="yes":
                                    featured.append(post)
                for keys_about in post.keys():
                    if "about_" in keys_about:
                        abouts.update({keys_about.split("_")[1].capitalize():post[keys_about].capitalize()})
                    else:
                        continue
                post.update({"abouts":abouts})
                all_featured.update({page.split("_")[1].capitalize():featured})
            
            with open(r'{}/post.yaml'.format(templates_dir)) as file:
                home_list = file.read()
                print("reading file")
                j2_template = Environment(loader=FileSystemLoader("templates/")).from_string(home_list)
                open("{}/{}.yaml".format(output_dir,page.split("_")[1]),"w+").write(j2_template.render(title=page.split("_")[1],all_layout_config=all_layout_config,posts=posts,read_more=False,comment_yes=False)) 

        except Exception as e:
            print("Error",e,"\nDid you forget to include a page which is mentioned in the `menuitems` ?")
            open("{}/{}.yaml".format(output,page.split("_")[1]),"w+")

    with open(r'templates/home.yaml') as file:
        home_list = file.read()
        j2_template = Environment(loader=FileSystemLoader("templates/")).from_string(home_list)
        open("{}/lowdefy.yaml".format(output_dir),"w+").write(j2_template.render(all_layout_config=all_layout_config,all_featured=all_featured)) 

def download_excel(url_input,output):
    try:
        url = 'https://drive.google.com/uc?id={}'.format(url_input.split("/")[-2])
#         output = 'book_excel_download.xlsx'
        gdown.download(url, output, quiet=False)
        
    except Exception as e:
        print("Could not download the file. Please recheck the file/connection/url\n",e)

try:
    download_excel(url_to_download,excel_download_name)
    make_lowdefy(templates_dir,output_dir,excel_download_name)

except Exception as e:
    print("Unexpected error occured",e)
    exit(0)

