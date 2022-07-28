from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import Union
import re
from bs4 import BeautifulSoup
import requests
import base64

app = FastAPI()

def format_URL(url):
    # checl url contains "://" using regex
    if re.search(r'://', url):
        # if true then check the protocol is http or https  using regex
        if re.search(r'^http(s)?://', url):
            return url
        else:
            return False
    else:
        return 'http://' + url

def valid_URL(formatedURL):
    if re.search(r'^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$', str(formatedURL)):
        return True
    else:
        return False

def get_title(soup_object):
    try:
        # Look title in Basic Meta Tags first and then OpenGraph Meta Tags
        title = soup_object.find('title')
        if title:
            return title.text
        else:
            title = soup_object.find("meta", {"property": "og:title"})
            if title:
                return title.get('content')
            else:
                title = soup_object.find("meta", {"name": "apple-mobile-web-app-title"})
                if title:
                    return title.get('content')
                else:
                    title = soup_object.find("meta", {"property": "og:site_name"})
                    if title:
                        return title.get('content')
                    else:
                        return False
    except Exception as e:
        return False

def get_decription(soup_object):
    try:
        description = soup_object.find("meta", {"name": "description"})
        if description:
            return description.get('content')
        else:
            description = soup_object.find("meta", {"property": "og:description"})
            if description:
                return description.get('content')
            else:
                return False
    except Exception as e:
        return False

def get_image(soup_object, requestedURL):
    try:
        image = soup_object.find("link", {"rel": "apple-touch-icon"})
        if image:
            if image.get('href').startswith("/"):
                if requestedURL.endswith('/'):
                    return requestedURL + image.get('href')[1:]
                else:
                    return requestedURL + image.get('href')
            return image.get('href')
        else:
            image = soup_object.find("meta", {"property": "og:image"})
            if image:
                if image.get('content')[0] == '/':
                    return requestedURL + image.get('content')
                return image.get('content')
            else:
                image = soup_object.find("link", {"rel": "shortcut icon"})
                if image:
                    if image.get('href').startswith("/"):
                        return requestedURL + image.get('href')[1:]
                    return image.get('href')
                else:
                    image = soup_object.find("link", {"rel": "icon"})
                    if image:
                        if image.get('href').startswith("/"):
                            if requestedURL.endswith('/'):
                                return requestedURL + image.get('href')[1:]
                            else:
                                return requestedURL + image.get('href')
                        return image.get('href')
                    else:
                        try:
                            if requestedURL.endswith('/'):
                                favicon = 'favicon.ico'
                            else:
                                favicon = '/favicon.ico'
                            favicon_response = requests.get(requestedURL + favicon, timeout=30)
                            if favicon_response.status_code == 200:
                                return requestedURL + favicon
                            else:
                                return False
                        except Exception as e:
                            print("Favicon Exception",e)
                            return False

    except Exception as e:
        print("Image Exception",e)
        return False

def get_image_bytes(image_url):
    b64_img = False
    data = requests.get(image_url, timeout=30)
    if data.status_code == 200:
        b64_img = base64.b64encode(data.content).decode()
    return b64_img

def check_URL_reqests_module_BS4(requestedURL):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    #     }
    try:
        response = requests.get(requestedURL, timeout=30)
        soup = BeautifulSoup(response.text, features="html.parser")
        title = get_title(soup)
        description = get_decription(soup)
        image = get_image(soup, requestedURL)
        image_bytes = get_image_bytes(image)

        return {
            'title': title, 
            'description': description, 
            'image': image_bytes,
        }
    except Exception as e:
        print(e)
        return False

@app.get("/")
def home_page():
    return {
        'message': 'Welcome to LinkPreview API',
        'github': "https://github.com/4akhilkumar/LinkPreview" 
    }

@app.get("/link_preview")
def link_preview(url: Union[str, None] = None):
    formatedURL = format_URL(url)
    if format_URL(url) is not False:
        validURL = valid_URL(formatedURL)
        if validURL is True:
            linkPreview_data = check_URL_reqests_module_BS4(formatedURL)
            if linkPreview_data is not False:
                return {
                    "title": linkPreview_data['title'],
                    "description": linkPreview_data['description'],
                    "image": linkPreview_data['image']
                }
            else:
                return {"msg": "Connection Time out"}
        else:
            return {"msg": "Invalid URL"}
    else:
        return {"msg": "Can't process URL"}

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)