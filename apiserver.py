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

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        path = self.path[1:]
        components = string.split(path, '/')

        node = parse_node(content, components)

        self.wfile.write(json.dumps(node))

        return

# Thanks to Stack Overflow user Steven Moseley for the help on this function!
def parse_node(node, components):
    # For a valid node and component list:
    if node and len(components) and components[0] != "favicon.ico":
        # Dicts will return parse_node of the top-level node component found,
        # reducing the list by 1
        if type(node) == dict:
            return parse_node(node.get(components[0], None), components[1:])

        elif type(node) == list:
            # A list with an "all" argument will return a full list of sub-nodes matching the rest of the URL criteria
            if components[0] == "all":
                return [parse_node(n, components[1:]) for n in node]
            # A normal list node request will work as it did previously
            else:
                return parse_node(node[int(components[0])], components[1:])
    else:
        return node

    return None

try:
    server = HTTPServer(('', port), WhitneyAPIServer)
    print 'Starting Whitney API server on port %s...' % (port)
    server.serve_forever()

except KeyboardInterrupt:
    print 'Stopping Whitney API server...'
    server.socket.close()
