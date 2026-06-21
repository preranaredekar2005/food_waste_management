# ============================================================
# LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
# Exploratory Data Analysis (EDA)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import psycopg2
import warnings
import os

warnings.filterwarnings("ignore")

# ── Output folder for plots ───────────────────────────────────
os.makedirs("eda_plots", exist_ok=True)

# ── DB Connection ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "database": "food_wastage",
    "user":     "postgres",
    "password": "prerana123",
    "port":     5432
}

def load(query):
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ── Style ─────────────────────────────────────────────────────
sns.set_theme(style="whitegrid")
COLORS = ["#2ecc71","#e74c3c","#f39c12","#3498db","#9b59b6","#1abc9c","#e67e22","#e91e63"]
plt.rcParams["figure.dpi"] = 120

print("=" * 60)
print("   LOCAL FOOD WASTAGE MANAGEMENT SYSTEM - EDA REPORT")
print("=" * 60)

# ── Load all tables ───────────────────────────────────────────
providers    = load("SELECT * FROM providers")
receivers    = load("SELECT * FROM receivers")
food         = load("SELECT * FROM food_listings")
claims       = load("SELECT * FROM claims")

food["expiry_date"] = pd.to_datetime(food["expiry_date"])
claims["timestamp"] = pd.to_datetime(claims["timestamp"])

# ============================================================
# SECTION 1: BASIC STATS
# ============================================================
print("\n📊 SECTION 1: DATASET OVERVIEW")
print("-" * 40)
print(f"Total Providers    : {len(providers)}")
print(f"Total Receivers    : {len(receivers)}")
print(f"Total Food Listings: {len(food)}")
print(f"Total Claims       : {len(claims)}")

print("\n── Providers Sample ──")
print(providers.head(3).to_string(index=False))

print("\n── Food Listings Sample ──")
print(food.head(3).to_string(index=False))

print("\n── Claims Sample ──")
print(claims.head(3).to_string(index=False))

print("\n── Missing Values ──")
for name, df in [("Providers", providers), ("Receivers", receivers),
                 ("Food Listings", food), ("Claims", claims)]:
    print(f"{name}: {df.isnull().sum().sum()} missing values")

# ============================================================
# SECTION 2: PROVIDER ANALYSIS
# ============================================================
print("\n📊 SECTION 2: PROVIDER ANALYSIS")
print("-" * 40)

