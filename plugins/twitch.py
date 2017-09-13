#!/bin/python3
# coding: utf-8

from urllib.parse import urlparse
from feedgenerator import Atom1Feed
from datetime import datetime
from requests import get

import re


# Returns True or False depending on if this
# plugin can handle the url passed as an argument
def check(url):
    parsed = urlparse(url)
    regex = re.compile('^/.+/videos/(all|uploads|past-broadcasts|highlights)')

    return "twitch.tv" in parsed.netloc and regex.match(parsed.path) is not None


# Takes a url to a page, and returns the query that the generate function wants
def query(url):
    # Example that simply gets the query string from the url passedA
    return urlparse(url).path


# Takes a query and returns a utf-8 encoded string containing the feed
def generate(query):
    # Parse query
    path_split = query.split('/')
    query_channel = path_split[1]
    query_type = path_split[3]

    # Get Client-ID
    global_js = get('https://web-cdn.ttvnw.net/global.js').text
    client_id = re.findall('clientID:"(.+?)"', global_js)[0]
    request_headers = {'Client-ID': client_id}

    # Get channel info
    json_channel = get('https://api.twitch.tv/kraken/channels/' + query_channel, headers=request_headers).json()

    # A title/name for the whole feed
    feed_title = json_channel['display_name'] + '\'s Videos: ' + query_type.title()
    # A description for the feed
    feed_description = 'Twitch Videos By ' + json_channel['display_name'] + ' (' + query_type.title() + ')'
    # Link to where the feed was generated from
    feed_link = json_channel['url']

    feed = Atom1Feed(
            title=feed_title,
            description=feed_description,
            link=feed_link)

    # Get videos
    query_types = {
            'all': 'archive,upload,highlight',
            'uploads': 'upload',
            'past-broadcasts': 'archive',
            'highlights': 'highlight'
            }
    request_params = {
            'broadcast_type': query_types[query_type]
            }
    request_url = 'https://api.twitch.tv/kraken/channels/' + query_channel + '/videos'
    json_videos = get(url=request_url, headers=request_headers, params=request_params).json()

    # Generate feed items
    for video in json_videos['videos']:
        description = '<p><img src="' + video['preview'] + '" ></p>'
        if video['description_html']:
            description = description + video['description_html']

        date = datetime.strptime(video['published_at'], '%Y-%m-%dT%H:%M:%SZ')

        feed.add_item(
            title=video['title'],
            link=video['url'],
            author_name=json_channel['display_name'],
            author_link=json_channel['url'],
            pubdate=date,
            updateddate=date,
            unique_id=video['_id'],
            description=description,
            categories=('twitch', video['broadcast_type']))

    return feed.writeString("utf-8")
