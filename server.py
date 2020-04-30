from http.server import HTTPServer, BaseHTTPRequestHandler
import json, socket

class JSONRequestHandler(BaseHTTPRequestHandler):
    """
    Handles HTTP POST requests with a JSON payload, for intercepting
    heart rate data exported from Shortcuts.
    """

    def do_POST(self):
        """
        Invoked when a POST request has been made.
        """ 

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

def run(port=8888):
    """
    Starts the HTTP server and listens for a request.
    If request was made properly, will return the JSON payload of the request so it can be processed by another function.

    Args:
        port: The port to listen for requests on (defaults to 8888)
    """

    with HTTPServer(('localhost', port), JSONRequestHandler) as httpd:
        port = httpd.socket.getsockname()[1]
        hostname = socket.gethostname()
        print("Now accepting POST requests at http://{}:{}.".format(hostname, port))
        httpd.handle_request()
        return(httpd.payload)