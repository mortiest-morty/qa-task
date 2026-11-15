import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

SAUCEDEMO_URL = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com")
SAUCE_USERNAME = os.getenv("SAUCE_USERNAME", "standard_user")
SAUCE_PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")


@pytest.fixture
def driver():
    options = Options()

    if os.getenv("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.browser_version = "157"   
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(2)

    yield browser

    browser.quit()


def test_complete_purchase(driver):
    wait = WebDriverWait(driver, 20)

    driver.get(SAUCEDEMO_URL)

    wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys(SAUCE_USERNAME)

    driver.find_element(By.ID, "password").send_keys(SAUCE_PASSWORD)
    driver.find_element(By.ID, "login-button").click()

    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    backpack = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "add-to-cart-sauce-labs-backpack")
        )
    )
    backpack.click()

    cart_badge = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert cart_badge.text == "1"

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "cart_item"))
    )

    item_name = driver.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text
    assert item_name == "Sauce Labs Backpack"

    driver.find_element(By.ID, "checkout").click()

    wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    ).send_keys("Test")

    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    finish_button = wait.until(
        EC.presence_of_element_located((By.ID, "finish"))
    )
    
    driver.execute_script("arguments[0].scrollIntoView(true);", finish_button)
    
    wait.until(EC.element_to_be_clickable((By.ID, "finish")))

    overview_item = driver.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text
    assert overview_item == "Sauce Labs Backpack"

    driver.find_element(By.ID, "finish").click()

    success_message = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "complete-header")
        )
    )

    assert success_message.text == "Thank you for your order!"
    assert "/checkout-complete.html" in driver.current_url