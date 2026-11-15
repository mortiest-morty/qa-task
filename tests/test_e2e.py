import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_complete_purchase():
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.saucedemo.com")
        time.sleep(2) 

        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        time.sleep(2)

        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "1"

        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)

        item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        assert item_name == "Sauce Labs Backpack"

        driver.find_element(By.ID, "checkout").click()
        time.sleep(2)

        driver.find_element(By.ID, "first-name").send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()

        driver.find_element(By.ID, "finish").click()

        success_message = driver.find_element(By.CLASS_NAME, "complete-header")
        assert success_message.text == "Thank you for your order!"
    
    finally:
        driver.quit()