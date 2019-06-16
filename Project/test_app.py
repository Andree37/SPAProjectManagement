"""
 Integration Tests for app
 Made by: André Ribeiro & Daniel Afonso
"""
import unittest
import requests
from datetime import timedelta, datetime
# To test this, app.py must be running in a different thread or the web site must be running

base_url = 'http://darfkman.pythonanywhere.com/'  # "http://localhost:8000/"
s = requests.Session()


class BasicTests(unittest.TestCase):

    # Functions for user manipulation
    def create_test_user(self):
        create_url = base_url + 'api/user/register/'
        s.post(create_url, json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com', 'password': '123'})
        s.get(base_url + 'api/authenticate/c86627a2ecb27e0af08ec531423347005ea04dc7c837cad69409358f/')

    def login_test_user(self):
        login_url = base_url + 'api/user/login/'
        s.post(login_url, json={'username': 'user_test', 'password': '123'})

    def logout_test_user(self):
        logout_url = base_url + 'api/user/logout/'
        s.get(logout_url)

    def delete_test_user(self):
        delete_url = base_url + 'api/user/'
        s.delete(delete_url)

    # Admin tests
    # Test using Admin access as admin
    def test_admin_privilege_ok(self):
        test_url = base_url + 'admin/'
        login_url = base_url + 'api/user/login/'
        s.post(login_url, json={'username': 'dani', 'password': '123'})
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)

    # Test using Admin access as not admin
    def test_admin_privilege_deny(self):
        test_url = base_url + 'admin/'
        self.create_test_user()
        self.login_test_user()
        response = s.get(test_url)
        self.assertEqual(response.status_code, 403)
        self.delete_test_user()

    # Authentication Tests
    # Authenticate with correct key
    def test_authenticate_ok(self):
        test_url = base_url + 'api/authenticate/'
        create_url = base_url + 'api/user/register/'
        s.post(create_url, json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com', 'password': '123'})
        response = s.get(test_url + 'c86627a2ecb27e0af08ec531423347005ea04dc7c837cad69409358f/')
        self.assertEqual(response.status_code, 200)
        self.login_test_user()
        self.delete_test_user()

    # Authenticate with bad key
    def test_authenticate_deny(self):
        test_url = base_url + 'api/authenticate/'
        create_url = base_url + 'api/user/register/'
        s.post(create_url, json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com', 'password': '123'})
        response = s.get(test_url + '111/')
        self.assertEqual(response.status_code, 401)
        s.get(base_url + 'api/authenticate/c86627a2ecb27e0af08ec531423347005ea04dc7c837cad69409358f/')
        self.login_test_user()
        self.delete_test_user()

    # General tests
    # Test main page
    def test_main(self):
        response = s.get(base_url)
        self.assertEqual(response.status_code, 200)

    # Registration Tests
    # Test regular registration
    def test_register_ok(self):
        """Register should return 201"""
        test_url = base_url + 'api/user/register/'
        logout_url = base_url + 'api/user/logout/'
        s.get(logout_url)
        # Valid Input with new data
        response = s.post(test_url,
                          json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com', 'password': '123'})

        self.assertEqual(response.status_code, 201)
        s.get(base_url + 'api/authenticate/c86627a2ecb27e0af08ec531423347005ea04dc7c837cad69409358f/')
        # Delete the new data
        self.delete_test_user()

    # Test registration with existing user
    def test_register_old(self):
        test_url = base_url + 'api/user/register/'
        self.create_test_user()
        # Valid Input with existing data

        response = s.post(test_url,
                          json={'name': 'test', 'username': 'user_test', 'email': 'test@email.com',
                                'password': '123'})
        self.assertEqual(response.status_code, 409)
        # Delete test user
        self.login_test_user()
        self.delete_test_user()

    # Test registration with bad input values
    def test_register_bad_input(self):
        test_url = base_url + 'api/user/register/'
        # Bad Input
        response = s.post(test_url,
                          json={})
        self.assertEqual(response.status_code, 409)

    # Test registration with no input
    def test_register_no_input(self):
        test_url = base_url + 'api/user/register/'
        # NO Input
        response = s.post(test_url, None)
        self.assertEqual(response.status_code, 409)

    # Login Tests
    # Test regular login
    def test_login_ok(self):
        test_url = base_url + 'api/user/login/'
        self.create_test_user()
        #  valid input
        response = s.post(test_url,
                          json={'username': 'user_test', 'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test login with wrong password with existing user
    def test_login_wrong_data(self):
        test_url = base_url + 'api/user/login/'
        self.create_test_user()
        # wrong password
        response = s.post(test_url,
                          json={'username': 'user_test', 'password': '223'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test login with bad input values
    def test_login_bad_input(self):
        test_url = base_url + 'api/user/login/'
        # bad data
        response = requests.post(test_url, json={'bad': 'data'})
        self.assertEqual(response.status_code, 404)

    # Test login with no input values
    def test_login_no_input(self):
        test_url = base_url + 'api/user/login/'
        # no data
        response = requests.post(test_url, None)
        self.assertEqual(response.status_code, 404)

    # Logout Tests
    # Test logout with user logged in
    def test_logout_authorized(self):
        test_url = base_url + 'api/user/logout/'
        self.create_test_user()
        self.login_test_user()
        # Authorized
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.login_test_user()
        self.delete_test_user()

    # Test logout without logging in
    def test_logout_unauthorized(self):
        test_url = base_url + 'api/user/logout/'
        self.logout_test_user()
        # Unauthorized
        response = s.get(test_url)
        self.assertEqual(response.status_code, 401)

    # Single User Tests
    # Test single_user regular get
    def test_single_user_ok(self):
        test_url = base_url + 'api/user/'
        self.create_test_user()
        self.login_test_user()
        # GET
        # Normal request
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test single_user get without logging in
    def test_single_user_unauthorized(self):
        test_url = base_url + 'api/user/'
        self.logout_test_user()
        # Logged out request
        s.get(base_url + 'api/user/logout/')  # in case still logged in
        response = s.get(test_url)
        self.assertEqual(response.status_code, 401)

    # Test single_user put regular update
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

    # Test single_user put with bad input values for update
    def test_single_user_update_on_bad_input(self):
        test_url = base_url + 'api/user/'
        self.create_test_user()
        self.login_test_user()
        # bad update
        response = s.put(test_url, json={'bananas': '2'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_user put with no input values for update
    def test_single_user_update_no_input(self):
        test_url = base_url + 'api/user/'
        self.create_test_user()
        self.login_test_user()
        # bad update
        response = s.put(test_url, None)
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_user delete regular deletion and verifying that the deleted user no longer exists
    def test_single_user_delete(self):
        test_url = base_url + 'api/user/'
        self.create_test_user()
        self.login_test_user()
        # DELETE
        response = s.delete(test_url)
        self.assertEqual(response.status_code, 200)
        # Login with non existing user
        response = s.post(base_url+'/api/user/login/', json={'username': 'user_test', 'password': '123'})
        self.assertEqual(response.status_code, 404)

    # All Projects Tests
    # Test all_projects get regular project
    def test_all_projects_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test all_projects get without logging in
    def test_all_projects_unauthorized(self):
        test_url = base_url + 'api/projects/'
        self.logout_test_user()
        response = s.get(test_url)
        self.assertEqual(response.status_code, 401)

    # Test all_projects post regular project
    def test_all_projects_post_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        self.assertEqual(response.status_code, 201)
        self.delete_test_user()

    # Test all_projects post with no input values
    def test_all_projects_post_no_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test all_projects post with no input values
    def test_all_projects_post_bad_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'bananas': '2'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Single Project Tests
    # Test single_project get regular project
    def test_single_project_get_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        response = s.get(test_url + pk_id + '/')
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test single_project get without logging in
    def test_single_project_get_unauthorized(self):
        test_url = base_url + 'api/projects/'
        self.logout_test_user()
        response = s.get(test_url + '1/')
        self.assertEqual(response.status_code, 401)

    # Test single_project get forbidden project
    def test_single_project_get_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.get(test_url + '1' + '/')
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_project delete regular project
    def test_single_project_delete_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        response = s.delete(test_url + pk_id + '/')
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test single_project delete forbidden project
    def test_single_project_delete_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.delete(test_url + '1' + '/')
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_project update regular project
    def test_single_project_update_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        response = s.put(test_url + pk_id + '/', json={'title': 'Test Project'})
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test single_project update without logging in
    def test_single_project_update_unauthorized(self):
        test_url = base_url + 'api/projects/'
        self.logout_test_user()
        response = s.put(test_url + '1' + '/', json={'title': 'Test Project'})
        self.assertEqual(response.status_code, 401)

    # Test single_project update forbidden
    def test_single_project_update_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.put(test_url + '1' + '/', json={'title': 'Test Project'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_project update with bad input values
    def test_single_project_update_bad_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        response = s.put(test_url + pk_id + '/', json={'bananas': '2'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_project update with no input values
    def test_single_project_update_no_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        response = s.put(test_url + pk_id + '/', None)
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # All Tasks tests
    # Test all_tasks get regular
    def test_all_tasks_get_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += pk_id + '/tasks/'
        s.post(test_url, json={'title': 'Test Task'})
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test all_tasks get unauthorized
    def test_all_tasks_get_unauthorized(self):
        test_url = base_url + 'api/projects/'
        self.logout_test_user()
        response = s.get(test_url + '1/tasks/')
        self.assertEqual(response.status_code, 401)

    # Test all_tasks get forbidden
    def test_all_tasks_get_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.get(test_url + '1' + '/tasks/')
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test all_tasks post regular
    def test_all_tasks_post_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += pk_id + '/tasks/'
        response = s.post(test_url, json={'title': 'Test Task'})
        self.assertEqual(response.status_code, 201)
        self.delete_test_user()

    # Test all_tasks post forbidden
    def test_all_tasks_post_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        test_url += '1' + '/tasks/'
        response = s.post(test_url, json={'title': 'Test Project'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test all_tasks post with no input values
    def test_all_tasks_post_no_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += pk_id + '/tasks/'
        response = s.post(test_url, json={})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test all_tasks post with bad input values
    def test_all_tasks_post_bad_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += pk_id + '/tasks/'
        response = s.post(test_url, json={'bananas': '2'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Single Task Tests
    # Test single_task get regular
    def test_single_task_get_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        print(response.content)
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]

        test_url += pk_id + '/tasks/'
        response = s.post(test_url, json={'title': 'Test Task'})
        task_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += task_id + '/'
        response = s.get(test_url)
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test single_task get without logging in
    def test_single_task_get_unauthorized(self):
        test_url = base_url + 'api/projects/'
        self.logout_test_user()
        response = s.get(test_url + '1/tasks/1/')
        self.assertEqual(response.status_code, 401)

    # Test single_task get forbidden project
    def test_single_task_get_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.get(test_url + '1/tasks/1/')
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_task delete regular project
    def test_single_task_delete_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += pk_id + '/tasks/'
        response = s.post(test_url, json={'title': 'Test Task'})
        task_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += task_id + '/'
        response = s.delete(test_url)
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test single_task delete forbidden project
    def test_single_task_delete_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.delete(test_url + '/1/tasks/1/')
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_task update regular project
    def test_single_task_update_ok(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += pk_id + '/tasks/'
        response = s.post(test_url, json={'title': 'Test Task'})
        task_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += task_id + '/'
        response = s.put(test_url, json={'completed': True})
        self.assertEqual(response.status_code, 200)
        self.delete_test_user()

    # Test single_task update without logging in
    def test_single_task_update_unauthorized(self):
        test_url = base_url + 'api/projects/'
        self.logout_test_user()
        response = s.put(test_url + '1/tasks/1/', json={'completed': True})
        self.assertEqual(response.status_code, 401)

    # Test single_task update forbidden
    def test_single_task_update_forbidden(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.put(test_url + '1/tasks/1/', json={'completed': True})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_task update with bad input values
    def test_single_task_update_bad_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += pk_id + '/tasks/'
        response = s.post(test_url, json={'title': 'Test Task'})
        task_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += task_id + '/'
        response = s.put(test_url, json={'bananas': '2'})
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()

    # Test single_task update with no input values
    def test_single_task_update_no_input(self):
        test_url = base_url + 'api/projects/'
        self.create_test_user()
        self.login_test_user()
        response = s.post(test_url, json={'title': 'Test Project'})
        pk_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += pk_id + '/tasks/'
        response = s.post(test_url, json={'title': 'Test Task'})
        task_id = ((response.content.decode()).split('"id":')[1]).split(',')[0]
        test_url += task_id + '/'
        response = s.put(test_url, None)
        self.assertEqual(response.status_code, 404)
        self.delete_test_user()


if __name__ == "__main__":
    unittest.main()
