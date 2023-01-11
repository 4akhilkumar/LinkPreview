# Introduction

## What is LinkPreview?
LinkPreview is an API that provides detailed info. of almost every website. It is built using FastAPI & Beautiful Soup

## How does it work?
When you send us a link, we fetch it in our servers, format it and validate it, we will then send you back a preview of what's behind the link.

## Why is it useful?
LinkPreview summarize the contents of the URL and display the name of the given website, an image and a description of the website's content.

It's difficult to undestand a string of undecipherable characters like `https://youtu.be/dQw4w9WgXcQ`. LinkPreview provides you detailed website information - title, preview image, and short description in JSON format by default for any given URL

## API Endpoints
We provide both HTTP and HTTPS endpoints for our service:
| Endpoint | HTTP Method |
| -------- | ----------- |
| http://rinjo.herokuapp.com/link_preview/ | POST |
| https://rinjo.herokuapp.com/link_preview/ | POST |

## Response Fields

| Name | Type | Description | Example Response |
| -------- | ----------- | -------- | ----------- |
| title | string / boolean | Website title | Google |
| description | string / boolean | Description  | Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for. |
|image | bytes - base64 / boolean | Preview image URL | AAABAAIAEBAAAAEAIABoBAAAJgAAACAgAAABACAAqBAAAI4EAAAoAAA |
| msg | string | Response of the URL | "Invalid URL" or "Can't process URL" or "Connection Time out" |

## Note - 1
    Example Response of bytes - base64 is just sample format of the image base64 encoded. If title, description or image return false then it means our API could not fetch the data from the URL.

## Examples

## jQuery
### POST Request using Ajax
```
$.ajax({
    type: 'post',
    contentType: "application/json",
    url: "https://rinjo.herokuapp.com/link_preview/",
    data: JSON.stringify({
        url: "https://www.google.com"
    }),
    success: function(data) {            
        console.log(data);
    },
    error: function(data) {
        console.log(data);
    }
});
```

## POST Request using Python
```
import requests

API_URL = "http://rinjo.herokuapp.com/link_preview/"
target = "https://www.google.com"
try:
    response = requests.post(API_URL, json={'url': target}, timeout=60)
    print(response.json())
except Exception as e:
    print(e)
```

### JSON Response
```
{
    "title": "Google",
    "description": "Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for.",
    "image": "AAABAAIAEBAAAAEAIABoBAAAJgAAACAgAAABACAAqBAAAI4EAAAoAAA"
}
```

## Note - 2
    Example Response of bytes - base64 is just sample format of the image base64 encoded

## Live Demo
[LinkPreview API Live Demo](https://4akhilkumar.github.io/LinkPreview/index.html)

## Full Frontend Example - Codepen
[LinkPreview - Codepen](https://codepen.io/4akhilkumar/pen/PoRJmQm)

## How to Setup in your local machine?
- Clone the repository using `git clone https://github.com/4akhilkumar/LinkPreview.git`
- Install the [Python](https://www.python.org/downloads/) 3.8 or above

### For Windows       
1. Install the [Virtualenv](https://pypi.org/project/virtualenv/) using `pip install virtualenv`     
2. Create a virtual environment using `python -m venv venv`      
3. Activate the virtual environment using `venv\Scripts\activate`        
4. Install the requirements using `python -m pip install -r requirements.txt`

### For Linux
1. Install the [Virtualenv](https://pypi.org/project/virtualenv/) using `pip3 install virtualenv`     
2. Create a virtual environment using `python3 -m venv venv`     
3. Activate the virtual environment using `source venv/bin/activate`     
4. Install the requirements using `python3 -m pip install -r requirements.txt`

- If requirements installation failed, try these commands as per your OS:  
`python -m pip install fastapi uvicorn[standard] beautifulsoup4 requests`

- Run the server using `uvicorn <file_name>:app --reload`
