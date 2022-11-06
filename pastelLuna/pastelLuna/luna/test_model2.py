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
        submitbutton.send_keys(Keys.RETURN)