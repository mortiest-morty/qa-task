import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_complete_purchase():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.browser_version = "157"

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.saucedemo.com")

        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))

        backpack = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
        backpack.click()

        cart_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        assert cart_badge.text == "1"

        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_item")))

        item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        assert item_name == "Sauce Labs Backpack"

        driver.find_element(By.ID, "checkout").click()

        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()

        finish_button = wait.until(EC.presence_of_element_located((By.ID, "finish")))
        driver.execute_script("arguments[0].scrollIntoView(true);", finish_button)
        wait.until(EC.element_to_be_clickable((By.ID, "finish")))

        driver.find_element(By.ID, "finish").click()

        success_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))
        assert success_message.text == "Thank you for your order!"
    
    finally:
        driver.quit()