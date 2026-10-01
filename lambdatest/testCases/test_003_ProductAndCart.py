from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import quote_plus

from pageObjects.HomePage import HomePage


BASE_URL = "https://ecommerce-playground.lambdatest.io/"


class Test_ProductAndCart:
    def open_store(self, driver):
        driver.get(BASE_URL)
        HomePage(driver).acceptCookies()
        return WebDriverWait(driver, 10)

    def search_for(self, driver, term):
        wait = self.open_store(driver)
        driver.get(
            f"{BASE_URL}index.php?route=product/search&search={quote_plus(term)}"
        )
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        return wait

    def test_product_search_returns_matching_results(self, setup):
        driver = setup
        wait = self.search_for(driver, "iPhone")

        products = wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb"))
        )

        assert products, "Expected at least one product result for iPhone"
        assert any("iphone" in product.text.lower() for product in products)

    def test_product_search_shows_no_results_message(self, setup):
        driver = setup
        wait = self.search_for(driver, "product-that-does-not-exist-qa")

        page_text = wait.until(lambda current_driver: current_driver.find_element(By.TAG_NAME, "body").text)

        assert "There is no product that matches the search criteria" in page_text

    def test_add_product_to_cart(self, setup):
        driver = setup
        wait = self.search_for(driver, "iPhone")

        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".product-thumb button[title='Add to Cart']")
            )
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",
            add_to_cart,
        )

        driver.get(f"{BASE_URL}index.php?route=checkout/cart")
        assert wait.until(
            lambda current_driver: "iPhone" in current_driver.find_element(
                By.TAG_NAME, "body"
            ).text
        )

