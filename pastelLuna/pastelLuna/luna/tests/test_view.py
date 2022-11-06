from django.test import SimpleTestCase
from django.urls import reverse, resolve
from luna.models import *
from luna.views.home import *
from luna.views.loginpage import *
from luna.views.admin_dashboard import *
from luna.views.user import *
from luna.views.profile import *


# views unit test
# Test call sample urls


class test_views(SimpleTestCase):
    def setUp(self):
        self.shop_url = reverse('shop')
        self.home_url = reverse('profile')
        self.admin_url = reverse('admin_dashboard')
        self.editor_url = reverse('editor_dashboard')

    def test_route_GET(self):
        self.assertEqual(resolve(self.shop_url).func, shop)  # test access before login
        self.assertEqual(resolve(self.home_url).func, profile)  # test access after customer login
        self.assertEqual(resolve(self.admin_url).func, admin_dashboard) # test access admin dashboard
        self.assertEqual(resolve(self.editor_url).func, editor_dashboard) # test access editor dashboard
