-- ============================================================
-- LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
-- SQL Script - All 15 Queries
-- Database: food_wastage
-- ============================================================

-- ============================================================
-- TABLE CREATION
-- ============================================================

DROP TABLE IF EXISTS claims CASCADE;
DROP TABLE IF EXISTS food_listings CASCADE;
DROP TABLE IF EXISTS receivers CASCADE;
DROP TABLE IF EXISTS providers CASCADE;

CREATE TABLE providers (
    Provider_ID   SERIAL PRIMARY KEY,
    Name          VARCHAR(100),
    Type          VARCHAR(50),
    Address       VARCHAR(200),
    City          VARCHAR(50),
    Contact       VARCHAR(20)
);

CREATE TABLE receivers (
    Receiver_ID   SERIAL PRIMARY KEY,
    Name          VARCHAR(100),
    Type          VARCHAR(50),
    City          VARCHAR(50),
    Contact       VARCHAR(20)
);

CREATE TABLE food_listings (
    Food_ID       SERIAL PRIMARY KEY,
    Food_Name     VARCHAR(100),
    Quantity      INTEGER,
    Expiry_Date   DATE,
    Provider_ID   INTEGER REFERENCES providers(Provider_ID),
    Provider_Type VARCHAR(50),
    Location      VARCHAR(50),
    Food_Type     VARCHAR(30),
    Meal_Type     VARCHAR(30)
);

CREATE TABLE claims (
    Claim_ID      SERIAL PRIMARY KEY,
    Food_ID       INTEGER REFERENCES food_listings(Food_ID),
    Receiver_ID   INTEGER REFERENCES receivers(Receiver_ID),
    Status        VARCHAR(20),
    Timestamp     TIMESTAMP
);

-- ============================================================
-- QUERY 1: How many food providers and receivers are there in each city?
-- ============================================================
SELECT 
    p.city,
    COUNT(DISTINCT p.provider_id) AS total_providers,
    COUNT(DISTINCT r.receiver_id) AS total_receivers
FROM providers p
LEFT JOIN receivers r ON p.city = r.city
GROUP BY p.city
ORDER BY total_providers DESC;

-- ============================================================
-- QUERY 2: Which type of food provider contributes the most food?
-- ============================================================
SELECT 
    provider_type,
    COUNT(*) AS total_listings,
    SUM(quantity) AS total_quantity
FROM food_listings
GROUP BY provider_type
ORDER BY total_quantity DESC;

-- ============================================================
-- QUERY 3: What is the contact information of food providers in each city?
-- ============================================================
SELECT 
    name,
    type,
    city,
    contact,
    address
FROM providers
ORDER BY city, name;

-- ============================================================
-- QUERY 4: Which receivers have claimed the most food?
-- ============================================================
SELECT 
    r.name,
    r.type,
    r.city,
    COUNT(c.claim_id) AS total_claims
FROM receivers r
JOIN claims c ON r.receiver_id = c.receiver_id
GROUP BY r.name, r.type, r.city
ORDER BY total_claims DESC
LIMIT 10;

-- ============================================================
-- QUERY 5: What is the total quantity of food available from all providers?
-- ============================================================
SELECT 
    SUM(quantity)  AS total_quantity,
    ROUND(AVG(quantity), 2) AS avg_quantity,
    MAX(quantity)  AS max_quantity,
    MIN(quantity)  AS min_quantity
FROM food_listings;

-- ============================================================
-- QUERY 6: Which city has the highest number of food listings?
-- ============================================================
SELECT 
    location AS city,
    COUNT(*) AS total_listings,
    SUM(quantity) AS total_quantity
FROM food_listings
GROUP BY location
ORDER BY total_listings DESC;

-- ============================================================
-- QUERY 7: What are the most commonly available food types?
-- ============================================================
SELECT 
    food_type,
    COUNT(*) AS count,
    SUM(quantity) AS total_quantity
FROM food_listings
GROUP BY food_type
ORDER BY count DESC;

-- ============================================================
-- QUERY 8: How many food claims have been made for each food item?
-- ============================================================
SELECT 
    fl.food_name,
    COUNT(c.claim_id) AS total_claims
FROM food_listings fl
LEFT JOIN claims c ON fl.food_id = c.food_id
GROUP BY fl.food_name
ORDER BY total_claims DESC
LIMIT 15;

-- ============================================================
-- QUERY 9: Which provider has had the highest number of successful food claims?
-- ============================================================
SELECT 
    p.name AS provider,
    p.type,
    p.city,
    COUNT(c.claim_id) AS completed_claims
FROM providers p
JOIN food_listings fl ON p.provider_id = fl.provider_id
JOIN claims c ON fl.food_id = c.food_id
WHERE c.status = 'Completed'
GROUP BY p.name, p.type, p.city
ORDER BY completed_claims DESC
LIMIT 10;

-- ============================================================
-- QUERY 10: What percentage of food claims are Completed vs Pending vs Cancelled?
-- ============================================================
SELECT 
    status,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM claims
GROUP BY status
ORDER BY count DESC;

-- ============================================================
-- QUERY 11: What is the average quantity of food claimed per receiver?
-- ============================================================
SELECT 
    r.name,
    r.type,
    COUNT(c.claim_id) AS total_claims,
    ROUND(AVG(fl.quantity), 2) AS avg_quantity_per_claim
FROM receivers r
JOIN claims c ON r.receiver_id = c.receiver_id
JOIN food_listings fl ON c.food_id = fl.food_id
GROUP BY r.name, r.type
ORDER BY avg_quantity_per_claim DESC
LIMIT 10;

-- ============================================================
-- QUERY 12: Which meal type is claimed the most?
-- ============================================================
SELECT 
    fl.meal_type,
    COUNT(c.claim_id) AS total_claims
FROM food_listings fl
JOIN claims c ON fl.food_id = c.food_id
GROUP BY fl.meal_type
ORDER BY total_claims DESC;

-- ============================================================
-- QUERY 13: What is the total quantity of food donated by each provider?
-- ============================================================
SELECT 
    p.name AS provider,
    p.city,
    SUM(fl.quantity) AS total_donated
FROM providers p
JOIN food_listings fl ON p.provider_id = fl.provider_id
GROUP BY p.name, p.city
ORDER BY total_donated DESC
LIMIT 10;

-- ============================================================
-- QUERY 14: Which food items are expiring soon (next 60 days)?
-- ============================================================
SELECT 
    fl.food_name,
    fl.quantity,
    fl.expiry_date,
    fl.location,
    p.name AS provider,
    p.contact
FROM food_listings fl
JOIN providers p ON fl.provider_id = p.provider_id
WHERE fl.expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '60 days'
ORDER BY fl.expiry_date ASC
LIMIT 20;

-- ============================================================
-- QUERY 15: What is the monthly trend of food claims?
-- ============================================================
SELECT 
    TO_CHAR(timestamp, 'YYYY-MM') AS month,
    COUNT(*) AS total_claims,
    COUNT(CASE WHEN status = 'Completed' THEN 1 END) AS completed_claims,
    COUNT(CASE WHEN status = 'Pending'   THEN 1 END) AS pending_claims,
    COUNT(CASE WHEN status = 'Cancelled' THEN 1 END) AS cancelled_claims
FROM claims
GROUP BY month
ORDER BY month;
