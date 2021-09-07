import unittest
import requests

import settings


class Test_TestSql(unittest.TestCase):
    def test_get(self):
        g = requests.get(
            f'http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/get_sqlite')
        self.assertEqual(g.status_code, 200)

    def test_post(self):
        p = requests.post(
            f'http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/post_sqlite',
            data='{"name":"\'Alex\'"}',
        )
        self.assertEqual(p.status_code, 200)

    def test_post_bad_data(self):
        p = requests.post(
            f'http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/post_sqlite',
            data='{"no":"Alex"}',
        )
        self.assertEqual(p.status_code, 400)


class Test_TestRedis(unittest.TestCase):
    def test_get(self):
        g = requests.get(
            f'http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/get_redis')
        self.assertEqual(g.status_code, 200)

    def test_post(self):
        p = requests.post(
            f'http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/post_redis',
            data='{"name":"\'Alex\'"}',
        )
        self.assertEqual(p.status_code, 200)

    def test_post_bad_data(self):
        p = requests.post(
            f'http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/post_redis',
            data='something not a json',
        )
        self.assertEqual(p.status_code, 400)


class Test_TestPaths(unittest.TestCase):
    def test_get_wrong_path(self):
        r = requests.get(
            f'http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/get_something')
        self.assertEqual(r.status_code, 404)


if __name__ == '__main__':
    unittest.main()
