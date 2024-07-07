import http.server
import http.client
import urllib.parse

class ReverseProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request('GET')

    def do_POST(self):
        self.proxy_request('POST')

    def proxy_request(self, method):
        # Parse the URL to extract the path and query
        url = urllib.parse.urlparse(self.path)
        path = url.path
        if url.query:
            path += '?' + url.query
        
        # Set up the connection to the target server
        conn = http.client.HTTPSConnection('ai.mcbbs.app')
        
        # Get the headers from the incoming request
        headers = dict(self.headers)
        
        # Remove the 'Host' header and set the target host
        headers.pop('Host', None)
        headers['Host'] = 'ai.mcbbs.app'
        
        # If the request is a POST, get the content length and read the body
        body = None
        if method == 'POST':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
        
        # Send the request to the target server
        conn.request(method, path, body, headers)
        
        # Get the response from the target server
        response = conn.getresponse()
        
        # Send the response status and headers to the client
        self.send_response(response.status, response.reason)
        for header, value in response.getheaders():
            self.send_header(header, value)
        self.end_headers()
        
        # Send the response body to the client
        self.wfile.write(response.read())
        
        # Close the connection to the target server
        conn.close()

if __name__ == '__main__':
    # Set the server address and port
    server_address = ('', 2333)
    
    # Create the HTTP server with the reverse proxy handler
    httpd = http.server.HTTPServer(server_address, ReverseProxyHTTPRequestHandler)
    
    # Start the HTTP server
    print('Starting reverse proxy server on port 2333...')
    httpd.serve_forever()
