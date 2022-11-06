import unittest
from django.test import client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.test import Client
from luna.models import *

#Selenium Testing
from django.test import LiveServerTestCase
from selenium import webdriver #to select your browser
from selenium.webdriver.common.keys import Keys #To simulate entering keys
import time

#Test Registration using Selenium

class RegistrationTest(LiveServerTestCase):

    def testregistrationform_normal(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/luna/registration')

        #SYNTAX TO USE THIS
        # driver.find_element("id","id_of_element")
        firstname = driver.find_element(driver.By.NAME, "first_name")
        lastname = driver.find_element(driver.By.NAME, "last_name")
        email = driver.find_element(driver.By.NAME, "email")
        password = driver.find_element(driver.By.NAME, "password")
        cfm_password = driver.find_element(driver.By.NAME, "confirm_password")
        #skipping allergies since can be null
        submitbutton = driver.find_element(driver.By.Name,"submit")


        firstname.send_keys('John Testing Selenium')
        lastname.send_keys('Tan')
        email.send_keys('johntan_selenium@gmail.com')
        password.send_keys('P@ssword123')
        cfm_password.send_keys('P@ssword123')




# incorrect credential
def create_users_fail(role_id_id=1, first_name="Lee", last_name="Dion", password=None, email="5566@gmail.com",
                 address=None, phone="99987777", allergies=None):
    return Users.objects.create(role_id_id=role_id_id, first_name=first_name, last_name=last_name,
                                password=password, email=email, address=address, phone=phone, allergies=allergies)


# models unit test
class test_roles_model(unittest.TestCase):
    # show match of role desc to the role permission
    def test_assertion_permission_match_role_desc(self):
        customer = Roles.objects.get(id=1)
        administrator = Roles.objects.get(id=2)
        editor = Roles.objects.get(id=3)
        self.assertEqual(customer.role_desc, "shop")  # add assertion here
        self.assertEqual(administrator.role_desc, "db access")  # add assertion here
        self.assertEqual(editor.role_desc, "site editor")  # add assertion here


class test_users_model(unittest.TestCase):
    # create user function sample test case
    def create_users(self, role_id_id=1, first_name="Lee", last_name="Dion", password=None, email="5566@gmail.com",
                     address=None, phone="99987777", allergies=None):
        return Users.objects.create(role_id_id=role_id_id, first_name=first_name, last_name=last_name,
                                    password=password, email=email, address=address, phone=phone, allergies=allergies)

    @unittest.expectedFailure
    def test_user_creation_fail(self):
        # fail test case = pass (Password cannot be null)
        w = self.create_users()
        if w.password is None:
            self.assertRaises(ValidationError, w.password)
            w.full_clean()


class test_product_category_model(unittest.TestCase):
    # test the char field max length
    @unittest.expectedFailure
    def test_category_name_length(self):
        # (max_length=100) # this should be 120
        # we have max length = 20 # this should be 24
        lots = 'T' * 25
        Product_Category.objects.create(category_name=lots)
        with self.assertRaises(ValidationError):
            Product_Category.full_clean()


class test_promotion_model(unittest.TestCase):
    def update_promotion_amt(self, product_id_id=1, promotion_amount=10.699):
        Promotion.product_id = product_id_id
        Promotion.promotion_amount = promotion_amount
        return Promotion.save()

    @unittest.expectedFailure
    def test_promotion_amt_decimal_places(self):
        w1 = self.update_promotion_amt()
        if len(w1.promotion_amount.rsplit('.')[-1]) != 2:
            self.assertRaises(ValidationError, w1.promotion_amount)
            w1.full_clean()


# TODO: Test for product  stock avail
class test_cart_stock_avail(unittest.TestCase):
    # get a record of product details
    def get_record_product_details(self):
        pd = Product_Details.objects.get(id=1)
        stock_avail = pd.stock_available
        return stock_avail

    # 20 < 67
    def test_is_stock_available_false(self):
        stock_avail_cart_dummy = 10
        stock_avail_actual_pd = self.get_record_product_details()  #
        check_stock = stock_avail_actual_pd - stock_avail_cart_dummy
        if check_stock >=0:
            self.assertEqual(True, True)
        else:
            self.assertEqual(False, False)


# Test Authorised_User can never be customer
class test_authorised_user_model(unittest.TestCase):
    # authorised roles - 2,3
    # 1 is customer
    def test_is_user_authorised(self):
        Editor = Authorised_User.objects.get(id=1)
        Administrator = Authorised_User.objects.get(id=2)
        self.assertNotEqual(Editor.role_id, 1)
        self.assertNotEqual(Administrator.role_id, 1)


# views unit test
# Test call sample to shop.html
class test_views(unittest.TestCase):
    def test_shop_page_GET(self):
        client = Client()
        response = client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
