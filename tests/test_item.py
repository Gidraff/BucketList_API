"""Modules test case for item."""
import unittest
import json
from app import db, create_app


class itemTestCase(unittest.TestCase):
    """Class that contains all the test cases."""

    def setUp(self):
        """Test cases fixture."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        # user
        self.user = {
            'username': 'usertest',
            'email': 'usertest@usertest.com',
            'password': 'usertestpass'
        }
        # bucketlist
        self.bucketlist = {
            'title': 'Travel',
            'description': 'Travel to middle east'
        }
        # item
        self.item = {
            'item': 'learn different culture',
            "done": True
        }

        with self.app.app_context():
            """Initialize  database."""
            db.create_all()

    def register(self):
        """Register a user."""
        self.client.post(
            '/auth/register/',
            data=json.dumps(self.user),
            content_type='application/json')

    def login(self):
        """Login a user."""
        response = self.client.post(
            '/auth/login/',
            data=json.dumps(self.user),
            content_type='application/json')
        return response

    def test_create_bucketlist(self):
        """Test bucketlist creation."""
        self.register()
        token = json.loads(self.login().data)
        response = self.client.post(
            '/bucketlists/',
            data=json.dumps(self.bucketlist),
            content_type='application/json',
            headers={"Authorization": token['access_token']})
        self.assertEqual(201, response.status_code)
    # post

    def test_item_was_be_created(self):
        """Test item creation."""
        self.register()
        token = json.loads(self.login().data)
        res = self.client.post(
            '/bucketlists/',
            data=json.dumps(self.bucketlist),
            content_type='application/json',
            headers={'Authorization': token['access_token']})

        # test for item creation
        res = self.client.post(
            '/bucketlists/1/items/',
            data=json.dumps(self.item),
            content_type='application/json',
            headers={'Authorization': token['access_token']})
        print("asdfghjk", res.data.decode())
        self.assertEqual(201, res.status_code)

    def test_item_exist(self):
        """Test get item by id."""
        self.register()
        token = json.loads(self.login().data)
        res = self.client.post(
            '/bucketlists/',
            data=json.dumps(self.bucketlist),
            content_type='application/json',
            headers={'Authorization': token['access_token']})
        self.assertEqual(201, res.status_code)

        result = self.client.post(
            '/bucketlists/1/items/',
            data=json.dumps(self.item),
            content_type='application/json',
            headers={'Authorization': token['access_token']})
        self.assertEqual(201, result.status_code)

        rev = self.client.get(
            '/bucketlists/1/items/',
            headers={'Authorization': token['access_token']})
        self.assertEqual(200, rev.status_code)

    # put
    def test_item_can_be_edited(self):
        """Test  item editing."""
        self.register()
        token = json.loads(self.login().data)
        res = self.client.post(
            '/bucketlists/',
            data=json.dumps(self.bucketlist),
            content_type='application/json',
            headers={'Authorization': token['access_token']})
        self.assertEqual(201, res.status_code)

        result = self.client.post(
            '/bucketlists/1/items/',
            data=json.dumps(self.item),
            content_type='application/json',
            headers={'Authorization': token['access_token']})
        self.assertEqual(201, result.status_code)

        rev = self.client.put(
            '/bucketlists/1/items/1/',
            data=json.dumps({
                'item': 'learn ways of asians',
                "done": False}),
            content_type='application/json',
            headers={'Authorization': token['access_token']})
        print("++=======", rev.data.decode())

        result = self.client.get(
            '/bucketlists/1/items/1/',
            headers={'Authorization': token['access_token']},
            content_type='application/json')
        self.assertIn('learn ways of asians', str(result.data))

    def test_delete_item(self):
        """Test item  deletion."""
        self.register()
        token = json.loads(self.login().data)
        result = self.client.post(
            '/bucketlists/',
            data=json.dumps(self.bucketlist),
            content_type='application/json',
            headers={'Authorization': token["access_token"]})

        res = self.client.post(
            '/bucketlists/1/items/',
            data=json.dumps({
                'item': 'learn japaness',
                "done": False}),
            content_type='application/json',
            headers={"Authorization": token["access_token"]})
        self.assertEqual(201, res.status_code)

        rev = self.client.delete(
            '/bucketlists/1/items/1/',
            headers={"Authorization": token['access_token']},
            content_type='application/json')
        self.assertEqual(200, rev.status_code)

        result = self.client.get(
            '/bucketlists/1/items/1/',
            headers={"Authorization": token['access_token']})
        self.assertEqual(404, result.status_code)

    def tearDown(self):
        """Tear down setup fixtures."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
