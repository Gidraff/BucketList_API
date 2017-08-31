import unittest
from app import create_app, db



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
            db.drop_all()
            db.create_all()
    