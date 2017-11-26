from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import socket

class MyHandler(BaseHTTPRequestHandler):

    # HTTP REQUESTS HERE
    def do_POST(self):
        print self.rfile.read(3)

        content = b"POST: Hello, Mbed!"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)
        return

    def do_GET(self):
        content = b"GET: Hello, Mbed!"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)
        return

    def do_PUT(self):
        content = b"PUT: Hello, Mbed!"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)
        return



def run():
    httpd = HTTPServer(('', 8080), MyHandler)
    print "HTTP server running on port 8080"
    print "Your IP address is: ", socket.gethostbyname(socket.gethostname())
    httpd.serve_forever()

if __name__ == '__main__':
    run()
