from selenium.webdriver.common.by import By
from configparser import ConfigParser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class cartPage:

    remove_from_cart_each = (By.CSS_SELECTOR, '.btn_secondary')
    shopping_cart_badge = (By.CSS_SELECTOR, '.shopping_cart_badge')
    checkout = (By.ID, 'checkout')
    title = (By.CSS_SELECTOR, '.title')
    cart_inventory_item_name = (By.CSS_SELECTOR, '.inventory_item_name')

    checkout_first_name = (By.ID, 'first-name')
    checkout_last_name = (By.ID, 'last-name')
    checkout_postal_code = (By.ID, 'postal-code')

    continue_button = (By.ID, 'continue')
    finish = (By.ID, 'finish')
    back_home_button = (By.ID, 'back-to-products')

    def __init__(self, driver):
        self.driver = driver
        self.login_config = ConfigParser()
        self.login_config.read('fixtures/login_config.ini')
        self.items_config = ConfigParser()
        self.items_config.read('fixtures/items_config.ini')

    def verify_cart_badge_number(self):
        # Get the count of elements in the cart
        elements = self.driver.find_elements(*self.remove_from_cart_each)
        elementCount = len(elements)
    # Locate the cart badge element
        cart_badge = self.driver.find_element(*self.shopping_cart_badge)
    # Verify that the cart badge text matches the element count
        assert cart_badge.text == str(elementCount), f"Cart badge count doesn't match: expected {
            elementCount}, but found {cart_badge.text}"

    def remove_each_item_from_cart(self):
        elements = self.driver.find_elements(*self.remove_from_cart_each)
        for element in elements:
            element.click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/inventory.html'))

    def click_on_checkout(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.checkout))
        element.click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/checkout-step-one.html'))
        element2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.title))
        assert 'Checkout: Your Information' in element2.text

    def enter_checkout_information(self):
        # Locate and interact with the input fields (replace with the correct locators)
        first_name_field = self.driver.find_element(*self.checkout_first_name)
        last_name_field = self.driver.find_element(*self.checkout_last_name)
        postal_code_field = self.driver.find_element(
            *self.checkout_postal_code)

        first_name = self.login_config.get('loginData', 'first_name')
        last_name = self.login_config.get('loginData', 'last_name')
        postal_code = self.login_config.get('loginData', 'zip')

        # Enter data into the input fields and verify their values
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        assert first_name_field.get_attribute("value") == first_name

        last_name_field.clear()
        last_name_field.send_keys(last_name)
        assert last_name_field.get_attribute("value") == last_name

        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)
        assert postal_code_field.get_attribute("value") == postal_code

    def click_on_continue(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.continue_button))
        element.click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/checkout-step-two.html'))
        element2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.title))
        assert 'Checkout: Overview' in element2.text
        element3 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.cart_inventory_item_name))
        item = self.items_config.get('itemsData', 'backpack_item')
        assert item in element3.text

    def click_on_finish(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.finish))
        element.click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/checkout-complete.html'))
        element2 = WebDriverWait(self.driver, 10). until(
            EC.visibility_of_element_located(self.title))
        assert 'Checkout: Complete!' in element2.text

    def click_on_back_home(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.back_home_button))
        element.click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/inventory.html'))
        element2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.title))
        assert 'Products' in element2.text
