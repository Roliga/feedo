#!/bin/python3

from importplug import import_plugins

from time import asctime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import traceback

plugins = import_plugins("/home/roliga/stuff/mine/programming/python/feeds-modularized/plugins")

HOST_NAME = 'localhost'  # !!!REMEMBER TO CHANGE THIS!!!
LOCATION = 'http://localhost:9000/'
PORT_NUMBER = 9000  # Maybe set this to 9000.


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

            if url_plugin in plugins:
                # A valid plugin is available, so use it
                output = plugins[url_plugin].generate(url_query)

                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()

                s.wfile.write(output.encode("utf-8"))

                return
            else:
                # No valid plugin in the url, so check if a url was passed
                # in the query string has a plugin available for it
                for name, plugin in plugins.items():
                    if plugin.check(url_query):
                        # Usable plugin found
                        # Send redirect to proper feed url

                        redir = LOCATION + name + '?' + plugin.query(url_query)

                        s.send_response(301)
                        s.send_header('Location', redir)
                        s.end_headers()

                        return

                # Send a 404, because no plugin is available for the url

                s.send_error(404)

                return

        except Exception as e:
            s.send_error(500)
            traceback.print_exc()


if __name__ == '__main__':
    server = HTTPServer(('', PORT_NUMBER), MyHandler)
    print(asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print(asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
