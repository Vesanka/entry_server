from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)
import json

from sqlite_classes import (
    SqliteManager,
)

sql_manager = SqliteManager('test.db')

sql_table_name = 'testtable'

redislist = {}


class RequestHandler(BaseHTTPRequestHandler):

    global sql_manager

    def do_GET(self):

        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        output = ''

        if self.path.endswith('get_sqlite'):
            for value in sql_manager.do_select_all(sql_table_name):
                output += str(value)
            self.wfile.write(output.encode())

        if self.path.endswith('get_redis'):
            for key, value in redislist.items():
                output += f'{key}: {value}\n'
            self.wfile.write(output.encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(data_string)

        if self.path.endswith('post_sqlite'):
            sql_manager.do_insert(sql_table_name, data_string)


        if self.path.endswith('post_redis'):
            redislist.update(data)


def main():
    
    sql_manager.do_create(table_name=sql_table_name, name='TEXT', number='INTEGER')

    PORT = 9000
    server_addres = ('localhost', PORT)
    server = HTTPServer(server_addres, RequestHandler)
    print(f'Server running on port {PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    sql_manager.close()


if __name__ == '__main__':
    main()
