from unittest import TestCase
from main import app

class TestStuff(TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def login(self, username):
        return self.client.post('/login', data={'username': 'admin'},
                                follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_public(self):
        rv = self.client.get('/')
        self.assertTrue(b'Public' in rv.data)

    def test_redirect(self):
        rv = self.client.get('/redirect', follow_redirects=True)
        self.assertTrue(b'Public' in rv.data)

    def test_restricted(self):
        self.login('admin')
        rv = self.client.get('/restricted', follow_redirects=True)
        self.assertTrue(b'Restricted' in rv.data)

    def test_restricted_not_accessible_if_not_logged_in(self):
        rv = self.client.get('/restricted', follow_redirects=True)
        self.assertTrue(b'Login page' in rv.data)
