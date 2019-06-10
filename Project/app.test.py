

import unittest
from Project import app, db


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.logout('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()