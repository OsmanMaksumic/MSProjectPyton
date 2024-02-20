from selenium.webdriver.common.by import By
from configparser import ConfigParser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class homePage:

    item_name_element = '.inventory_item_name'
    items_elements = '.inventory_item'
    item_prices_element = '.inventory_item_price'

    menu_button = (By.ID, 'react-burger-menu-btn')
    footer_text = (By.CSS_SELECTOR, '.footer_copy')
    logout_bottom = (By.ID, 'logout_sidebar_link')
    inventory_container_items = (By.CSS_SELECTOR, '.inventory_list')
    inventory_container_name = (By.CSS_SELECTOR, '.inventory_item')
    add_backpack_to_cart = (By.ID, 'add-to-cart-sauce-labs-backpack')
    remove_backpack_from_cart = (By.ID, 'remove-sauce-labs-backpack')
    shopping_cart_container = (By.ID, 'shopping_cart_container')
    cart_inventory_item_name = (By.CSS_SELECTOR, '.inventory_item_name')
    add_to_cart_each = (By.CSS_SELECTOR, '.btn_primary')
    sort_menu = (By.CSS_SELECTOR, '[data-test="product_sort_container"]')
    item_desc = (By.CSS_SELECTOR, '.inventory_item_desc')

    def write_items_and_prices_into_txt_file(self):
        with open('itemNamesAndPrices.txt', 'w') as file:
            elements = self.driver.find_elements(
                By.CSS_SELECTOR, self.items_elements)
            for index, element in enumerate(elements):
                name_element = element.find_element(
                    By.CSS_SELECTOR, self.item_name_element)
                item_name = name_element.text
                price_element = element.find_element(
                    By.CSS_SELECTOR, self.item_prices_element)
                item_price = price_element.text
                item_data = f'{item_name} - {item_price}\n'
                file.write(item_data)

    def __init__(self, driver):
        self.driver = driver
        self.home_config = ConfigParser()
        self.home_config.read('fixtures/home_page_config.ini')
        self.items_config = ConfigParser()
        self.items_config.read('fixtures/items_config.ini')

    def click_menu_button(self):
        click_menu = self.driver.find_element(*self.menu_button)
        click_menu.click()

    def click_logout(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((self.logout_bottom)))
        element.click()

    def verify_products(self):
        parent_element = self.driver.find_element(
            *self.inventory_container_items)
        child_element = parent_element.find_elements(
            *self.inventory_container_name)
        expected_count = 6
        actual_count = len(child_element)
        assert actual_count == expected_count

    def add_backpack_into_cart(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((self.add_backpack_to_cart)))
        element.click()
        element2 = WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(self.remove_backpack_from_cart, 'Remove'))

    def click_on_shopping_cart(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((self.shopping_cart_container)))
        element.click()
        expected_substring = "/cart.html"
        current_url = self.driver.current_url
        assert expected_substring in current_url

    def verify_item_inside_cart(self):
        text = self.items_config.get('itemsData', 'backpack_item')
        element = self.driver.find_element(*self.cart_inventory_item_name)
        assert text in element.text

    def verify_footer(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        expected_text = self.home_config.get('homeData', 'footer_text')
        footer = self.driver.find_element(
            *self.footer_text)  # Find the footer element
        ft_text = footer.text
        print(expected_text)
        print(ft_text)
        assert expected_text in ft_text

    def add_each_item_to_cart(self):
        elements = self.driver.find_elements(*self.add_to_cart_each)
        for element in elements:
            element.click()

    def verify_sorting(self):
        # Locate and collect the text of elements
        elements = self.driver.find_elements(*self.shopping_cart_container)
        elements_text = [element.text for element in elements]
        # Create an expected sorted version of the data
        expected_sorted_data = sorted(elements_text)
        # Verify that the actual data is equal to the sorted data
        assert elements_text == expected_sorted_data

    def change_sorting(self, sort):
        # Locate the sort menu element (replace 'your_sort_menu' with the correct locator)
        sort_menu = self.driver.find_element(*self.sort_menu)
        # Create a Select object to interact with the dropdown menu
        select = Select(sort_menu)
        # Select the sorting option by visible text
        select.select_by_visible_text(sort)

    def write_text(self):
        elements = self.driver.find_elements(*self.cart_inventory_item_name)
        with open('itemNames.txt', 'w') as file:
            for element in elements:
                text = element.text
                file.write(text + '\n')

    def read_text(self):
        with open('itemNames.txt', 'r') as file:
            content = file.read()
        print(content)

    def compare_item_names_to_json(self):
        elements = self.driver.find_elements(*self.cart_inventory_item_name)

        with open('itemsData.json', 'r') as json_file:
            data = json.load(json_file)
            item_names_array = data['item_names']

        # Iterate through item_names_array and compare to the elements on the webpage
        for element in elements:
            element_name = element.text.strip()

            found = False
            for key, expected_item_name in item_names_array.items():
                if element_name.lower() == expected_item_name.lower():
                    found = True
                    break

            if not found:
                raise AssertionError(f"No matching element found for item name {
                                     element_name} in the JSON data.")

    def compare_item_description_to_json(self):
        elements = self.driver.find_elements(*self.item_desc)

        with open('itemsData.json', 'r') as json_file:
            data = json.load(json_file)
            item_names_array = data['item_description']

        # Iterate through item_names_array and compare to the elements on the webpage
        for element in elements:
            element_name = element.text.strip()

            found = False
            for key, expected_item_name in item_names_array.items():
                if element_name.lower() == expected_item_name.lower():
                    found = True
                    break

            if not found:
                raise AssertionError(f"No matching element found for item name {
                                     element_name} in the JSON data.")
