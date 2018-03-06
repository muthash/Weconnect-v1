import unittest
import json
from app import create_app


class AuthTestCase(unittest.TestCase):
    """Test case for the user creation and login"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.business = {
            'businessName': 'Kenya Power',
            'category': 'Lighting',
            'location': 'Nairobi'
        }

    def register_user(self, email="business@test.com", username="stephen", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {'email': email, 'username': username, 'password': password}
        return self.client().post(
                '/api/v1/register',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def login_user(self, email="business@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {'email': email, 'password': password}
        return self.client().post(
                '/api/v1/login',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def test_business_creation(self):
        """Test the API can create a bussiness (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/api/v1/businesses',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + access_token},
            data=json.dumps(self.business))
        bizIds = json.loads(res.data.decode())['business']
        self.assertIsInstance(bizIds, list)
        self.assertTrue(bizIds)
        self.assertIn(1, bizIds)
        self.assertEqual(res.status_code, 201)

    def test_get_all_businesses(self):
        """Test the API can create a bussiness (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/api/v1/businesses',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + access_token},
            data=json.dumps(self.business)
        )
        res = self.client().get(
            '/api/v1/businesses',
            headers={'Authorization': 'Bearer ' + access_token}
        )
        biz = json.loads(res.data.decode())
        self.assertTrue(biz)
        self.assertEqual(res.status_code, 200)

    def test_api_can_get_business_by_id(self):
        """Test API can get a single business by using it's Id"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/api/v1/businesses',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + access_token},
            data=json.dumps(self.business)
        )
        bizIds = json.loads(res.data.decode())['business']
        result2 = self.client().get(
            '/api/v1/businesses/{}'.format(bizIds[0]),
            headers={'Authorization': 'Bearer ' + access_token}
        )
        self.assertEqual(result2.status_code, 200)
        self.assertIn('Kenya Power', str(result2.data))
