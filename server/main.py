from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)
import json
import sqlite3

from sqlite_classes import (
    SqliteManager,
)
from methods import (
    LogManager,
)

logger = LogManager('server/log.json')

sql_manager = SqliteManager('test.db')

SQL_TABLE_NAME = 'testtable'

redislist = {}


class RequestHandler(BaseHTTPRequestHandler):

    def send_resp(self, response):
        self.send_response(response)
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def do_GET(self):

        output = ''

        if self.path.endswith('get_sqlite'):
            self.send_resp(200)
            for value in sql_manager.do_select_all(SQL_TABLE_NAME):
                output += str(value)
            self.wfile.write(output.encode())

        elif self.path.endswith('get_redis'):
            self.send_resp(200)
            for key, value in redislist.items():
                output += f'{key}: {value}\n'
            self.wfile.write(output.encode())

        elif self.path.endswith('get_logs'):
            self.send_resp(200)
            self.wfile.write(logger.get_log().encode())

        else:
            self.send_resp(404)

    def do_POST(self):

        data_string = self.rfile.read(int(self.headers['Content-Length']))

        if self.path.endswith('post_sqlite'):
            try:
                data = json.loads(data_string)
                sql_manager.do_insert(SQL_TABLE_NAME, data_string)
            except (json.JSONDecodeError, sqlite3.OperationalError) as err:
                self.send_resp(400)
                logger.error(code='400', path=self.path, headers=self.headers, error=err.__class__)
            else:
                self.send_resp(200)
                logger.info(code='200', path=self.path, headers=self.headers, body=data_string)

        elif self.path.endswith('post_redis'):
            try:
                data = json.loads(data_string)
            except json.JSONDecodeError:
                self.send_resp(400)
            else:
                self.send_resp(200)
                redislist.update(data)

        else:
            self.send_resp(404)


def main():

    sql_manager.do_create(
        table_name=SQL_TABLE_NAME,
        name='TEXT', 
        number='INTEGER',
    )

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
