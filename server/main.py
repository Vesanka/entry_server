from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)

sqllist = ['1', '2', '3']

redislist = ['4', '5', '6']

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path.endswith('get_sqlite'):

            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            
            output = ''
            output += '<html><body>'
            output += '<h1>Sql List</h1>'
            for item in sqllist:
                output += item
                output += '</br>'
            
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('get_redis'):

            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            
            output = ''
            output += '<html><body>'
            output += '<h1>Redis List</h1>'
            for item in redislist:
                output += item
                output += '</br>'
            
            output += '</body></html>'
            self.wfile.write(output.encode())


def main():
    PORT = 9000
    server_addres = ('localhost', PORT)
    server = HTTPServer(server_addres, RequestHandler)
    print(f'Server running on port {PORT}')
    server.serve_forever()

if __name__ == '__main__':
    main()