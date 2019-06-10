import unittest
import requests


# To test this, app.py must be running in a different thread


class BasicTests(unittest.TestCase):

    def test_mainpage(self):
        response = requests.get("http://localhost:8000/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = requests.post('http://localhost:8000/api/user/login/',
                                 json={'username': 'anocas', 'password': '123'})
        self.assertEqual(response.status_code, 200)

        # fail
        response = requests.post('http://localhost:8000/api/user/login/',
                                 json={'username': 'anocas', 'password': '222'})
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        response = requests.get('http://localhost:8000/api/user/logout/')
        self.assertEqual(response.status_code, 200)

        # Unauthorized
        response = requests.get('http://localhost:8000/api/user/logout/')
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
