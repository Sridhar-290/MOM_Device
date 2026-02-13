import os
import time
import json
from flask import Flask, request, jsonify, render_template
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Config
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your_api_key_here")
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

# State to track growls & Medical Data
growl_events = []
WINDOW_SIZE = 120 
MIN_GROWLS_FOR_ORDER = 3 
LAST_ORDER_TIME = 0
MUTE_DURATION = 3600 

# Default Medical Profile (Updated via /setup)
USER_MEDICAL_PROFILE = {
    "conditions": [], 
    "critical_restrictions": [],
    "health_goals": "Stay healthy"
}

def get_claude_recommendation(is_big_meal=False):
    """
    Claude acts as a Medical Nutritionist + Local Food Guide.
    """
    prompt = f"""
    Internal State: User is hungry. 
    Meal Size Request: {'Big' if is_big_meal else 'Small'}.
    
    PATIENT MEDICAL RECORD:
    - Conditions: {', '.join(USER_MEDICAL_PROFILE['conditions'])}
    - Restrictions: {', '.join(USER_MEDICAL_PROFILE['critical_restrictions'])}
    - Goals: {USER_MEDICAL_PROFILE['health_goals']}
    
    MANAGEMENT RULES:
    1. JOINT/LUNG HEALTH: Prioritize anti-inflammatory foods (Ginger, Turmeric, Omega-3s).
    2. DIABETES: Strict Zero-Sugar. Max fiber. No white rice/maida.
    3. BP/HEART: Zero deep-fry. Low salt. No processed meats.
    4. OBESITY: Focus on nutrient density over calorie density.
    
    TASK: Recommend a specific dish from a Mangaluru restaurant that fits these strict medical needs.
    Format your response as a JSON: {{"restaurant": "Name", "dish": "Dish Name", "rationale": "Medical Rationale"}}
    """
    
    try:
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error calling Claude: {e}")
        return '{"restaurant": "Pabbas", "dish": "Gudbud", "rationale": "Fallback"}'

def place_zomato_order(order_details):
    """
    Place order on Zomato
    Set ENABLE_REAL_ORDERS=true in .env to use web automation
    Otherwise uses mock/simulation mode
    """
    ENABLE_REAL_ORDERS = os.getenv("ENABLE_REAL_ORDERS", "false").lower() == "true"
    PLATFORM = os.getenv("FOOD_PLATFORM", "zomato").lower()  # zomato or swiggy
    USER_PHONE = os.getenv("USER_PHONE", "")
    USER_LOCATION = os.getenv("USER_LOCATION", "Mangaluru")
    
    print(f"--- {PLATFORM.upper()} ORDER TRIGGERED ---")
    print(f"ORDER: {order_details.get('dish')} from {order_details.get('restaurant')}")
    print(f"RATIONALE: {order_details.get('rationale')}")
    
    if ENABLE_REAL_ORDERS and USER_PHONE:
        print("🚀 REAL ORDER MODE ENABLED - Using Web Automation")
        try:
            if PLATFORM == "zomato":
                from zomato_automation import ZomatoAutomation
                bot = ZomatoAutomation(headless=False)
                success = bot.auto_order(
                    restaurant_name=order_details.get('restaurant'),
                    dish_name=order_details.get('dish'),
                    phone_number=USER_PHONE
                )
            elif PLATFORM == "swiggy":
                from swiggy_automation import SwiggyAutomation
                bot = SwiggyAutomation(headless=False)
                success = bot.auto_order(
                    restaurant_name=order_details.get('restaurant'),
                    dish_name=order_details.get('dish'),
                    phone_number=USER_PHONE,
                    location=USER_LOCATION
                )
            else:
                print(f"❌ Unknown platform: {PLATFORM}")
                success = False
            
            if success:
                print(f"--- ✅ REAL ORDER PLACED SUCCESSFULLY ---")
            else:
                print(f"--- ❌ ORDER FAILED ---")
            return success
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            print("Falling back to mock mode...")
    
    # Mock mode (default)
    print("📝 MOCK MODE - No real order placed (simulation only)")
    print(f"--- ORDER SUCCESSFUL (SIMULATED) ---")
    return True

@app.route('/')
def home():
    return render_template('setup.html', profile=USER_MEDICAL_PROFILE)

@app.route('/setup', methods=['POST'])
def setup():
    global USER_MEDICAL_PROFILE
    USER_MEDICAL_PROFILE['conditions'] = request.form.getlist('conditions')
    USER_MEDICAL_PROFILE['critical_restrictions'] = request.form.get('restrictions', '').split(',')
    USER_MEDICAL_PROFILE['health_goals'] = request.form.get('goals', 'Healthy living')
    return render_template('setup.html', status="Profile Saved Successfully!")

@app.route('/detect', methods=['POST'])
def detect_growl():
    global growl_events, LAST_ORDER_TIME
    current_time = time.time()
    
    if current_time - LAST_ORDER_TIME < MUTE_DURATION:
        return jsonify({"status": "muted"}), 200

    data = request.json
    growl_events.append(current_time)
    growl_events = [t for t in growl_events if current_time - t < WINDOW_SIZE]
    
    count = len(growl_events)
    if count >= MIN_GROWLS_FOR_ORDER:
        is_big_meal = count >= 5
        recommendation_json = get_claude_recommendation(is_big_meal=is_big_meal)
        
        try:
            order_details = json.loads(recommendation_json)
        except:
            order_details = {"restaurant": "Machali", "dish": "Fish Thali", "rationale": "Fallback"}

        place_zomato_order(order_details)
        LAST_ORDER_TIME = current_time
        growl_events = []
        
        return jsonify({"status": "ordered", "order": order_details}), 200
    
    return jsonify({"status": "monitoring", "count": count}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
