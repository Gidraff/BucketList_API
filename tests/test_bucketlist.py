"""Module that contains bucketlis test cases."""
import unittest
import json
from app import db, create_app


class BucketlistTestCase(unittest.TestCase):
    """Class for bucketlist test cases."""

    def setUp(self):
        """Set up test fixture."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.user = {
            'username': 'testuser',
            'email': 'testuser@testuser.com',
            'password': 'password'
        }

        self.bucketlist = {
            "title": "travel",
            "description": "sail across atlantic"
        }
        # binds app to the current_context
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def registration(self):
        """Register a user."""
        self.client.post(
            '/auth/register/',
            data=json.dumps(self.user),
            content_type='application/json'
        )

    def login(self):
        """Login user."""
        response = self.client.post(
            '/auth/login/',
            data=json.dumps(self.user),
            content_type='application/json'
        )
        return response

    def test_bucketlist_creation(self):
        """Test bucketlist creation."""
        self.registration()
        token = json.loads(self.login().data)
        res = self.client.post('/bucketlists/',
                               data=json.dumps(self.bucketlist),
                               content_type='application/json',
                               headers={
                                   "Authorization": token['access_token']})
        self.assertEqual(res.status_code, 201)

    def test_api_can_get_all_bucketlist(self):
        """Test get all bucketlist."""
        self.registration()
        token = json.loads(self.login().data)
        res = self.client.post(
            '/bucketlists/',
            data=json.dumps(self.bucketlist),
            content_type='application/json',
            headers={'Authorization': token["access_token"]})
        rev = self.client.get(
            '/bucketlists/',
            content_type='application/json',
            headers={'Authorization': token["access_token"]})
        self.assertEqual(200, rev.status_code)

    def test_bucketlist_can_be_edited(self):
        """Test bucketlist editing."""
        self.registration()
        token = json.loads(self.login().data)

        res = self.client.post(
            '/bucketlists/',
            data=json.dumps({
                'title': 'Goto',
                'description': 'Nort pole for weekened'}),
            content_type='application/json',
            headers={"Authorization": token["access_token"]})

        results = json.loads(res.data.decode())
        print('results', results)

        rev = self.client.put(
            '/bucketlists/{}/'.format(results['id']),
            data=json.dumps({
                'title': 'Go to hawaii',
                'description': 'goforvacation'}),
            content_type='application/json',
            headers={"Authorization": token["access_token"]})

        print("Reeeees", rev.data.decode())
        self.assertEqual(200, rev.status_code)

    def test_api_can_get_bucketlist_by_id(self):
        """Test get bucket by id."""
        self.registration()
        token = json.loads(self.login().data)

        res = self.client.post(
            '/bucketlists/',
            data=json.dumps(self.bucketlist),
            content_type='application/json',
            headers={'Authorization': token["access_token"]}
        )
        self.assertEqual(201, res.status_code)
        result_in_json = json.loads(
            res.data)

        rev = self.client.get(
            '/bucketlists/{}/'.format(
                result_in_json['id']),
            content_type='application/json',
            headers={'Authorization': token["access_token"]})
        self.assertEqual(200, rev.status_code)
        self.assertIn('travel', str(rev.data))

    def test_api_can_delete_bucketlist(self):
        """Test bucketlist deletion."""
        self.registration()
        response = self.login()
        data = json.loads(response.data.decode())
        result = self.client.post(
            '/bucketlists/',
            data=json.dumps({
                'title': 'travel',
                'description': 'travel asia'
            }),
            headers={
                "Authorization": data['access_token']
            },
            content_type='application/json'
        )

        response = self.client.delete(
            '/bucketlists/1/',
            headers={
                "Authorization": data['access_token']},
            content_type='application/json')
        self.assertEqual(200, response.status_code)
