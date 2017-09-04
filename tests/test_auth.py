import unittest
import json
from app import create_app, db
from app.models import User



class FlaskTest(unittest.TestCase):
    """Test fof flask routes"""

    def setUp(self):
        """Test Case fixtures"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.user_data = {
            'username': 'janedoe',
            'email': 'janedoe@janedoe.com',
            'password': 'janedoe@123' 
        }

        with self.app.app_context():
            db.session.close()
            db.create_all()
    
    ###### HELPER METHODS ######

    def registration(self):
        """Test API can register a user"""
        response = self.client().post(
            '/auth/register/', data=self.user_data)

    def login(self):
        return self.client.post(
            '/auth/login', data=self.user_data,
             follow_redirects=True)

    def logout(self):
        return self.client.post(
            '/auth/logout', follow_redirects=True)


    def test_valid_user_registration(self):
        """Test for user has been created"""
        response = self.client.post(
            '/auth/register', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        
    def test_invalid_registration_details(self):
        """Test for invalid user details"""
        user_data = {'username': 'janedoes',
                     'email': 'janedoe@janedoe.com'
                     }
        response = self.client.post(
            '/auth/register', data=user_data)
        self.assertEqual(response.status_code, 400)

    def test_user_duplication_registration(self):
        """Test if an existing user can register
           again
        """
        user_two = {'username': 'janedoe',
                    'email': 'janedoe@janedoe.com',
                    'password': 'janedoe@123'
                    }
        response = self.client.post(
            '/auth/register', data=user_two)
        self.assertEqual(response.status_code, 409)

    def test_null_registration_details(self):
        """Test for null values in registration"""
        user_data = {
            'username': '',
            'email': '',
            'password': ''
                    }
        response = self.client.post(
            '/auth/register', data=user_data)
        self.assertEqual(response.status_code, 400)

    def test_valid_login(self):
        """Test valid login details"""
        user_details = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
            }
        response = self.client.post(
            '/auth/login', data=user_details)
        self.assertEqual(200, response.status_code)

    def test_invalid_login_password(self):
        """Test invalid login details"""
        user_details = {
            'email': self.user_data['email'],
            'password': '54321'
        }
        response = self.client.post(
            '/auth/login', data=user_details)
        self.assertEqual(401, response.status_code)

    def test_invalid_login_email(self):
        """Tests for invalid login email"""
        user_details = {
            'email': 'jane@jane.jane',
            'password': self.user_data['password']
        }
        response = self.client.post(
            '/auth/login', data=user_details)
        self.assertEqual(401, response.status_code)
        
    def test_reset_password(self):
        """Test resetting password"""
        self.user_data = {
            'username': 'janedoe',
            'email': 'janedoe@janedoe.com',
            'password': 'janedoe@123' 
        }
        self.user_data['password'] = 'doe@jone321'
        response = self.client.post(
            '/auth/reset-password')
        self.assertEqual(201, response.status_code)

    def test_user_login(self):
        """Test a user can log in"""
        response = self.login()
        self.assertIn(
            b'You were logged in', response.data)

    def test_user_logout(self):
        """Test a user can logout"""
        response = self.logout()
        self.assertIn(
            b'You were logged out', response.data)
    
    def tearDown(self):
        """Tear down all initialized variables"""
        with self.app.app_context():
            db.drop_all()

        