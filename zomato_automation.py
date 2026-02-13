"""
Zomato Web Automation - Automatically places orders via browser automation
WARNING: This is for educational purposes. Using automation may violate Terms of Service.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json

class ZomatoAutomation:
    def __init__(self, headless=False):
        """Initialize Chrome browser with options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.logged_in = False
    
    def login(self, phone_number):
        """
        Login to Zomato using phone number
        Note: You'll need to manually enter OTP
        """
        print("🔐 Logging into Zomato...")
        self.driver.get("https://www.zomato.com/")
        
        try:
            # Click Login button
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Log in')]"))
            )
            login_btn.click()
            
            # Enter phone number
            phone_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "phone"))
            )
            phone_input.send_keys(phone_number)
            
            # Click Continue
            continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
            continue_btn.click()
            
            print("⏳ Please enter OTP manually in the browser window...")
            print("⏳ Waiting 60 seconds for you to complete login...")
            time.sleep(60)  # Wait for manual OTP entry
            
            self.logged_in = True
            print("✅ Login successful!")
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
        
        return True
    
    def search_restaurant(self, restaurant_name, location="Mangaluru"):
        """Search for a restaurant"""
        print(f"🔍 Searching for {restaurant_name} in {location}...")
        
        try:
            # Set location
            location_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your delivery location']"))
            )
            location_input.clear()
            location_input.send_keys(location)
            time.sleep(2)
            
            # Click first suggestion
            first_suggestion = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='sc-1mo3ldo-0']//p"))
            )
            first_suggestion.click()
            
            # Search for restaurant
            search_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search for restaurant, cuisine or a dish']"))
            )
            search_input.send_keys(restaurant_name)
            time.sleep(3)
            
            # Click on restaurant
            restaurant_card = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{restaurant_name.lower()}')]"))
            )
            restaurant_card.click()
            
            print(f"✅ Found {restaurant_name}")
            return True
            
        except Exception as e:
            print(f"❌ Restaurant search failed: {e}")
            return False
    
    def add_to_cart(self, dish_name):
        """Add a dish to cart"""
        print(f"🍽️ Adding {dish_name} to cart...")
        
        try:
            # Find the dish and click ADD button
            add_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{dish_name}')]/ancestor::div//button[contains(text(), 'ADD')]"))
            )
            add_button.click()
            
            time.sleep(2)
            print(f"✅ {dish_name} added to cart")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add dish: {e}")
            return False
    
    def place_order(self, address_index=0):
        """
        Place the order
        address_index: Which saved address to use (0 = first address)
        """
        print("📦 Placing order...")
        
        try:
            # Click on cart
            cart_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'View Cart')]"))
            )
            cart_button.click()
            
            time.sleep(2)
            
            # Click Proceed to Pay
            proceed_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Proceed to Pay')]"))
            )
            proceed_button.click()
            
            time.sleep(3)
            
            # Select address (use first saved address)
            # This part varies based on your saved addresses
            
            # Click Place Order
            place_order_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Place Order')]"))
            )
            
            print("⚠️ READY TO PLACE ORDER!")
            print("⚠️ Uncomment the next line to actually place the order")
            # place_order_button.click()  # UNCOMMENT THIS TO ACTUALLY ORDER
            
            print("✅ Order would be placed here (currently disabled for safety)")
            return True
            
        except Exception as e:
            print(f"❌ Order placement failed: {e}")
            return False
    
    def auto_order(self, restaurant_name, dish_name, phone_number):
        """
        Complete automatic ordering flow
        """
        try:
            # Step 1: Login
            if not self.login(phone_number):
                return False
            
            # Step 2: Search restaurant
            if not self.search_restaurant(restaurant_name):
                return False
            
            # Step 3: Add dish to cart
            if not self.add_to_cart(dish_name):
                return False
            
            # Step 4: Place order
            if not self.place_order():
                return False
            
            print("🎉 Order completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Auto-order failed: {e}")
            return False
        finally:
            time.sleep(5)
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    # Configuration
    config = {
        "phone": "9876543210",  # Your phone number
        "restaurant": "Pabbas Ice Cream",
        "dish": "Gudbud"
    }
    
    # Create automation instance
    bot = ZomatoAutomation(headless=False)  # Set True to hide browser
    
    # Run automatic ordering
    bot.auto_order(
        restaurant_name=config["restaurant"],
        dish_name=config["dish"],
        phone_number=config["phone"]
    )
