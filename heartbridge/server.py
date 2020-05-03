"""
Used to receive HTTP requests at a specified port. Will only
handle JSON payloads contained in POST requests.
"""

import json, socket
from http.server import HTTPServer, BaseHTTPRequestHandler

class JSONRequestHandler(BaseHTTPRequestHandler):
    """
    Handles HTTP POST requests with a JSON payload, for intercepting
    heart rate data exported from Shortcuts.
    """

    def do_POST(self):
        """
        Invoked when a POST request has been made.
        """ 

        # The server's payload property will hold deserialized JSON to be passed to another function.
        self.server.payload = None

        # Get Content-Length for JSON file:
        content_length = int(self.headers.get('Content-Length'))
        if content_length is None:
            # Refuse to accept anything without a Content-Length header sent.
            self.send_error(411)
        content_type = self.headers.get('Content-Type')
        if content_type != 'application/json':
            # Let the user know the header was either not sent, or the payload was unexpected.
            self.log_error("This application only accepts JSON payloads, please POST one with the Content-Type:application/json header set.")
            self.send_error(415)
            self.server.payload = None
        else:
            # Read the right number of bytes in based on content length:
            input_data = self.rfile.read(content_length)
            decoded = input_data.decode('UTF-8')
            # Deserialize the JSON passed in, and process it:
            try:
                json_data = json.loads(decoded)
                # Set the payload attribute on the HTTP Server to the JSON received.
                # This will be returned to another function once the request has been handled.
                self.server.payload = json_data
                self.send_response(200)
            except json.JSONDecodeError as e:
                self.send_error(400, "Invalid JSON")
        self.end_headers()

    def log_request(self, code='-', size='-'):
        # This is overridden to quiet the server a little when receiving successful requests
        pass

def run(port=8888):
    """
    Starts the HTTP server and listens for a request. If request was made 
    properly, will return the JSON payload of the request, deserialized to a dict
    so it can be processed by another function.

    Arguments:
        * port: The port to listen on (defaults to 8888)
    """

    with HTTPServer(('0.0.0.0', port), JSONRequestHandler) as httpd:
        port = httpd.socket.getsockname()[1]
        hostname = socket.gethostname()
        print("\U000026A1 Waiting to receive heart rate sample data at http://{}:{}.".format(hostname, port))
        # Handles a single HTTP request:
        httpd.handle_request()
        return(httpd.payload)