#!/bin/python3
# coding: utf-8

from feedgenerator import Atom1Feed
from datetime import datetime

# Imports for the examples
# from urllib.parse import urlparse
# from json import loads
# from urllib.request import urlopen


# Returns True or False depending on if this
# plugin can handle the url passed as an argument
def check(url):
    # For example check if domain name contains a certain string:
    # parsed = urlparse(url)
    # return "somesite.com" in parsed.netloc
    pass


# Takes a url to a page, and returns the query that the generate function wants
def query(url):
    # Example that simply gets the query string from the url passed
    # return urlparse(url).query
    pass


# Takes a query and returns a utf-8 encoded string containing the feed
def generate(query):
    # Usefol thing for loading a json document from a site:
    # response = urlopen(url)
    # json_data = loads(response.read().decode("utf-8"))
    # json_data is then a tree of dictionaries containing the json response

    # A title/name for the whole feed
    feed_title = "A feed title"
    # A description for the feed
    # Optional and maybe not too relevant in all cases
    feed_description = "A short feed description"
    # Link to where the feed was generated from
    feed_link = "https://where.the/feed/came/from/"

    feed = Atom1Feed(
            title=feed_title,
            description=feed_description,
            link=feed_link)

    posts = ()
    for post in posts:
        # An id that must be uniqute for this post
        # This shouldn't change even if the post contents change
        post_id = 987345
        # A title for the post
        post_title = "A Post Title"
        # Link to the post itself
        post_link = "https://website.com/a_post"
        # The date the post was updated.
        # The following formats a unix epoch timestamp into the correct format:
        post_date = datetime.strptime(1493157617, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Post description or contents.
        # This is what will be shown in your feed reader
        post_description = "A description/some post contents"
        # A list of tags/categories for the post.
        # This is optional but can be very useful for filtering in feed readers
        post_tags = ("a", "list", "of", "tags")

        feed.add_item(
            title=post_title,
            link=post_link,
            pubdate=post_date,
            unique_id=post_id,
            description=post_description,
            categories=post_tags)

    return feed.writeString("utf-8")
