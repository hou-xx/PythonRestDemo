#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import time

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        result = {}
        result["header"] = dict(self.headers)
        try:
            if "sleep" in result.get("header"):
                sleeptime = int(result.get("header").get("sleep"))
                if sleeptime > 0 and sleeptime <= 60:
                    time.sleep(sleeptime)
        except:
            pass

        result["url"] = self.path
        self.wfile.write(str.encode(json.dumps(result)))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_str = post_data.decode('utf-8')
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_str)
        result = {}
        result["post_raw"] = post_str
        result["header"] = dict(self.headers)
        try:
            if "sleep" in result.get("header"):
                sleeptime = int(result.get("header").get("sleep"))
                if sleeptime > 0 and sleeptime <= 60:
                    time.sleep(sleeptime)
        except:
            pass
        result["url"] = self.path
        try:
            json_obj = json.loads(post_str)
            result["post_json"] = json_obj
        except:
            pass
            
        self._set_response()
        self.wfile.write(str.encode(json.dumps(result)))

def run(server_class=HTTPServer, handler_class=S, port=80):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
