import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = '0.0.0.0' # This will map to avialable port in docker
PORT_NUMBER = 8001


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def get_trees(self):
        self.do_HEAD()
        self.wfile.write(bytes(json.dumps({"myFavouriteTree":"Oak"}), 'utf-8'))

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        endpoint = self.path
        if endpoint == '/trees':
            return self.get_trees()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

if __name__ == '__main__':
    myServer = HTTPServer((HOST_NAME, PORT_NUMBER), HTTPRequestHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass
    myServer.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))