from unittest import TestCase
from main import app
from csrf_decorator import FlaskClient

class TestStuff(TestCase):
    def setUp(self):
        app.testing = True
        # app.config['WTF_CSRF_ENABLED'] = False
        app.test_client_class = FlaskClient
        self.client = app.test_client()
        app.app_context().push()

    def test_01_public(self):
        rv = self.client.get('/')
        self.assertTrue(b'Public' in rv.data)

    def test_02_redirect(self):
        rv = self.client.get('/redirect', follow_redirects=True)
        self.assertTrue(b'Public' in rv.data)

    def test_03_restricted(self):
        self.client.login('admin', 'password')
        rv = self.client.get('/restricted', follow_redirects=True)
        self.assertTrue(b'Restricted' in rv.data)

    def test_04_restricted_not_accessible_if_not_logged_in(self):
        rv = self.client.get('/restricted', follow_redirects=True)
        self.assertTrue(b'Log in' in rv.data)
