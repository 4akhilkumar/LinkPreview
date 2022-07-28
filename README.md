# Introduction

## What is LinkPreview?
LinkPreview is an API that provides detailed info. of almost every website. It is built using FastAPI & Beautiful Soup

## How does it work?
When you send us a link, we fetch it in our servers, format it and validate it, we will then send you back a preview of what's behind the link.

## Why is it useful?
LinkPreview summarize the contents of the URL and display the name of the given website, an image and a description of the website's content.

It's difficult to undestand a string of undecipherable characters like `https://youtu.be/dQw4w9WgXcQ`. LinkPreview provides you detailed website information - title, preview image, and short description in JSON format by default for any given URL


## Quick example

### Simple GET Request
```
https://rinjo.herokuapp.com/link_preview?url=https://www.google.com
```

### JSON Response
```
{
    "title": "Google",
    "description": "Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for.",
    "image": "https://www.google.com/logos/doodles/2022/celebrating-steelpan-6753651837108467.2-2xa.gif"
}
```

## API Endpoints
We provide both HTTP and HTTPS endpoints for our service:
| Endpoint | HTTP Method |
| -------- | ----------- |
| http://rinjo.herokuapp.com/link_preview?url=<YOUR_URL> | GET |
| https://rinjo.herokuapp.com/link_preview?url=<YOUR_URL> | GET |

## Query parameter
```
https://rinjo.herokuapp.com/link_preview?url=https://www.google.com
```

| Parameter | Description | Example | Required |
| -------- | ----------- | -------- | ----------- |
| url | URL to be previewed | https://www.google.com | Yes |

## Response Fields

| Name | Type | Description | Example Response |
| -------- | ----------- | -------- | ----------- |
| title | string / boolean | Website title | Google |
| description | string / boolean | Description  | Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for. |
|image | bytes - base64 / boolean | Preview image URL | https://www.google.com/logos/doodles/2022/celebrating-steelpan-6753651837108467.2-2xa.gif |
| msg | string | Response of the URL | "Invalid URL" or "Can't process URL" or "Connection Time out" |

### If title, description or image return false then it means our API could not fetch the data from the URL.

## Examples

## jQuery
### GET Request using Ajax
```
$.ajax({
    url: "https://rinjo.herokuapp.com/link_preview?url=https://www.google.com",
    type: 'GET',
    data : {},
    success: function(data) {            
        console.log(data);
    },
    error: function(data) {
        console.log(data);
    }
});
```

## GET Request using Python
```
import requests

API_URL = "http://rinjo.herokuapp.com/link_preview"
target = "https://www.google.com"
try:
    response = requests.get(API_URL, params={'url': target}, timeout=30)
    print(response.json())
except Exception as e:
    print(e)
```

## Full Frontend Example - Codepen
[LinkPreview - Codepen](https://codepen.io/4akhilkumar/pen/PoRJmQm)

## Output
![LinkPreview](https://raw.githubusercontent.com/4akhilkumar/LinkPreview/gh-pages/Screenshot%202022-07-27%20082644.jpg "LinkPreview")