"""
Test script to simulate stomach growl detection and trigger ordering
Run this to test your MOM device without the ESP32 hardware
"""

import requests
import time
import json

# Configuration
SERVER_URL = "http://localhost:5000"

def test_single_growl():
    """Test a single growl detection (should not trigger order)"""
    print("\n🔊 Simulating SINGLE stomach growl...")
    response = requests.post(f"{SERVER_URL}/detect", json={})
    result = response.json()
    print(f"Response: {result}")
    return result

def test_multiple_growls(count=5, delay=2):
    """Test multiple growls (should trigger order)"""
    print(f"\n🔊 Simulating {count} stomach growls (hungry!)...")
    
    for i in range(count):
        print(f"Growl {i+1}/{count}...")
        response = requests.post(f"{SERVER_URL}/detect", json={})
        result = response.json()
        print(f"Response: {result}")
        
        if result.get('status') == 'ordered':
            print("\n✅ ORDER TRIGGERED!")
            print(f"Order Details: {json.dumps(result.get('order'), indent=2)}")
            return result
        
        if i < count - 1:
            time.sleep(delay)
    
    return None

def test_mute_period():
    """Test that orders are muted after recent order"""
    print("\n🔇 Testing mute period (should be blocked)...")
    response = requests.post(f"{SERVER_URL}/detect", json={})
    result = response.json()
    print(f"Response: {result}")
    return result

def check_server():
    """Check if server is running"""
    try:
        response = requests.get(SERVER_URL)
        print("✅ Server is running!")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("Please start the server first: python app.py")
        return False

def main():
    print("=" * 60)
    print("🍕 MOM Device Testing Suite")
    print("=" * 60)
    
    # Check server
    if not check_server():
        return
    
    print("\nChoose a test:")
    print("1. Single growl (no order)")
    print("2. Multiple growls (trigger order)")
    print("3. Test mute period")
    print("4. Full simulation (single → multiple → mute)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        test_single_growl()
    
    elif choice == "2":
        test_multiple_growls(count=5, delay=2)
    
    elif choice == "3":
        test_mute_period()
    
    elif choice == "4":
        print("\n📋 Running full simulation...\n")
        
        # Test 1: Single growl
        print("TEST 1: Single growl")
        test_single_growl()
        time.sleep(3)
        
        # Test 2: Multiple growls to trigger order
        print("\nTEST 2: Multiple growls")
        test_multiple_growls(count=5, delay=2)
        time.sleep(3)
        
        # Test 3: Try ordering again (should be muted)
        print("\nTEST 3: Immediate retry (should be muted)")
        test_mute_period()
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
