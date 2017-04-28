#!/bin/python3

from importplug import import_plugins

from time import asctime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from os import getcwd

import traceback
import argparse


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        try:
            url = urlparse(s.path)
            url_query = url.query
            url_path = url.path
            url_plugin = url_path.split(sep='/')[-1]

            if url_path == '/':
                url_query_parsed = parse_qs(url.query)
                if 'url' in url_query_parsed:
                    for name, plugin in plugins.items():
                        if plugin.check(url_query_parsed['url'][0]):
                            # Usable plugin found
                            # Send redirect to proper feed url

                            redir = args.location + name + '?' + plugin.query(url_query_parsed['url'][0])

                            s.send_response(301)
                            s.send_header('Location', redir)
                            s.end_headers()

                            return
                else:
                    # Send index page
                    s.send_response(200)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()

                    f = open(args.directory + "/index.html", 'rb')
                    s.wfile.write(f.read())
                    f.close()

                    return

            elif url_plugin in plugins:
                # A valid plugin is available, so use it
                output = plugins[url_plugin].generate(url_query)

                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()

                s.wfile.write(output.encode("utf-8"))

                return

            # Send a 404, because no plugin is available for the url
            s.send_error(404)

        except Exception as e:
            s.send_error(500)
            traceback.print_exc()


# Argument parsing
parser = argparse.ArgumentParser()

parser.add_argument('--host',
                    help='Hostname/address to listen on',
                    default='localhost')
parser.add_argument('--port',
                    help='Port to use for incoming connections',
                    type=int,
                    default=80)
parser.add_argument('--directory',
                    help='Directory where index.html and /plugins directory is stored',
                    default=getcwd())
parser.add_argument('--location',
                    help='Full location/URL where Feedo is available',
                    default='http://localhost/')

args = parser.parse_args()


# Import plugins
plugins = import_plugins(args.directory + '/plugins')

server = HTTPServer((args.host, args.port), MyHandler)

# Run server
print(asctime(), 'Starting Feedo..')

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
print(asctime(), 'Feedo closing!')
