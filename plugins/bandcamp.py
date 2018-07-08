#!/bin/python3
# coding: utf-8

from urllib.parse import urlparse
from feedgenerator import Atom1Feed
from datetime import datetime
from requests import get
from lxml import html

import re


class Album:
    def __init__(self, link, title, artwork):
        title_regex = re.compile('\s+(.+)')
        artwork_regex = re.compile('_\d+.jpg')

        self.link = link
        self.title = title_regex.findall(title)[0]
        self.artwork = artwork_regex.sub('_0.jpg', artwork)


# Returns a list of albums
def get_albums(tree, url_base):
    albums = []

    grid = tree.find_class('music-grid-item')

    # If artist only has 1 album, it is directly displayed
    # instead of the usual album grid so it must be handled differently
    if len(grid) == 0:
        link = url_base
        title = tree.find_class('trackTitle')[0].text_content()
        artwork = tree.get_element_by_id('tralbumArt')\
            .xpath('a')[0].attrib['href']

        albums.append(Album(link, title, artwork))
    else:
        for element in grid:
            link = element.xpath('a')[0].attrib['href']
            artwork = element.xpath('a/div/img')[0].attrib['src']
            title = element.xpath('a/p')[0].text_content()

            albums.append(Album(link, title, artwork))

    return albums


# Returns True or False depending on if this
# plugin can handle the url passed as an argument
def check(url):
    url_music = url + '/music'
    page = get(url_music, headers={'User-Agent': 'Mozilla/5.0'})
    tree = html.fromstring(page.content)

    grid = tree.find_class('music-grid-item')

    if len(grid) > 0:
        return True
    else:
        if tree.get_element_by_id('name-section', None) is not None:
            return True

    return False


# Takes a url to a page, and returns the query that the generate function wants
def query(url):
    return urlparse(url).netloc


# Takes a query and returns a utf-8 encoded string containing the feed
def generate(query):
    url_base = 'http://' + query
    url_music = url_base + '/music'

    # Load page
    page = get(url_music, headers={'User-Agent': 'Mozilla/5.0'})
    tree = html.fromstring(page.content)
    tree.make_links_absolute(url_base)

    # A title/name for the whole feed
    feed_title = tree.get_element_by_id('band-name-location')\
        .find_class('title')[0].text_content()
    # A description for the feed
    bio_element = tree.get_element_by_id('bio-text', None)
    if bio_element is None:
        feed_description = ""
    else:
        feed_description = bio_element.text_content()
    # Link to where the feed was generated from
    feed_link = url_base

    feed = Atom1Feed(
            title=feed_title,
            description=feed_description,
            link=feed_link)

    # Get albums
    albums = get_albums(tree, url_base)

    # Generate feed items
    for album in albums:
        # print(album.title)
        # print('  ' + album.link)
        # print('  ' + album.artwork)

        desc = '<a href="' + album.link + '">' + \
               '<img src="' + album.artwork + '" width="500px">' + \
               '</img>' + \
               '</a>'

        feed.add_item(
            title=album.title,
            link=album.link,
            pubdate=datetime.now(),
            unique_id=album.title,
            description=desc,
            categories=('music', 'bandcamp'))

    return feed.writeString("utf-8")


# print(generate(query('http://lapfoxtrax.com/')))
# print('---------------------------------------------')
# generate('laurenbousfieldanyev3r.bandcamp.com')
# print('---------------------------------------------')
# print(generate('stuckinnovember.bandcamp.com'))
