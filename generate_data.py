import pandas as pd
import random
import os
from datetime import datetime, timedelta

random.seed(42)

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Pune", "Hyderabad", "Kolkata", "Ahmedabad"]
provider_types = ["Restaurant", "Grocery Store", "Supermarket", "Hotel", "Bakery", "Canteen"]
receiver_types = ["NGO", "Community Center", "Individual", "Orphanage", "Old Age Home"]
food_names = ["Rice", "Dal", "Bread", "Vegetables", "Fruits", "Biryani", "Chapati", "Sambar",
              "Idli", "Poha", "Upma", "Curd Rice", "Sandwich", "Salad", "Pasta", "Soup",
              "Khichdi", "Pulao", "Paneer Curry", "Mixed Snacks"]
food_types = ["Vegetarian", "Non-Vegetarian", "Vegan"]
meal_types = ["Breakfast", "Lunch", "Dinner", "Snacks"]
statuses = ["Pending", "Completed", "Cancelled"]

# --- 1. Providers ---
providers = []
provider_names = [
    "Green Leaf Restaurant", "City Bakery", "Fresh Mart", "Spice Garden", "Hotel Sunshine",
    "Daily Needs Store", "Royal Kitchen", "Big Basket Outlet", "Annapurna Canteen",
    "Metro Supermarket", "Taste of India", "Swad Restaurant", "Reliance Fresh",
    "Hotel Grand", "Udupi Bhavan", "Morning Glory Bakery", "Nature's Basket",
    "Food Court Central", "Raj Catering", "Surya Hotel"
]
for i in range(1, 21):
    providers.append({
        "Provider_ID": i,
        "Name": provider_names[i-1],
        "Type": random.choice(provider_types),
        "Address": f"{random.randint(1,200)}, {random.choice(['MG Road','Anna Salai','Park Street','FC Road','Linking Road'])}",
        "City": random.choice(cities),
        "Contact": f"9{random.randint(100000000, 999999999)}"
    })
df_providers = pd.DataFrame(providers)
df_providers.to_csv("data/providers_data.csv", index=False)

# --- 2. Receivers ---
receivers = []
receiver_names = [
    "Helping Hands NGO", "Care Foundation", "Roti Bank", "Anath Ashram", "Shanti Old Age Home",
    "City Relief Center", "Hope Community", "Seva Sadan", "Bal Bhavan Trust", "Green Earth NGO",
    "Asha Kiran", "Nav Jeevan Center", "Disha Foundation", "People's Kitchen", "Smile Foundation",
    "United Relief", "Sneh Sadan", "Jeevan Jyoti", "Mamta NGO", "Udaan Trust"
]
for i in range(1, 21):
    receivers.append({
        "Receiver_ID": i,
        "Name": receiver_names[i-1],
        "Type": random.choice(receiver_types),
        "City": random.choice(cities),
        "Contact": f"8{random.randint(100000000, 999999999)}"
    })
df_receivers = pd.DataFrame(receivers)
df_receivers.to_csv("data/receivers_data.csv", index=False)

# --- 3. Food Listings ---
food_listings = []
base_date = datetime(2025, 1, 1)
for i in range(1, 101):
    expiry = base_date + timedelta(days=random.randint(1, 365))
    provider = random.choice(providers)
    food_listings.append({
        "Food_ID": i,
        "Food_Name": random.choice(food_names),
        "Quantity": random.randint(5, 200),
        "Expiry_Date": expiry.strftime("%Y-%m-%d"),
        "Provider_ID": provider["Provider_ID"],
        "Provider_Type": provider["Type"],
        "Location": provider["City"],
        "Food_Type": random.choice(food_types),
        "Meal_Type": random.choice(meal_types)
    })
df_food = pd.DataFrame(food_listings)
df_food.to_csv("data/food_listings_data.csv", index=False)

# --- 4. Claims ---
claims = []
for i in range(1, 151):
    ts = base_date + timedelta(days=random.randint(0, 364), hours=random.randint(0, 23))
    claims.append({
        "Claim_ID": i,
        "Food_ID": random.randint(1, 100),
        "Receiver_ID": random.randint(1, 20),
        "Status": random.choice(statuses),
        "Timestamp": ts.strftime("%Y-%m-%d %H:%M:%S")
    })
df_claims = pd.DataFrame(claims)
df_claims.to_csv("data/claims_data.csv", index=False)

print("✅ All 4 CSV files generated successfully!")
print(f"Providers: {len(df_providers)} rows")
print(f"Receivers: {len(df_receivers)} rows")
print(f"Food Listings: {len(df_food)} rows")
print(f"Claims: {len(df_claims)} rows")
