# This test verifies that the system does not allow a login attempt with
# incorrect credentials and displays an appropriate error message.

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class InvalidLoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_invalid_login(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/accounts/login/")  # Navigate to the login page

        # Use invalid credentials
        invalid_username = "invaliduser"
        invalid_password = "wrongpassword"

        # Enter invalid credentials
        username_field = driver.find_element(By.ID, "id_username")
        password_field = driver.find_element(By.ID, "id_password")

        username_field.send_keys(invalid_username)
        password_field.send_keys(invalid_password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)

        # Check for the presence of an error message
        try:
            error_message = driver.find_element(By.XPATH, "//*[contains(text(), 'username and password')]")
            self.assertTrue(error_message.is_displayed(), "Error message for invalid login is not displayed.")
        except NoSuchElementException:
            self.fail("Error message not found for invalid login attempt.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
