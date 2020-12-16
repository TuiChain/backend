from django.test import SimpleTestCase
from django.urls import reverse, resolve
from tuichain.api.views import auth

class TestUrls(SimpleTestCase):
    
    # AUTHENTICATION ROUTES
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, auth.login)