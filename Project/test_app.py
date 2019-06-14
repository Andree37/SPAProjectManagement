import unittest
import requests

# To test this, app.py must be running in a different thread

base_url = "http://localhost:8000/"
s = requests.Session()


class BasicTests(unittest.TestCase):

    def create_test_user(self):
        create_url = base_url + 'api/user/register/'
        response = s.post(create_url, json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com', 'password': '123'})
        s.get(base_url + 'api/authenticate/c86627a2ecb27e0af08ec531423347005ea04dc7c837cad69409358f/')

    def login_test_user(self):
        login_url = base_url + 'api/user/login/'
        s.post(login_url, json={'username': 'user_test', 'password': '123'})

    def delete_test_user(self):
        logout_url = base_url + 'api/user/'
        self.login_test_user()
        s.delete(logout_url)

    def test_main(self):
        response = s.get(base_url)
        self.assertEqual(response.status_code, 200)

    def test_register_ok(self):
        """Register should return 201"""
        test_url = base_url + 'api/user/register/'

        # Valid Input with new data
        response = s.post(test_url,
                          json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com', 'password': '123'})
        self.assertEqual(response.status_code, 201)
        s.get(base_url + 'api/authenticate/c86627a2ecb27e0af08ec531423347005ea04dc7c837cad69409358f/')
        # Delete the new data
        self.delete_test_user()

    def test_register_old(self):
        test_url = base_url + 'api/user/register/'
        self.create_test_user()
        # Valid Input with existing data

        response = s.post(test_url,
                          json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com',
                                'password': '123'})
        self.assertEqual(response.status_code, 409)
        # Delete test user
        self.delete_test_user()

    def test_register_bad_input(self):
        test_url = base_url + 'api/user/register/'
        # Bad Input
        response = s.post(test_url,
                          json={})
        self.assertEqual(response.status_code, 409)

    def test_register_no_input(self):
        test_url = base_url + 'api/user/register/'
        # NO Input
        response = s.post(test_url, None)
        self.assertEqual(response.status_code, 409)

    def test_login_ok(self):
        test_url = base_url + 'api/user/login/'
        self.create_test_user()
        #  valid input
        response = s.post(test_url,
                          json={'username': 'user_test', 'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    def test_login_wrong_data(self):
        test_url = base_url + 'api/user/login/'
        self.create_test_user()
        # wrong password
        response = s.post(test_url,
                          json={'username': 'user_test', 'password': '223'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    def test_login_bad_data(self):
        test_url = base_url + 'api/user/login/'
        # bad data
        response = requests.post(test_url, json={'bad': 'data'})
        self.assertEqual(response.status_code, 404)

    def test_login_no_data(self):
        test_url = base_url + 'api/user/login/'
        # no data
        response = requests.post(test_url, None)
        self.assertEqual(response.status_code, 404)

    def test_logout_authorized(self):
        test_url = base_url + 'api/user/logout/'
        self.create_test_user()
        self.login_test_user()
        # Authorized
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    def test_logout_unauthorized(self):
        test_url = base_url + 'api/user/logout/'
        # Unauthorized
        response = s.get(test_url)
        self.assertEqual(response.status_code, 401)

    def test_single_user_ok(self):
        test_url = base_url + 'api/user/'
        self.create_test_user()
        self.login_test_user()
        # GET
        # Normal request
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    def test_single_user_unauthorized(self):
        test_url = base_url + 'api/user/'
        # Logged out request
        s.get(base_url + 'api/user/logout/')  # in case still logged in
        response = s.get(test_url)
        self.assertEqual(response.status_code, 401)

    def test_single_user_update(self):
        test_url = base_url + 'api/user/'
        self.create_test_user()
        self.login_test_user()
        # PUT
        # update email
        response = s.put(test_url, json={'email': 'banana@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, (s.get(test_url)).content)
        self.delete_test_user()

    def test_single_user_update_on_bad_input(self):
        test_url = base_url + 'api/user/'
        self.create_test_user()
        self.login_test_user()
        # bad update
        response = s.put(test_url, json={'bananas': '2'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    def test_single_user_update_no_input(self):
        test_url = base_url + 'api/user/'
        self.create_test_user()
        self.login_test_user()
        # bad update
        response = s.put(test_url, None)
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    def test_single_user_delete(self):
        test_url = base_url + 'api/user/'
        self.create_test_user()
        self.login_test_user()
        # DELETE
        response = s.delete(test_url)
        self.assertEqual(response.status_code, 200)
        # Login with non existing user
        response = s.post('http://localhost:8000/api/user/login/', json={'username': 'user_test', 'password': '123'})
        self.assertEqual(response.status_code, 404)

    def test_all_projects_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    def test_all_projects_unauthorized(self):
        test_url = base_url + 'api/projects/'
        response = s.get(test_url)
        self.assertEqual(response.status_code, 401)

    def test_all_projects_post_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        self.assertEqual(response.status_code, 201)
        self.delete_test_user()

    def test_all_projects_post_no_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    def test_all_projects_post_bad_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'bananas': '2'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    def test_single_project_get_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id": ')[1]).split(',')[0]
        print(pk_id)
        response = s.get(test_url + pk_id + '/')
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    def test_single_project_get_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.get(test_url + '1' + '/')
        self.assertEqual(response.status_code, 403)
        self.delete_test_user()

    def test_single_project_delete_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id": ')[1]).split(',')[0]
        print(pk_id)
        response = s.delete(test_url + pk_id + '/')
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    def test_single_project_delete_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.delete(test_url + '1' + '/')
        self.assertEqual(response.status_code, 403)
        self.delete_test_user()

    def test_single_project_update_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id": ')[1]).split(',')[0]
        print(pk_id)
        response = s.put(test_url + pk_id + '/', json={'title': 'Test Project'})
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    def test_single_project_update_unauthorized(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        response = s.put(test_url + '1' + '/', json={'title': 'Test Project'})
        self.assertEqual(response.status_code, 401)
        self.delete_test_user()

    def test_single_project_update_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.put(test_url + '1' + '/', json={'title': 'Test Project'})
        self.assertEqual(response.status_code, 403)
        self.delete_test_user()

    def test_single_project_update_bad_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id": ')[1]).split(',')[0]
        print(pk_id)
        response = s.put(test_url + pk_id + '/', json={'bananas': '2'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    def test_single_project_update_no_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id": ')[1]).split(',')[0]
        print(pk_id)
        response = s.put(test_url + pk_id + '/', None)
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()


if __name__ == "__main__":
    unittest.main()
