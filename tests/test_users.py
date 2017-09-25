"""Module that contains user Test cases."""
import unittest
import json
from app import db
from app import create_app


class FlaskTest(unittest.TestCase):
    """Test Cases for user."""

    def setUp(self):
        """Test Case fixtures."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.user_data = {
            'username': 'janedoe',
            'email': 'janedoe@janedoe.com',
            'password': 'janedoe@123'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    # HELPER METHODS

    def registration(self):
        """Test API can register a user."""
        response = self.client.post(
            '/auth/register/',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        return response

    def login(self):
        """Login helper method."""
        return self.client.post(
            '/auth/login/',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )

    def logout(self, token):
        """Logout helper method."""
        return self.client.post(
            '/auth/logout/',
            headers={'Authorization': "{}".format(token)},
            content_type='application/json')

    def test_valid_user_registration(self):
        """Test if a user has been created."""
        response = self.client.post(
            '/auth/register/',
            data=json.dumps(self.user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_invalid_registration_details(self):
        """Test invalid register  details."""
        user_data = {'username': 'janedoes',
                     'email': 'janedoe@janedoe.com'
                     }
        response = self.client.post(
            '/auth/register/',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_user_duplication_registration(self):
        """Test duplicate in registering."""
        rev = self.registration()
        self.assertEqual(201, rev.status_code)

        user_two = {'username': 'janedoe',
                    'email': 'janedoe@janedoe.com',
                    'password': 'janedoe@123'
                    }
        response = self.client.post(
            '/auth/register/',
            data=json.dumps(user_two),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    def test_null_registration_details(self):
        """Test null values in registering."""
        user_data = {
            'username': '',
            'email': '',
            'password': ''
        }
        response = self.client.post(
            '/auth/register/',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_valid_login(self):
        """Test for valid details in login."""
        res = self.registration()
        deta = (self.login().data)
        self.assertEqual(201, res.status_code)

        user_details = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(
            '/auth/login/',
            data=json.dumps(user_details),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)

    def test_invalid_login_password(self):
        """Test for invalid details in login."""
        rev = self.registration()
        self.assertEqual(201, rev.status_code)

        user_details = {
            'email': self.user_data['email'],
            'password': '54321'
        }
        response = self.client.post(
            '/auth/login/',
            data=json.dumps(user_details),
            content_type='application/json'
        )
        self.assertEqual(401, response.status_code)

    def test_invalid_login_email(self):
        """Tests for invalid login email."""
        rev = self.registration()
        self.assertEqual(201, rev.status_code)

        user_details = {
            'email': 'jane@jane.jane',
            'password': self.user_data['password']
        }
        response = self.client.post(
            '/auth/login/',
            data=json.dumps(user_details),
            content_type='application/json'
        )
        self.assertEqual(401, response.status_code)

    def test_reset_password(self):
        """Test for password resetting."""
        self.registration()
        response = self.client.post(
            '/auth/reset-password/',
            data=json.dumps({"email": self.user_data['email']}),
            content_type='application/json'
        )
        print("response", response.data)
        self.assertEqual(200, response.status_code)

    def test_user_login(self):
        """Test for user login."""
        res = self.registration()
        self.assertEqual(201, res.status_code)

        response = self.login()
        self.assertIn(
            b'You are logged in!', response.data)

    def test_user_logout(self):
        """Test for user logout."""
        self.registration()
        token = json.loads(self.login().data.decode())['access_token']
        response = self.logout(token)
        self.assertEqual(200, response.status_code)
