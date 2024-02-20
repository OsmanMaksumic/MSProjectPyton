from selenium.webdriver.common.by import By
from configparser import ConfigParser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class loginPage:

    username = (By.ID, 'user-name')
    password = (By.ID, 'password')
    login_button = (By.ID, 'login-button')

    def __init__(self, driver):
        self.driver = driver
        self.config = ConfigParser()
        self.config.read('fixtures/login_config.ini')

    def visit_google(self):
        self.driver.get("https://www.saucedemo.com")

    def enter_username(self):
        username_input = self.config.get('loginData', 'username')
        entering_username = self.driver.find_element(*self.username)
        entering_username.clear()
        entering_username.send_keys(username_input)
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element_value(self.username, username_input))

    def enter_password(self):
        password_input = self.config.get('loginData', 'password')
        entering_password = self.driver.find_element(*self.password)
        entering_password.clear()
        entering_password.send_keys(password_input)
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element_value(self.password, password_input))

    def submit_login(self):
        submit_login = self.driver.find_element(*self.login_button)
        submit_login.click()
