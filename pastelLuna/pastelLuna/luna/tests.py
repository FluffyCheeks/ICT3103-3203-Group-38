import unittest
from .models import *


class test_Roles_Model(unittest.TestCase):
    def test_something_that_will_pass(self):
        customer = Roles.objects.get(id=1)
        administrator = Roles.objects.get(id=2)
        editor = Roles.objects.get(id=3)
        self.assertEqual(customer.role_desc, "shop")  # add assertion here
        self.assertEqual(administrator.role_desc, "db access")  # add assertion here
        self.assertEqual(editor.role_desc, "site editor")  # add assertion here

    def test_something_that_will_fail(self):
        customer = Roles.objects.get(id=1)
        administrator = Roles.objects.get(id=2)
        editor = Roles.objects.get(id=3)
        self.assertEqual(customer.role_desc, "db access")  # add assertion here
        self.assertEqual(administrator.role_desc, "site editor")  # add assertion here
        self.assertEqual(editor.role_desc, "shop")  # add assertion here


if __name__ == '__main__':
    print(__package__)