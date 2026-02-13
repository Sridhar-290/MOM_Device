# 🍕 How to Enable REAL Food Ordering

This guide explains how to make your MOM device actually place real orders on Zomato or Swiggy.

## ⚠️ IMPORTANT WARNINGS

1. **This will place REAL orders and charge your account**
2. **You must manually enter OTP during the first login**
3. **This uses web automation which may violate Terms of Service**
4. **Use at your own risk - for educational purposes only**
5. **Test in mock mode first before enabling real orders**

---

## 📋 Prerequisites

### 1. Install Chrome Browser
The automation requires Google Chrome to be installed.

### 2. Install ChromeDriver
The automation will automatically download the correct ChromeDriver, but you can also install it manually:

**Windows:**
```powershell
# Using chocolatey
choco install chromedriver

# Or download from: https://chromedriver.chromium.org/
```

**Manual Installation:**
1. Download ChromeDriver from https://chromedriver.chromium.org/
2. Extract and add to your PATH

### 3. Install Python Dependencies
```bash
cd server
pip install -r requirements.txt
```

This will install:
- `selenium` - Browser automation
- `webdriver-manager` - Automatic ChromeDriver management

---

## 🔧 Configuration

### Step 1: Copy Environment File
```bash
cp .env.example .env
```

### Step 2: Edit `.env` File

Open `.env` and configure:

```bash
# Your Anthropic API Key (required)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# Enable REAL ordering (set to 'true' when ready)
ENABLE_REAL_ORDERS=false  # Change to 'true' to enable

# Choose platform: zomato or swiggy
FOOD_PLATFORM=zomato

# Your phone number (10 digits, no +91)
USER_PHONE=9876543210

# Your delivery location
USER_LOCATION=Mangaluru
```

---

## 🚀 How It Works

### Mock Mode (Default - Safe)
```
Growl Detected → AI Recommends Food → Prints to Console → No Real Order
```

### Real Order Mode (When ENABLE_REAL_ORDERS=true)
```
Growl Detected → AI Recommends Food → Opens Browser → Logs In → Searches Restaurant → Adds to Cart → Places Order
```

---

## 📝 Step-by-Step Usage

### Testing in Mock Mode (Recommended First)

1. **Keep `ENABLE_REAL_ORDERS=false` in `.env`**
2. **Run the server:**
   ```bash
   python app.py
   ```
3. **Trigger a test growl:**
   ```bash
   # In another terminal
   curl -X POST http://localhost:5000/detect -H "Content-Type: application/json" -d "{}"
   ```
4. **Check console output** - should show "MOCK MODE"

### Enabling Real Orders

1. **Update `.env`:**
   ```bash
   ENABLE_REAL_ORDERS=true
   USER_PHONE=your_actual_phone_number
   FOOD_PLATFORM=zomato  # or swiggy
   ```

2. **Run the server:**
   ```bash
   python app.py
   ```

3. **Trigger an order:**
   - When a growl is detected, a Chrome browser will open
   - **You must manually enter the OTP** when prompted
   - The browser will then automatically:
     - Search for the restaurant
     - Add the dish to cart
     - Navigate to checkout
     - **STOP before final confirmation** (for safety)

4. **Final Order Placement:**
   - By default, the script STOPS before clicking "Place Order"
   - To enable automatic final placement, edit the automation files:
   
   **In `zomato_automation.py` or `swiggy_automation.py`:**
   ```python
   # Find this line (around line 120):
   # place_order_button.click()  # UNCOMMENT TO ACTUALLY ORDER
   
   # Remove the # to enable:
   place_order_button.click()
   ```

---

## 🎯 Platform-Specific Notes

### Zomato
- Uses phone number + OTP login
- Requires manual OTP entry (60 second window)
- Works with saved addresses
- Supports most restaurants in India

### Swiggy
- Uses phone number + OTP login
- Requires manual OTP entry
- Location detection required
- May have different UI elements (update selectors if needed)

---

## 🐛 Troubleshooting

### "Element not found" errors
**Problem:** Website UI changed  
**Solution:** Update the XPath selectors in the automation files

### Browser doesn't open
**Problem:** ChromeDriver not installed  
**Solution:** Run `pip install webdriver-manager` and restart

### Login fails
**Problem:** OTP timeout  
**Solution:** Increase the wait time in the login function:
```python
time.sleep(60)  # Increase to 120 if needed
```

### Order doesn't complete
**Problem:** Address not selected  
**Solution:** Ensure you have saved addresses in your account

---

## 🔒 Security Recommendations

1. **Never commit your `.env` file** (it's in `.gitignore`)
2. **Use a separate payment method** with spending limits
3. **Set up order notifications** on your phone
4. **Test thoroughly in mock mode** first
5. **Monitor the first few real orders** manually

---

## 📊 Monitoring Orders

The system will print detailed logs:

```
--- ZOMATO ORDER TRIGGERED ---
ORDER: Fish Curry from Machali Restaurant
RATIONALE: High in Omega-3, anti-inflammatory
🚀 REAL ORDER MODE ENABLED - Using Web Automation
🔐 Logging into Zomato...
⏳ Please enter OTP manually in the browser window...
✅ Login successful!
🔍 Searching for Machali Restaurant...
✅ Found Machali Restaurant
🍽️ Adding Fish Curry to cart...
✅ Fish Curry added to cart
📦 Placing order...
⚠️ READY TO PLACE ORDER!
--- ✅ REAL ORDER PLACED SUCCESSFULLY ---
```

---

## 🎓 Educational Use Only

This project demonstrates:
- ✅ Audio signal processing (growl detection)
- ✅ AI integration (Claude for recommendations)
- ✅ Web automation (Selenium)
- ✅ IoT device integration (ESP32)

**Remember:** Automated ordering may violate platform Terms of Service. Use responsibly and at your own risk.

---

## 🆘 Getting Help

If you encounter issues:

1. Check the console logs for detailed error messages
2. Ensure Chrome and ChromeDriver versions match
3. Verify your `.env` configuration
4. Test with a simple manual Selenium script first
5. Check if the website UI has changed (update XPaths)

---

## 🔄 Switching Between Platforms

To switch from Zomato to Swiggy:

```bash
# In .env file
FOOD_PLATFORM=swiggy  # Change from zomato
```

The system will automatically use the correct automation script.
