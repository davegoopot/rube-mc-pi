"""Simple HTTP server for demonstrating the http plug in"""

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import urlparse

class DemoHttpServer(BaseHTTPRequestHandler):
    """Keep a simple dictionary of request paths.  Return (0,0) if hasn't
    been set before."""
    
    VALUE_DICT = {}
    
    def do_GET(self):
        """Return the value recorded for the path"""
        value = DemoHttpServer.VALUE_DICT.get(self.path, "0,0")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(value)
        return

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        
        value = form["block"].value
        DemoHttpServer.VALUE_DICT[self.path] = value
        
        self.wfile.write("Value set = " + value)
        
        return        
        
        
if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('192.168.56.101', 8888), DemoHttpServer)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()