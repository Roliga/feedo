Feedo
=====

Python 3 program that generates RSS/Atom feeds for sites that don't have them.

A basic docker container for Feedo is available at [roliga/docker-feedo](https://github.com/Roliga/docker-feedo/)

Usage
-----

	usage: feedo.py [-h] [--host HOST] [--port PORT] [--directory DIRECTORY]                                                                 
			[--location LOCATION]

	optional arguments:
	  -h, --help            show this help message and exit
	  --host HOST           Hostname/address to listen on
	  --port PORT           Port to use for incoming connections
	  --directory DIRECTORY
				Directory where index.html and /plugins directory is
				stored
	  --location LOCATION   Full location/URL where Feedo is available

Dependencies
------------

* Python 3
* LXML library for python 3
* Requests library for python 3

Supported sites
---------------

* [Bandcamp](https://bandcamp.com)
	- Artists, URLs like `https://[artist].bandcamp.com`, or any custom domain artist might have
* [Derpibooru](https://derpibooru.org/)
	- Searches, URLs like `https://derpibooru.org/search?[query]`
* [Github](https://github.com)
	- Comments on issues, URLs like `https://github.com/[author]/[project]/issues/[issue id]`
* [Twitch](https://twitch.tv/)
	- Channel videos, URLs like `https://twitch.tv/[channel]/videos/[video type]`

Planned sites
-------------

* [Soundcloud](https://soundcloud.com)
	- Artists uploads (with/without reposts)
* [Steam](https://store.steampowered.com/)
	- Salte status of game
	- Early access status
	- Released status
* [PriceSpy](https://pricespy.co.uk/)
	- Price changes of a product (including where the price changed, to allow filtering out unwanted stores)
