import json
import unittest

from scipy.stats import chisquare

import backend.app as app


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_simple_roll(self):
        rv = self.app.get('/roll')
        response = json.loads(rv.data.decode('utf8'))
        self.assertTrue(1 <= response['sum'] <= 6)

    def test_d2_roll(self):
        rv = self.app.get('/roll?sides=2')
        response = json.loads(rv.data.decode('utf8'))
        self.assertTrue(1 <= response['sum'] <= 2)

    def test_big_roll(self):
        rv = self.app.get('/roll?sides=6&quantity=100')
        response = json.loads(rv.data.decode('utf8'))
        self.assertTrue(100 <= response['sum'] <= 600)

    def test_world_is_random(self):
        rv = self.app.get('/roll?sides=6&quantity=99999')
        response = json.loads(rv.data.decode('utf8'))
        self.assertTrue((chisquare(response['dice'])[1]) > 0.95)

if __name__ == '__main__':
    unittest.main()