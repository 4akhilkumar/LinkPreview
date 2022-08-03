from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from typing import Union
import re
from bs4 import BeautifulSoup
import requests
import base64

app = FastAPI()

def format_URL(url):
    try:
        # checl url contains "://" using regex
        if re.search(r'://', url):
            # if true then check the protocol is http or https using regex
            if re.search(r'^http(s)?://', url):
                return url
            else: # other than http or https are like ftp
                return False
        else:
            return 'http://' + url
    except Exception as e:
        print("Format URL Exception",e)
        return False

def valid_URL(formatedURL):
    try:
        if re.search(r'^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$', str(formatedURL)):
            return True
        else:
            return False
    except Exception as e:
        print("Valid URL Exception",e)
        return False

def extract_domain_url(any_url = None):
    domain_name = re.search(r'^(?:http(s)?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', any_url)
    return domain_name.group(2)

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

def make_image_url(requestedURL = None, imageURL = None):
    if not re.search(r'^http(s)?://', imageURL):
        domainFromrequestedURL = "http://" + extract_domain_url(requestedURL)
        if(imageURL.startswith("//")):
            imageURL = "http:" + imageURL
            return imageURL
        elif imageURL.startswith("/"):
            imageURL = domainFromrequestedURL + imageURL
            return imageURL
        elif imageURL.startswith("./"):
            imageURL = domainFromrequestedURL + imageURL[1:]
            return imageURL
        elif imageURL.startswith("../"):
            imageURL = domainFromrequestedURL + imageURL[2:]
            return imageURL
        else:
            imageURL = domainFromrequestedURL + "/" + imageURL
            return imageURL
    else:
        return imageURL

# imageURL = format_URL(extract_domain_url(requestedURL)) + imageURL

def get_image(soup_object, requestedURL):
    try:
        image = soup_object.find("link", {"rel": "apple-touch-icon"})
        if image:
            imageURL = make_image_url(requestedURL, image.get('href'))
            return imageURL
        else:
            image = soup_object.find("meta", {"property": "og:image"})
            if image:
                imageURL = make_image_url(requestedURL, image.get('content'))
                return imageURL
            else:
                image = soup_object.find("link", {"rel": "shortcut icon"})
                if image:
                    imageURL = make_image_url(requestedURL, image.get('href'))
                    return imageURL
                else:
                    image = soup_object.find("link", {"rel": "icon"})
                    if image:
                        imageURL = make_image_url(requestedURL, image.get('href'))
                        return imageURL
                    else:
                        try:
                            favicon = '/favicon.ico'
                            final_domain = "http://" + extract_domain_url(requestedURL) + favicon
                            favicon_response = requests.get(final_domain, timeout=60)
                            if favicon_response.status_code == 200:
                                return final_domain
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
    try:
        data = requests.get(image_url, timeout=60)
        if data.status_code == 200:
            b64_img = base64.b64encode(data.content).decode()
    except Exception as e:
        print("Image Bytes Exception",e)
        b64_img = False
    return b64_img

def check_URL_reqests_module_BS4(requestedURL):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    #     }
    try:
        response = requests.get(requestedURL, timeout=60)
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
        print("IMAGE URL",e)
        return False

@app.get("/")
def home_page():
    return {
        'message': 'Welcome to LinkPreview API',
        'github': "https://github.com/4akhilkumar/LinkPreview" 
    }

class URL(BaseModel):
    url: Union[str, None] = None

@app.post("/link_preview/")
async def create_item(url: URL):
    try:
        formatedURL = format_URL(url.url)
        if formatedURL is not False:
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
    except Exception as e:
        print("Main Func Exception",e)
        return home_page()


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