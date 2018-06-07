#!/bin/python3

from urllib.parse import urlparse
from datetime import datetime
from json import loads
from urllib.request import urlopen

import feedgenerator


# Returns True or False depending on if this
# plugin can handle the url passed as an argument
def check(url):
    parsed = urlparse(url)
    return "derpibooru.org" in parsed.netloc and \
           parsed.path.startswith('/search')


# Takes a url to a page, and returns the query that the generate function wants
def query(url):
    return urlparse(url).query


# Takes a query and returns a utf-8 encoded string containing the feed
def generate(query):
    url = "https://derpibooru.org/search.json?filter_id=56027&" + query
    feedUrl = "https://derpibooru.org/search?filter_id=56027&" + query

    response = urlopen(url)
    jsonData = loads(response.read().decode("utf-8"))

    feedName = "Derpibooru Search: " + query

    feed = feedgenerator.Atom1Feed(
            title=feedName,
            description=query,
            link=feedUrl)

    for post in jsonData["search"]:
        # Generate description/post contents
        descript = '<p><a href="' + post["image"] + '"><img src="' +\
            post["representations"]["medium"] + '"></a></p>'

        # Add original post description (if any)
        descript += "<p>" + post["description"] + "</p>"

        # Add size information
        size = str(post["width"]) + "x" + str(post["height"])
        descript += "<b>Size:</b> " + size + "<br>"

        # Add a link to the source url of the post
        descript += '<b>Source:</b> <a href="' + post["source_url"] + '">' +\
            post["source_url"] + '</a><br>'

        postUrl = "https://derpibooru.org/" + str(post["id"])
        date = datetime.strptime(post["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
        tags = post["tags"].split(sep=', ')

        feed.add_item(
            title=str(post["id"]),
            link=postUrl,
            pubdate=date,
            unique_id=str(post["id"]),
            description=descript,
            categories=tags)

    return feed.writeString("utf-8")
