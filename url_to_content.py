from trafilatura import fetch_url, extract
import re
import urllib.parse
import requests
import os
import logging


def is_valid_url(url):
    if url is None:
        return False

    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    p = re.compile(regex)
    if re.search(p, url):
        return True
    else:
        return False


def url_to_content(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.hostname.endswith('youtube'):
            return youtube_url_to_content(parsed_url)
        else:
            return article_url_to_content(url)
    except Exception as e:
        logging.error(e)
        return 'Something went wrong, when parsing the url'


def article_url_to_content(url):
    try:
        html = fetch_url(url)
        result = extract(html)
        return result
    except Exception as e:
        logging.error(e)


def youtube_url_to_content(url):
    try:
        video_id = urllib.parse.parse_qs(url.query).get('v')

        api_endpoint = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'key': f"{os.getenv('GOOGLE_API_KEY')}",
            'part': 'snippet',
            'id': video_id[0]
        }
        response = requests.get(api_endpoint, params=params)

        data = response.json()

        video_info = data['items'][0]['snippet']

        title = video_info['title']
        channel = video_info['channelTitle']
        description = video_info['description']

        return f"{title} - {channel} - {description}"
    except Exception as e:
        logging.error(e)
