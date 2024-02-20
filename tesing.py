from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageObjects.login_page import loginPage
from pageObjects.home_page import homePage
from pageObjects.cart_page import cartPage
from configparser import ConfigParser
import unittest
import json
import os
import time


class myTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.login = loginPage(self.driver)
        self.home = homePage(self.driver)
        self.cart = cartPage(self.driver)
        self.perform_login()

    def tearDown(self):
        # Add any additional cleanup steps you need here.
        pass

    def perform_login(self):
        """Common login procedure"""
        login = loginPage(self.driver)
        login.visit_google()
        login.enter_username()
        login.enter_password()
        login.submit_login()

    def test_write_prices(self):
        self.home.write_items_and_prices_into_txt_file()


if __name__ == '__main__':
    unittest.main()
