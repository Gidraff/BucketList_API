"""Modules and packages to be imported"""
import unittest
import json
from app import db, create_app

class ActivityTestCase(unittest.TestCase):
    """Class that contains all the test cases"""

    def setUp(self):
        """Test cases fixture"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        #user
        self.user = {
            'username': 'usertest',
            'email': 'usertest@usertest.com',
            'password': 'usertestpass'
        }
        #bucketlist
        self.bucketlist = {
            'title': 'Travel',
            'description': 'Travel to middle east'
        }
        #activity
        self.activity = {
            'activity': 'learn different culture'
        }

        with self.app.app_context():
            """Initialized all database"""
            db.create_all()

    def register(self):
        """Register a user"""
        response = self.client().post(
            '/auth/register/', 
            data=self.user,
            content_type='application/json')
    
    def login(self):
        """logins a user"""
        return self.client.post(
            '/auth/login', 
            data=self.user,
            content_type='application/json')

    def test_create_bucketlist(self):
        """Creates bucketlist"""
        response = self.client.post(
            '/bucketlists/', 
            data=self.bucketlist,
            content_type='application/json')
    # post
    def test_activity_was_be_created(self):
        """Test if an activity was created"""
        res = self.client.post(
            '/bucketlists/', 
            data=self.bucketlist,
            content_type='application/json')
        self.assertEqual(201, res.status_code)

        # test for activity creation
        res = self.client.post(
            '/bucketlists/1/activities', 
            data=self.activity,
            content_type='application/json')
        self.assertEqual(201, res.status_code)

    def test_activity_exist(self):
        """Test if an activity can be retreived"""
        res = self.client.post(
            '/bucketlists/', 
            data=self.bucketlist,
            content_type='application/json')
        self.assertEqual(201, res.status_code)

        result = self.client.post(
            '/bucketlists/1/activities', 
            data=self.activity,
            content_type='application/json')
        self.assertEqual(201, result.status_code)

        rev = self.client.get(
            '/bucketlists/1/activities/1')
        self.assertIn(
            'learn different culture', rev.data)

    #put
    def test_activity_can_be_edited(self):
        """Test if an activity can be edited"""
        res = self.client.post(
            '/bucketlists/', 
            data=self.bucketlist,
            content_type='application/json')
        self.assertEqual(201, res.status_code)

        result = self.client.post(
            '/bucketlists/1/activities', 
            data=self.activity,
            content_type='application/json')
        self.assertEqual(201, result.status_code)

        rev = self.client.put(
            '/bucketlists/1/activities/1', data={
                'title': 'learn ways of asians'
            }, content_type='application/json')
        self.assertEqual(200, rev.status_code)

        result = self.client.get(
            '/bucketlists/1/activities/1')
        self.assertIn(
            'learn ways of asians', result.data)

    def test_delete_activity(self):
        """Test if an activity can be reviewed"""
        result = self.client.post(
            '/bucketlists/', 
            data=self.bucketlist,
            content_type='application/json')
        res = self.client.post(
            '/bucketlists/1/activities', data={
                'activity': 'learn japaness'
            }, content_type='application/json')
        self.assertEqual(201, res.status_code)

        rev = self.client.delete(
            '/bucketlists/1/activities/1')
        
        result = self.client.get('/bucketlists/1/activities/1')
        self.assertEqual(404, result.status_code)

    def tearDown(self):
        """Tear down variables initialized
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()