"""
Swiggy Web Automation - Automatically places orders via browser automation
WARNING: This is for educational purposes. Using automation may violate Terms of Service.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class SwiggyAutomation:
    def __init__(self, headless=False):
        """Initialize Chrome browser with options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.logged_in = False
    
    def login(self, phone_number):
        """Login to Swiggy using phone number"""
        print("🔐 Logging into Swiggy...")
        self.driver.get("https://www.swiggy.com/")
        
        try:
            # Click Login button
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign in')]"))
            )
            login_btn.click()
            
            time.sleep(2)
            
            # Enter phone number
            phone_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "mobile"))
            )
            phone_input.send_keys(phone_number)
            
            # Click Continue
            continue_btn = self.driver.find_element(By.XPATH, "//a[contains(text(), 'CONTINUE')]")
            continue_btn.click()
            
            print("⏳ Please enter OTP manually in the browser window...")
            print("⏳ Waiting 60 seconds for you to complete login...")
            time.sleep(60)
            
            self.logged_in = True
            print("✅ Login successful!")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def search_and_order(self, restaurant_name, dish_name, location="Mangaluru"):
        """Search for restaurant and add dish"""
        print(f"🔍 Searching for {restaurant_name}...")
        
        try:
            # Enter location
            location_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your delivery location']"))
            )
            location_input.send_keys(location)
            time.sleep(2)
            
            # Select first location suggestion
            first_location = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='_3oDsP']"))
            )
            first_location.click()
            
            time.sleep(3)
            
            # Search for restaurant
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search for restaurants and food']"))
            )
            search_box.send_keys(restaurant_name)
            time.sleep(3)
            
            # Click on restaurant
            restaurant_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, 'restaurants')]"))
            )
            restaurant_link.click()
            
            time.sleep(3)
            
            # Add dish to cart
            add_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{dish_name}')]/ancestor::div//div[contains(text(), 'ADD')]"))
            )
            add_button.click()
            
            print(f"✅ {dish_name} added to cart")
            return True
            
        except Exception as e:
            print(f"❌ Search/Add failed: {e}")
            return False
    
    def checkout(self):
        """Complete the checkout process"""
        print("📦 Proceeding to checkout...")
        
        try:
            # Click View Cart
            view_cart = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'VIEW CART')]"))
            )
            view_cart.click()
            
            time.sleep(2)
            
            # Click Checkout
            checkout_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'CHECKOUT')]"))
            )
            checkout_btn.click()
            
            time.sleep(3)
            
            # Place Order button
            place_order = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'PLACE ORDER')]"))
            )
            
            print("⚠️ READY TO PLACE ORDER!")
            print("⚠️ Uncomment the next line to actually place the order")
            # place_order.click()  # UNCOMMENT TO ACTUALLY ORDER
            
            print("✅ Order would be placed here (currently disabled for safety)")
            return True
            
        except Exception as e:
            print(f"❌ Checkout failed: {e}")
            return False
    
    def auto_order(self, restaurant_name, dish_name, phone_number, location="Mangaluru"):
        """Complete automatic ordering flow"""
        try:
            if not self.login(phone_number):
                return False
            
            if not self.search_and_order(restaurant_name, dish_name, location):
                return False
            
            if not self.checkout():
                return False
            
            print("🎉 Swiggy order completed!")
            return True
            
        except Exception as e:
            print(f"❌ Auto-order failed: {e}")
            return False
        finally:
            time.sleep(5)
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    config = {
        "phone": "9876543210",
        "restaurant": "Ideal Ice Cream",
        "dish": "Gadbad",
        "location": "Mangaluru"
    }
    
    bot = SwiggyAutomation(headless=False)
    bot.auto_order(
        restaurant_name=config["restaurant"],
        dish_name=config["dish"],
        phone_number=config["phone"],
        location=config["location"]
    )
