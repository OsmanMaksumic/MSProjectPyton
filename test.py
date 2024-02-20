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
import os
from xmlrunner import XMLTestRunner
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
        self.login.visit_google()
        self.login.enter_username()
        self.login.enter_password()
        self.login.submit_login()

    def test_click_menu(self):
        """User should be able to open Menu and Close it"""
        self.home.click_menu_button()

    def test_verify_footer_text(self):
        """Verify footer text"""
        self.home.verify_footer()

    def test_write_prices(self):
        """Write item names and prices in .txt file"""
        self.home.write_items_and_prices_into_txt_file()

    def test_login_logout(self):
        """Verify that user is logged in and then logout"""
        self.home.click_menu_button()
        self.home.click_logout()

    def test_verify_products(self):
        """Verify Products are displayed on the home page and verify its 6 of them"""
        self.home.verify_products()

    def test_add_item_to_cart(self):
        """Add 1 item to cart and verify it inside the cart"""
        self.home.add_backpack_into_cart()
        self.home.click_on_shopping_cart()
        self.home.verify_item_inside_cart()

    def test_add_all_items_to_cart_and_remove_them(self):
        """Add all 6 items to cart and remove them from cart"""
        self.home.add_each_item_to_cart()
        self.cart.verify_cart_badge_number()
        self.home.click_on_shopping_cart()
        self.cart.remove_each_item_from_cart()

    def test_add_1_item_and_checkout(self):
        """Add 1 item and proceed to checkout"""
        self.home.add_backpack_into_cart()
        self.home.click_on_shopping_cart()
        self.cart.click_on_checkout()
        self.cart.enter_checkout_information()
        self.cart.click_on_continue()
        self.cart.click_on_finish()
        self.cart.click_on_back_home()

    def test_verify_sorting_AZ(self):
        """Verify that items are sorted properly (A-Z)"""
        sort = "Name (A to Z)"
        self.home.verify_sorting()
        self.home.change_sorting(sort)

    def test_verify_sorting_ZA(self):
        """Verify that items are sorted properly (Z-A)"""
        sort = "Name (Z to A)"
        self.home.verify_sorting()
        self.home.change_sorting(sort)

    def test_verify_sorting_lio(self):
        """Verify that items are sorted properly Price(low-high)"""
        sort = "Price (low to high)"
        self.home.verify_sorting()
        self.home.change_sorting(sort)

    def test_test_verify_sorting_hio(self):
        """Verify that items are sorted properly Price(high-low)"""
        sort = "Price (high to low)"
        self.home.verify_sorting()
        self.home.change_sorting(sort)

    def test_write_into_file(self):
        """Write each item name into .txt file"""
        self.home.write_text()

    def test_read_from_file(self):
        """Read content of itemNames.txt"""
        self.home.read_text()

    def test_verify_footer_text(self):
        """Compare item names to JSON file"""
        self.home.compare_item_names_to_json()

    def test_compare_desc(self):
        """Compare item description to JSON file"""
        self.home.compare_item_description_to_json()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(myTestCase)

    # Run the tests using the XMLTestRunner
with open('test-reports/test_report.xml', 'wb') as output:
    runner = XMLTestRunner(output=output)
    runner.run(suite)
    