provider_type_counts = providers["type"].value_counts()
print("\nProvider Type Distribution:")
print(provider_type_counts.to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Provider Analysis", fontsize=14, fontweight="bold")

axes[0].bar(provider_type_counts.index, provider_type_counts.values,
            color=COLORS[:len(provider_type_counts)])
axes[0].set_title("Providers by Type")
axes[0].set_xlabel("Provider Type")
axes[0].set_ylabel("Count")
axes[0].tick_params(axis="x", rotation=30)

city_providers = providers["city"].value_counts()
axes[1].barh(city_providers.index, city_providers.values, color=COLORS[:len(city_providers)])
axes[1].set_title("Providers by City")
axes[1].set_xlabel("Count")

plt.tight_layout()
plt.savefig("eda_plots/01_provider_analysis.png")
plt.show()
print("✅ Saved: eda_plots/01_provider_analysis.png")

# ============================================================
# SECTION 3: FOOD LISTINGS ANALYSIS
# ============================================================
print("\n📊 SECTION 3: FOOD LISTINGS ANALYSIS")
print("-" * 40)

print("\nFood Type Distribution:")
print(food["food_type"].value_counts().to_string())
print("\nMeal Type Distribution:")
print(food["meal_type"].value_counts().to_string())
print("\nQuantity Stats:")
print(food["quantity"].describe().to_string())

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Food Listings Analysis", fontsize=14, fontweight="bold")

# Food type pie
ft_counts = food["food_type"].value_counts()
axes[0,0].pie(ft_counts.values, labels=ft_counts.index,
              autopct="%1.1f%%", colors=COLORS[:len(ft_counts)], startangle=140)
axes[0,0].set_title("Food Type Distribution")

# Meal type bar
mt_counts = food["meal_type"].value_counts()
axes[0,1].bar(mt_counts.index, mt_counts.values, color=COLORS[:len(mt_counts)])
axes[0,1].set_title("Meal Type Distribution")
axes[0,1].set_ylabel("Count")

# Quantity distribution
axes[1,0].hist(food["quantity"], bins=20, color="#2ecc71", edgecolor="white")
axes[1,0].set_title("Quantity Distribution")
axes[1,0].set_xlabel("Quantity")
axes[1,0].set_ylabel("Frequency")

# Food listings by city
city_food = food["location"].value_counts()
axes[1,1].bar(city_food.index, city_food.values, color=COLORS[:len(city_food)])
axes[1,1].set_title("Food Listings by City")
axes[1,1].set_xlabel("City")
axes[1,1].set_ylabel("Count")
axes[1,1].tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.savefig("eda_plots/02_food_listings_analysis.png")
plt.show()
print("✅ Saved: eda_plots/02_food_listings_analysis.png")

# ============================================================
# SECTION 4: CLAIMS ANALYSIS
# ============================================================
print("\n📊 SECTION 4: CLAIMS ANALYSIS")
print("-" * 40)

print("\nClaim Status Distribution:")
print(claims["status"].value_counts().to_string())

claims["month"] = claims["timestamp"].dt.to_period("M").astype(str)
monthly = claims.groupby("month").size().reset_index(name="count")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Claims Analysis", fontsize=14, fontweight="bold")

# Status pie
st_counts = claims["status"].value_counts()
axes[0].pie(st_counts.values, labels=st_counts.index,
            autopct="%1.1f%%", colors=["#2ecc71","#e74c3c","#f39c12"], startangle=140)
axes[0].set_title("Claim Status Distribution")

# Monthly trend
axes[1].plot(monthly["month"], monthly["count"], marker="o", color="#3498db", linewidth=2)
axes[1].set_title("Monthly Claims Trend")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Number of Claims")
axes[1].tick_params(axis="x", rotation=45)
axes[1].fill_between(range(len(monthly)), monthly["count"], alpha=0.1, color="#3498db")

plt.tight_layout()
plt.savefig("eda_plots/03_claims_analysis.png")
plt.show()
print("✅ Saved: eda_plots/03_claims_analysis.png")

# ============================================================
# SECTION 5: COMBINED / JOINED ANALYSIS
# ============================================================
print("\n📊 SECTION 5: COMBINED ANALYSIS")
print("-" * 40)

# Total quantity donated per provider type
qty_by_type = load("""
    SELECT provider_type, SUM(quantity) AS total_quantity
    FROM food_listings GROUP BY provider_type ORDER BY total_quantity DESC
""")
print("\nTotal Quantity by Provider Type:")
print(qty_by_type.to_string(index=False))

# Top receivers
top_receivers = load("""
    SELECT r.name, COUNT(c.claim_id) AS total_claims
    FROM receivers r JOIN claims c ON r.receiver_id = c.receiver_id
    GROUP BY r.name ORDER BY total_claims DESC LIMIT 10
""")
print("\nTop 10 Receivers by Claims:")
print(top_receivers.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Combined Analysis", fontsize=14, fontweight="bold")

axes[0].barh(qty_by_type["provider_type"], qty_by_type["total_quantity"],
             color=COLORS[:len(qty_by_type)])
axes[0].set_title("Total Quantity Donated by Provider Type")
axes[0].set_xlabel("Total Quantity")

axes[1].barh(top_receivers["name"], top_receivers["total_claims"],
             color=COLORS[:len(top_receivers)])
axes[1].set_title("Top 10 Receivers by Claims")
axes[1].set_xlabel("Total Claims")

plt.tight_layout()
plt.savefig("eda_plots/04_combined_analysis.png")
plt.show()
print("✅ Saved: eda_plots/04_combined_analysis.png")

# ============================================================
# SECTION 6: EXPIRY ANALYSIS
# ============================================================
print("\n📊 SECTION 6: EXPIRY DATE ANALYSIS")
print("-" * 40)

food["expiry_month"] = food["expiry_date"].dt.month_name()
food["expiry_year"]  = food["expiry_date"].dt.year

expiry_month = food.groupby("expiry_month")["quantity"].sum().reset_index()
month_order  = ["January","February","March","April","May","June",
                "July","August","September","October","November","December"]
expiry_month["expiry_month"] = pd.Categorical(expiry_month["expiry_month"],
                                               categories=month_order, ordered=True)
expiry_month = expiry_month.sort_values("expiry_month")

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(expiry_month["expiry_month"], expiry_month["quantity"],
       color="#e74c3c", edgecolor="white")
ax.set_title("Total Food Quantity by Expiry Month", fontsize=13, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Total Quantity")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig("eda_plots/05_expiry_analysis.png")
plt.show()
print("✅ Saved: eda_plots/05_expiry_analysis.png")

# ============================================================
# SECTION 7: KEY INSIGHTS
# ============================================================
print("\n" + "=" * 60)
print("   KEY INSIGHTS & RECOMMENDATIONS")
print("=" * 60)

top_city  = food["location"].value_counts().idxmax()
top_ftype = food["food_type"].value_counts().idxmax()
top_mtype = food["meal_type"].value_counts().idxmax()
comp_pct  = round(claims[claims["status"]=="Completed"].shape[0] / len(claims) * 100, 1)
top_ptype = qty_by_type.iloc[0]["provider_type"]

print(f"""
1. 📍 City with most food listings  : {top_city}
2. 🥗 Most common food type         : {top_ftype}
3. 🍽️  Most common meal type         : {top_mtype}
4. ✅ Claim completion rate          : {comp_pct}%
5. 🏪 Top contributing provider type: {top_ptype}
6. 📦 Total food listings           : {len(food)}
7. 📋 Total claims made             : {len(claims)}
8. 🤝 Total receivers registered    : {len(receivers)}

RECOMMENDATIONS:
- Focus food distribution efforts in {top_city} where listings are highest
- {top_ftype} food dominates — ensure receivers with dietary needs are covered
- Claim completion rate of {comp_pct}% — improve follow-up for Pending claims
- Expand {top_ptype} partnerships as they contribute the most food
- Monitor expiry dates closely to reduce wastage
""")

print("=" * 60)
print("✅ EDA Complete! All plots saved in 'eda_plots/' folder.")
print("=" * 60)
