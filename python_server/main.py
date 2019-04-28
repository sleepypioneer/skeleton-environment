import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import Counter, MetricsHandler

c = Counter('requests_total', 'requests', ['status', 'endpoint'])

HOST_NAME = '0.0.0.0' # This will map to avialable port in docker
PORT_NUMBER = 8001


class HTTPRequestHandler(MetricsHandler):
    def get_trees(self):
        self.do_HEAD()
        self.wfile.write(bytes(json.dumps({"myFavouriteTree":"Oak"}), 'utf-8'))
        c.labels(status='200', endpoint='/trees').inc()

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        endpoint = self.path
        if endpoint == '/trees':
            return self.get_trees()
        elif endpoint == '/metrics':
            return super(HTTPRequestHandler, self).do_GET()
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