"""
This file contains the main logic of the project - Link Preview API
"""
import re
import logging
from typing import Union
import base64
import requests
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup

LOGGING_META_ATTRIBUTES = '%(filename)s:%(lineno)d: %(funcName)s (%(message)s)\n'

logging.basicConfig(
            format = '[%(levelname)s] %(asctime)s\n' + LOGGING_META_ATTRIBUTES,
            datefmt = '%d-%b-%y %H:%M:%S',
            filename = "link_preview_log_data.log",filemode = "w")

app = FastAPI()

def format_url(url: str) -> bool:
    """
    Check url contains "://" using regex
    if true then check the protocol is http or https using regex
    other than http or https are like ftp
    """
    if len(url) > 3:
        if re.search(r'://', url):
            if re.search(r'^http(s)?://', url):
                return url
            logging.error("URL is not in a proper format -> %s", str(url))
            return False
        return 'http://' + str(url)
    logging.error("URL is too short!")
    return False

def extract_domain_url(any_url: str) -> str:
    """
    Extract domain name from any url
    """
    domain_name = re.search(r'^(?:http(s)?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', any_url)
    return domain_name.group(2)

def get_title(soup_object):
    """
    Get title from soup object
    Look title in Basic Meta Tags first and then OpenGraph Meta Tags
    """
    title = soup_object.find('title')
    if title:
        return title.text
    title = soup_object.find("meta", {"property": "og:title"})
    if title:
        return title.get('content')
    title = soup_object.find("meta", {"name": "apple-mobile-web-app-title"})
    if title:
        return title.get('content')
    title = soup_object.find("meta", {"property": "og:site_name"})
    if title:
        return title.get('content')
    return False

def get_decription(soup_object):
    """
    Get description from soup object
    """
    description = soup_object.find("meta", {"name": "description"})
    if description:
        return description.get('content')
    description = soup_object.find("meta", {"property": "og:description"})
    if description:
        return description.get('content')
    return False

def make_image_url(requested_url = None, image_url = None):
    """
    Make image url from relative url
    """
    if not re.search(r'^http(s)?://', image_url):
        domain_from_requested_url = "http://" + extract_domain_url(requested_url)
        if image_url.startswith("//"):
            image_url = "http:" + image_url
            return image_url
        if image_url.startswith("/"):
            image_url = domain_from_requested_url + image_url
            return image_url
        if image_url.startswith("./"):
            image_url = domain_from_requested_url + image_url[1:]
            return image_url
        if image_url.startswith("../"):
            image_url = domain_from_requested_url + image_url[2:]
            return image_url
        image_url = domain_from_requested_url + "/" + image_url
        return image_url
    return image_url

def get_image(soup_object, requested_url):
    """
    Get image from soup object
    Look image in Basic Meta Tags first and then OpenGraph Meta Tags
    """
    try:
        image = soup_object.find("link", {"rel": "apple-touch-icon"})
        if image:
            image_url = make_image_url(requested_url, image.get('href'))
            return image_url
        image = soup_object.find("meta", {"property": "og:image"})
        if image:
            image_url = make_image_url(requested_url, image.get('content'))
            return image_url
        image = soup_object.find("link", {"rel": "shortcut icon"})
        if image:
            image_url = make_image_url(requested_url, image.get('href'))
            return image_url
        image = soup_object.find("link", {"rel": "icon"})
        if image:
            image_url = make_image_url(requested_url, image.get('href'))
            return image_url
        final_domain = "http://" + extract_domain_url(requested_url) + '/favicon.ico'
        favicon_response = requests.get(final_domain, timeout = 60)
        if favicon_response.status_code == 200:
            return final_domain
        return False
    except Exception as error_msg:
        logging.error("%s", str(error_msg))
        return False

def get_image_bytes(image_url):
    """
    Get image bytes from image url
    """
    b64_img = False
    try:
        data = requests.get(image_url, timeout = 60)
        if data.status_code == 200:
            b64_img = base64.b64encode(data.content).decode()
    except Exception as error_msg:
        logging.error("%s", str(error_msg))
        b64_img = False
    return b64_img

def check_url_reqests_module_bs4(requested_url):
    """
    Check URL using requests module and BeautifulSoup
    """
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    #                   AppleWebKit/537.36 (KHTML, like Gecko) \
    #                   Chrome/103.0.0.0 Safari/537.36'
    #     }
    try:
        response = requests.get(requested_url, timeout = 60)
        soup = BeautifulSoup(response.text, features = "html.parser")
        title = get_title(soup)
        description = get_decription(soup)
        image = get_image(soup, requested_url)
        image_bytes = get_image_bytes(image)
        return {
            'title': title,
            'description': description,
            'image': image_bytes,
        }
    except Exception as error_msg:
        logging.error("%s", str(error_msg))
        return False

@app.get("/")
def home_page():
    """
    Home Page
    """
    return {
        'message': 'Welcome to LinkPreview API',
        'github': "https://github.com/4akhilkumar/LinkPreview"
    }

class URL(BaseModel):
    """
    URL Model
    """
    url: Union[str, None] = None

@app.post("/link_preview/")
async def link_preview(url_ref: URL):
    """
    Main Function
    """
    try:
        formated_url = format_url(url_ref.url)
        if formated_url is not False:
            link_preview_data = check_url_reqests_module_bs4(formated_url)
            if link_preview_data is not False:
                return {
                    "title": link_preview_data['title'],
                    "description": link_preview_data['description'],
                    "image": link_preview_data['image']
                }
            return {"msg": "Connection Time out"}
        return {"msg": "Can't process URL"}
    except Exception as error_msg:
        logging.error("%s", str(error_msg))
        return home_page()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
