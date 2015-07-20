# yolo

import string
import json
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from argparse import ArgumentParser


parser = ArgumentParser(description='Process the desired port.')
parser.add_argument("-p", "--port", dest="port", help="Port to listen on", metavar="PORT")

args = parser.parse_args().__dict__

port_arg = args['port'] or "8080"
port = 8080 if port_arg is None else int(port_arg)

file_arg = "whitney.json"

try:
    content = json.loads(open(file_arg).read())
except IOError:
    print "Couldn't find JSON file '%s'" % file_arg
    sys.exit()

class WhitneyAPIServer(BaseHTTPRequestHandler):
  def GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        path = self.path[1:]
        components = string.split(path, '/')

        node = content
        for component in components:
            if len(component) == 0 or component == "favicon.ico":
                continue

            if type(node) == dict:
                node = node[component]

            elif type(node) == list:
                node = node[int(component)]

        self.wfile.write(json.dumps(node))

        return

try:
    server = HTTPServer(('', port), InstantAPIServer)
    print 'Starting instant API server on port %s...' % (port)
    server.serve_forever()

except KeyboardInterrupt:
    print 'Stopping instant API server...'
    server.socket.close()
