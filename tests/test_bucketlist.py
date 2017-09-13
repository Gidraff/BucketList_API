import unittest
import json
from app import db, create_app


class BucketlistTestCase(unittest.TestCase):
    """Class for bucketlist test cases"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.user = {
            'username': 'testuser',
            'email': 'testuser@testuser.com',
            'password': 'password'
        }

        self.bucketlist = {
            'title': 'travel',
            'description': 'sail across atlantic'
        }
        # binds app to the current_context
        with self.app.app_context():
            # creates all tables
            db.create_all()

    def registration(self):
        """Register a user"""
        response = self.client.post(
            '/auth/register/',
            data=self.user,
            content_type='application/json'
        )

    def login(self):
        """logins user"""
        return self.client.post(
            '/auth/login',
            data=self.user,
            content_type='application/json'
        )

    def test_bucketlist_creation(self):
        """Test if bucketlist has been created"""
        self.registration()
        self.login()
        res = self.client.post('/bucketlists/',
                               data=self.bucketlist,
                               content_type='application/json')
        self.assertEqual(201, res.status_code)

    def test_api_can_get_all_bucketlist(self):
        """
        Test if an API can return all bucketlists
        """
        self.registration()
        self.login()

        res = self.client.post(
            '/bucketlists/',
            data=self.bucketlist,
            content_type='application/json')
        self.assertEqual(201, res.status_code)
        rev = self.client.get('/bucketlists/')
        self.assertEqual(200, rev.status_code)

    def test_bucketlist_can_be_edited(self):
        """Test if bucketlis can be updated"""
        self.registration()
        self.login()

        res = self.client.post(
            '/bucketlists/', data={
                'title': 'Go to',
                'description': 'Nort pole for weekened'
            }, content_type='application/json')
        self.assertEqual(201, res.status_code)
        rev = self.client.put(
            '/bucketlists/1',
            data={
                'title': 'Go to hawaii',
                'descrption': 'go for vacation'
            }, content_type='application/json'
        )
        self.assertEqual(200, rev.status_code)

    def test_api_can_get_bucketlist_by_id(self):
        """Test if bucketlist can get a specific
            bucketlist using it's id
        """
        self.registration()
        self.login()

        res = self.client.post(
            '/bucketlists/',
            data=self.bucketlist,
            content_type='application/json'
        )
        self.assertEqual(201, res.status_code)
        result_in_json = json.loads(
            res.data.decode('utf-8'))

        rev = self.client.get(
            '/bucketlists/{}'.format(
                result_in_json['id']))
        self.assertEqual(200, rev.status_code)
        self.assertIn('travel', rev.data)

    def test_api_can_delete_bucketlist(self):
        """Test if a bucketlist can be deleted"""
        self.registration()
        self.login()

        result = self.client.post(
            '/bucketlists/', data={
                'title': 'travel',
                'description': 'travel asia'
            })
        self.assertEqual(201, result.status_code)

        response = self.client.delete('/bucketlists/1')
        self.assertEqual(200, response.status_code)

        rev = self.client.get('/bucketlists/1')
        self.assertEqual(404, rev.status_code)
    # delete

    def tearDown(self):
        """Tear down all initialized variables"""
        with self.app.app_context():
            db.session.close()
            db.drop_all()
