#!/bin/python3
# coding: utf-8

from urllib.parse import urlparse
from feedgenerator import Atom1Feed
from datetime import datetime
from requests import head, get

import re

# Imports for the examples
# from urllib.parse import urlparse
# from json import loads
# from urllib.request import urlopen


# Returns True or False depending on if this
# plugin can handle the url passed as an argument
def check(url):
    parsed = urlparse(url)
    regex = re.compile('^/.+/.+/issues/\d+')

    return "github.com" in parsed.netloc and regex.match(parsed.path) is not None


# Takes a url to a page, and returns the query that the generate function wants
def query(url):
    # Example that simply gets the query string from the url passed
    return urlparse(url).path


# Takes a query and returns a utf-8 encoded string containing the feed
def generate(query):
    # Get issue information
    url_issue = 'https://api.github.com/repos' + query
    json_issue = get(url_issue).json()

    # A title/name for the whole feed
    feed_title = json_issue['title']
    # A description for the feed
    feed_description = 'Issue number: ' + str(json_issue['number'])
    # Link to where the feed was generated from
    feed_link = json_issue['html_url']

    feed = Atom1Feed(
            title=feed_title,
            description=feed_description,
            link=feed_link)

    # Get latest comments
    url_comments = json_issue['comments_url']
    links_comments = head(url_comments).links

    if 'last' in links_comments:
        url_latest = links_comments['last']['url']
    else:
        url_latest = url_comments

    json_comments = get(url_latest).json()

    # Generate feed items
    for comment in json_comments:
        feed.add_item(
            title='Comment by ' + comment['user']['login'],
            link=comment['url'],
            author_name=comment['user']['login'],
            author_link=comment['user']['html_url'],
            pubdate=datetime.strptime(comment['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
            updateddate=datetime.strptime(comment['updated_at'], '%Y-%m-%dT%H:%M:%SZ'),
            unique_id=str(comment['id']),
            description=comment['body'],
            categories=('github', 'issue comment'))

    return feed.writeString("utf-8")
