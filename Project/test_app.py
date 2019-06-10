import unittest
import requests

# To test this, app.py must be running in a different thread

base_url = "http://localhost:8000/"
s = requests.Session()


class BasicTests(unittest.TestCase):

    def test_main(self):
        response = s.get(base_url)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        test_url = base_url + 'api/user/register/'

        # Valid Input with new data
        response = s.post(test_url,
                          json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com', 'password': '123'})
        self.assertEqual(response.status_code, 201)

        # Valid Input with old
        response = s.post(test_url,
                          json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com',
                                'password': '123'})
        self.assertEqual(response.status_code, 200)  # ? Shouldn't accept the data, but should return OK ?
        # Delete test user
        s.post('http://localhost:8000/api/user/login/', json={'username': 'user_test', 'password': '123'})
        s.delete('http://localhost:8000/api/user/')

        # Bad Input
        response = s.post(test_url,
                          json={})
        self.assertEqual(response.status_code, 404)

        # NO Input
        response = s.post(test_url, None)
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        test_url = base_url + 'api/user/login/'

        #  valid input
        response = s.post(test_url,
                          json={'username': 'anocas', 'password': '123'})
        self.assertEqual(response.status_code, 200)

        # wrong password
        response = s.post(test_url,
                          json={'username': 'anocas', 'password': '223'})
        self.assertEqual(response.status_code, 404)

        # bad data
        response = requests.post(test_url, json={'BONKERS YEAH': 'CRAZY'})
        self.assertEqual(response.status_code, 404)

        # no data
        response = requests.post(test_url, None)
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        test_url = base_url + 'api/user/logout/'
        # Authorized
        s.post('http://localhost:8000/api/user/login/', json={'username': 'anocas', 'password': '123'})
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)

        # Unauthorized
        response = s.get(test_url)
        self.assertEqual(response.status_code, 401)

    def test_single_user(self):
        test_url = base_url + 'api/user/'
        # Create Test user
        s.post(base_url + 'api/user/register/',
               json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com', 'password': '123'})
        s.post('http://localhost:8000/api/user/login/', json={'username': 'user_test', 'password': '123'})

        # GET
        # Normal request
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)
        # Logged out request
        s.get(base_url + 'api/user/logout/')
        response = s.get(test_url)
        self.assertEqual(response.status_code, 401)
        s.post('http://localhost:8000/api/user/login/', json={'username': 'user_test', 'password': '123'})

        # PUT
        # update email
        response = s.put(test_url, json={'email': 'banana@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, (s.get(test_url)).content)
        # bad update
        response = s.put(test_url, json={'bananas': '2'})
        print(response.content)
        self.assertEqual(response.status_code, 404)

        # DELETE
        response = s.delete(test_url)
        self.assertEqual(response.status_code, 200)
        response = s.post('http://localhost:8000/api/user/login/', json={'username': 'user_test', 'password': '123'})
        self.assertEqual(response.status_code, 404)



if __name__ == "__main__":
    unittest.main()
