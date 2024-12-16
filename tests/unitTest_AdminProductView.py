# This test validates that an admin can log in and access the admin product view page.

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

class AdminProductViewTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_admin_product_view(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/accounts/login/")  # Navigate to the login page

        try:
            # Admin login credentials
            username = "jacoby"
            password = "superuser"

            # Locate and fill the login form
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")

            username_input.send_keys(username)
            password_input.send_keys(password)
            login_button.click()  # Click the login button
            time.sleep(2)

            # Verify successful login by checking for the Admin Function link
            admin_function_tab = driver.find_element(By.LINK_TEXT, "Admin Function")
            admin_function_tab.click()
            time.sleep(1)

            # Navigate to Admin Product View
            product_view_link = driver.find_element(By.LINK_TEXT, "Admin Product View")
            product_view_link.click()
            time.sleep(2)

            # Verify Admin Product View page loads
            header = driver.find_element(By.TAG_NAME, "h2")
            self.assertEqual(header.text, "Admin", "Admin Product View page did not load correctly.")

        except (NoSuchElementException, ElementNotInteractableException) as e:
            self.fail(f"Admin Product View page elements not found or not interactable: {e}")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

