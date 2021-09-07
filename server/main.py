from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)
import json
import sqlite3

import redis

from sqlite_classes import (
    SqliteManager,
)
from methods import (
    LogManager,
)
from redis_classes import (
    RedisManager,
)
import settings

logger = LogManager(settings.LOG_FILE)

sql_manager = SqliteManager(settings.SQL_DB)

redis_manager = RedisManager(
    settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)


class RequestHandler(BaseHTTPRequestHandler):

    def send_resp(self, response):
        self.send_response(response)
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def do_GET(self):

        output = ''

        if self.path.endswith('get_sqlite'):
            self.send_resp(200)
            for value in sql_manager.do_select_all(settings.SQL_TABLE):
                output += str(value)
            self.wfile.write(output.encode())

        elif self.path.endswith('get_redis'):
            self.send_resp(200)
            re_data = redis_manager.do_get_all()
            for key, value in re_data.items():
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
                sql_manager.do_insert(settings.SQL_TABLE, data_string)
            except (json.JSONDecodeError, sqlite3.OperationalError) as err:
                self.send_resp(400)
                logger.error(code='400', path=self.path,
                             headers=self.headers, error=err.__class__)
            else:
                self.send_resp(200)
                logger.info(code='200', path=self.path,
                            headers=self.headers, body=data_string)

        elif self.path.endswith('post_redis'):
            try:
                data = json.loads(data_string)
                for key, value in data.items():
                    redis_manager.do_set(key=key, value=value)
            except json.JSONDecodeError as err:
                self.send_resp(400)
                logger.error(code='400', path=self.path,
                             headers=self.headers, error=err.__class__)
            except redis.exceptions.ConnectionError as err:
                self.send_resp(500)
                logger.error(code='500', path=self.path,
                            headers=self.headers, error=err.__class__)
            else:
                self.send_resp(200)
                logger.info(code='200', path=self.path,
                            headers=self.headers, body=data_string)

        else:
            self.send_resp(404)


def main():

    sql_manager.do_create(
        table_name=settings.SQL_TABLE,
        name='TEXT',
        number='INTEGER',
    )

    server_addres = (settings.SERVER_HOST, settings.SERVER_PORT)
    server = HTTPServer(server_addres, RequestHandler)
    print(f'Server running on port {settings.SERVER_PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    sql_manager.close()
    redis_manager.close()


if __name__ == '__main__':
    main()
