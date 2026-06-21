# 📊 Local Food Wastage Management System
## Recommendations & Insights Report

---

## 1. Project Overview

The Local Food Wastage Management System is a data-driven platform designed to connect surplus food providers — such as restaurants, hotels, grocery stores, and canteens — with receivers including NGOs, orphanages, community centres, and individuals in need. The system is built using Python, PostgreSQL, and Streamlit, and it manages four core datasets: Providers, Receivers, Food Listings, and Claims.

---

## 2. Key Findings from SQL Analysis

### 2.1 Provider Landscape
- The platform has **20 registered food providers** spread across 8 major Indian cities.
- **Restaurants and Hotels** are the most active provider types, contributing the highest total food quantity.
- **Mumbai, Delhi, and Bangalore** have the highest number of food listings, indicating strong urban participation.

### 2.2 Food Availability
- A total of **100 food listings** are active on the platform with a combined quantity exceeding **9,000 units**.
- **Vegetarian food** is the most commonly listed type, making up nearly 40% of all listings.
- **Lunch and Dinner** are the most frequently available meal types, while Breakfast listings are comparatively fewer.

### 2.3 Claims & Distribution
- **150 claims** have been made across the platform.
- Claim status breakdown:
  - ✅ Completed: ~35%
  - ⏳ Pending: ~33%
  - ❌ Cancelled: ~32%
- The high Pending and Cancelled rates indicate a gap in follow-through — a key area for improvement.
- Top receivers are NGOs and Community Centres, which collectively account for the majority of claims.

### 2.4 Wastage Risk
- Several food listings have expiry dates within the next 60 days and remain unclaimed — this represents a direct wastage risk.
- Expiry distribution shows a spike in listings expiring in mid-year months (May–August), suggesting seasonal surplus patterns.

---

## 3. Recommendations

### 🔴 Priority 1 — Improve Claim Completion Rate
The current completion rate is approximately 35%, which is low. Recommended actions:
- Send automated reminders to receivers for Pending claims.
- Add a deadline mechanism — if a claim is not confirmed within 24 hours, reassign it automatically.
- Allow providers to mark food as "Urgent" when expiry is near, triggering alerts to nearby receivers.

### 🟡 Priority 2 — Expand Breakfast & Vegan Listings
Lunch and Dinner dominate current listings, creating an imbalance. Recommended actions:
- Onboard bakeries, canteens, and school kitchens that typically produce morning surplus.
- Run targeted campaigns to encourage Vegan food providers to register on the platform.

### 🟢 Priority 3 — City-wise Expansion
Mumbai, Delhi, and Bangalore are well-represented, but cities like Kolkata, Ahmedabad, and Chennai have fewer listings. Recommended actions:
- Partner with local NGOs in underrepresented cities to onboard more providers.
- Offer simplified onboarding for small restaurants and home cooks in Tier-2 cities.

### 🔵 Priority 4 — Expiry Date Monitoring
A significant volume of food is at risk of expiring before being claimed. Recommended actions:
- Implement a daily expiry alert system.
- Prioritise listings with fewer than 7 days to expiry in the Streamlit filter dashboard.
- Generate weekly reports for providers showing unclaimed food items.

### 🟣 Priority 5 — Data Quality & Engagement
- Encourage providers to update quantities in real time after partial distributions.
- Add a rating or feedback system so receivers can rate the quality of food received.
- Track which receiver types (NGO vs Individual vs Community Centre) are most effective at completing claims.

---

## 4. EDA Summary

| Metric | Value |
|---|---|
| Total Providers | 20 |
| Total Receivers | 20 |
| Total Food Listings | 100 |
| Total Claims | 150 |
| Most Active City | Mumbai |
| Top Food Type | Vegetarian |
| Top Meal Type | Lunch |
| Claim Completion Rate | ~35% |
| Top Provider Type | Restaurant |

---

## 5. Streamlit Dashboard

The interactive Streamlit dashboard is deployed at:

🔗 **[Streamlit App Link — add after deployment]**

The dashboard provides:
- Live KPI metrics (total providers, receivers, listings, claims)
- 15 SQL query outputs with visualisations
- Filter panel by city, food type, meal type, and provider type
- Full CRUD operations (Add / Update / Delete food listings)
- Contact directory for providers and receivers
- Monthly trends and expiry analysis charts

---

## 6. Conclusion

The Local Food Wastage Management System demonstrates a practical, scalable approach to reducing urban food wastage through structured data management and real-time analytics. The SQL-backed Streamlit platform enables seamless interaction between food providers and receivers, while the EDA layer surfaces actionable insights to guide operational decisions. With targeted improvements in claim follow-through and city-wise expansion, the platform has strong potential for real-world social impact.

---

*Report prepared as part of LabMentix Data Science Project — Local Food Wastage Management System*
