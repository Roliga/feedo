#!/bin/python3
# coding: utf-8

from feedgenerator import Atom1Feed
from datetime import datetime

# Imports for the examples
from urllib.parse import urlparse
import re
from requests import get
from shlex import shlex
# from json import loads
# from urllib.request import urlopen


def api_request(path, params = {}):
    client_id = 'LvWovRaJZlWCHql0bISuum8Bd2KX79mb'

    url = 'https://api.soundcloud.com/' + path
    payload = { 'client_id' : client_id, **params}

    result = get(url, params=payload)
    return result.json()


# Returns True or False depending on if this
# plugin can handle the url passed as an argument
def check(url):
    parsed = urlparse(url)
    regex = re.compile('^/.+/?(|tracks|reposts)')

    return "soundcloud.com" in parsed.netloc and regex.match(parsed.path) is not None


# Takes a url to a page, and returns the query that the generate function wants
def query(url):
    # Example that simply gets the query string from the url passedA
    return urlparse(url).path


def get_tracks(user_id):
    url = 'users/' + str(user_id) + '/tracks'
    json = api_request(url, { 'linked_partitioning' : 1 })
    json_tracks = json['collection']

    if 'next_href' in json:
        url = json['next_href']
    else:
        return json_tracks

    while len(json_tracks) < 20:
        json = get(url).json()
        json_tracks += json['collection']

        if 'next_href' in json:
            url = json['next_href']
        else:
            break

    return json_tracks


# Takes a query and returns a utf-8 encoded string containing the feed
def generate(query):
    # Parse query
    path_split = query.split('/')
    query_user = path_split[1]

    # Get user info
    json_user = api_request('resolve', { 'url' : 'https://soundcloud.com/' + query_user })

    # A title/name for the whole feed
    feed_title = 'Tracks by ' + json_user['username']
    # A description for the feed
    # Optional and maybe not too relevant in all cases
    feed_description = json_user['description']
    # Link to where the feed was generated from
    feed_link = json_user['permalink_url']

    feed = Atom1Feed(
            title=feed_title,
            description=feed_description,
            link=feed_link)

    # Get sounds
    json_tracks = get_tracks(json_user['id'])

    for track in json_tracks:
        description = ''

        if track['artwork_url']:
            description = '<p><img src="' + track['artwork_url'] + '" ></p>'

        if track['description']:
            description = description + track['description']

        pubdate = datetime.strptime(track['created_at'], '%Y/%m/%d %H:%M:%S +0000')
        updateddate = datetime.strptime(track['last_modified'], '%Y/%m/%d %H:%M:%S +0000')

        categories = ['soundcloud']

        if track['genre']:
            categories += [track['genre']]

        if track['tag_list']:
            lex = shlex(track['tag_list'], posix=True)
            lex.whitespace_split = True
            lex.commenters = ''
            lex.quotes = '"'
            categories += list(lex)

        feed.add_item(
            title=track['title'],
            link=track['permalink_url'],
            author_name=track['user']['username'],
            author_link=track['user']['permalink_url'],
            pubdate=pubdate,
            updateddate=updateddate,
            unique_id=str(track['id']),
            description=description,
            categories=categories)

    return feed.writeString("utf-8")
