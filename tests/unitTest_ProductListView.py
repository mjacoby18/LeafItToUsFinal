# This test validates that products are displayed correctly on the home page.

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class ProductListViewTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_product_list_view(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/")  # Navigate to the home page

        try:
            # Check for the product list container
            product_list = driver.find_element(By.CLASS_NAME, "product-list")
            items = product_list.find_elements(By.CLASS_NAME, "item")

            # Verify at least one product is listed
            self.assertGreater(len(items), 0, "No products found on the home page.")

        except NoSuchElementException as e:
            self.fail(f"Product elements not found on the home page: {e}")

        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

