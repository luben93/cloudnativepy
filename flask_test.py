from app import app
import unittest


class FlaskappTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    def test_user_status_code(self):
        result = self.app.get('/api/v1/users')
        self.assertEqual(result.status_code,200)

    def test_tweets_status_code(self):
        result = self.app.get('/api/v2/tweets')
        self.assertEqual(result.status_code,200)

    def test_info_status_code(self):
        result = self.app.get('/api/v1/info')
        self.assertEqual(result.status_code,200)

    def test_add_user_status_code(self):
        result = self.app.post('/api/v1/users',data='{"username":"luben","email":"luben@mail.abc","password":"secret"}',content_type='application/json')
        print(result)
        self.assertEqual(result.status_code,201)

    def test_update_user_status_code(self):
        result = self.app.put('/api/v1/users/2',data='{"password":"not a secret anymore"}',content_type='application/json')
        self.assertEqual(result.status_code,200)

    def test_add_tweets_status_code(self):
        result = self.app.post('/api/v2/tweets',data='{"username":"luben","body":"cool tweet bro #testing"}',content_type='application/json')
        self.assertEqual(result.status_code,200)

    def test_delete_user_status_code(self):
        result = self.app.delete('/api/v1/users',data='{"username":"luben"}',content_type='application/json')
        self.assertEqual(result.status_code,200)


