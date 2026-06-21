import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
from datetime import date
import random
from datetime import datetime, timedelta

# ── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍛",
    layout="wide"
)

# ── DB PATH ────────────────────────────────────────────────────
DB_PATH = "food_wastage.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ── AUTO INIT DB ───────────────────────────────────────────────
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS providers (
            Provider_ID INTEGER PRIMARY KEY, Name TEXT, Type TEXT,
            Address TEXT, City TEXT, Contact TEXT);
        CREATE TABLE IF NOT EXISTS receivers (
            Receiver_ID INTEGER PRIMARY KEY, Name TEXT, Type TEXT,
            City TEXT, Contact TEXT);
        CREATE TABLE IF NOT EXISTS food_listings (
            Food_ID INTEGER PRIMARY KEY, Food_Name TEXT, Quantity INTEGER,
            Expiry_Date TEXT, Provider_ID INTEGER, Provider_Type TEXT,
            Location TEXT, Food_Type TEXT, Meal_Type TEXT);
        CREATE TABLE IF NOT EXISTS claims (
            Claim_ID INTEGER PRIMARY KEY, Food_ID INTEGER,
            Receiver_ID INTEGER, Status TEXT, Timestamp TEXT);
    """)

    # Only seed if empty
    if cur.execute("SELECT COUNT(*) FROM providers").fetchone()[0] == 0:
        random.seed(42)
        cities = ["Mumbai","Delhi","Bangalore","Chennai","Pune","Hyderabad","Kolkata","Ahmedabad"]
        provider_types = ["Restaurant","Grocery Store","Supermarket","Hotel","Bakery","Canteen"]
        receiver_types = ["NGO","Community Center","Individual","Orphanage","Old Age Home"]
        food_names = ["Rice","Dal","Bread","Vegetables","Fruits","Biryani","Chapati","Sambar",
                      "Idli","Poha","Upma","Curd Rice","Sandwich","Salad","Pasta","Soup",
                      "Khichdi","Pulao","Paneer Curry","Mixed Snacks"]
        food_types = ["Vegetarian","Non-Vegetarian","Vegan"]
        meal_types = ["Breakfast","Lunch","Dinner","Snacks"]
        statuses   = ["Pending","Completed","Cancelled"]

        provider_names = [
            "Green Leaf Restaurant","City Bakery","Fresh Mart","Spice Garden","Hotel Sunshine",
            "Daily Needs Store","Royal Kitchen","Big Basket Outlet","Annapurna Canteen",
            "Metro Supermarket","Taste of India","Swad Restaurant","Reliance Fresh",
            "Hotel Grand","Udupi Bhavan","Morning Glory Bakery","Nature's Basket",
            "Food Court Central","Raj Catering","Surya Hotel"
        ]
        receiver_names = [
            "Helping Hands NGO","Care Foundation","Roti Bank","Anath Ashram","Shanti Old Age Home",
            "City Relief Center","Hope Community","Seva Sadan","Bal Bhavan Trust","Green Earth NGO",
            "Asha Kiran","Nav Jeevan Center","Disha Foundation","People's Kitchen","Smile Foundation",
            "United Relief","Sneh Sadan","Jeevan Jyoti","Mamta NGO","Udaan Trust"
        ]
        roads = ["MG Road","Anna Salai","Park Street","FC Road","Linking Road"]

        providers = []
        for i in range(1, 21):
            city = random.choice(cities)
            providers.append((i, provider_names[i-1], random.choice(provider_types),
                              f"{random.randint(1,200)}, {random.choice(roads)}", city,
                              f"9{random.randint(100000000,999999999)}"))
        cur.executemany("INSERT INTO providers VALUES (?,?,?,?,?,?)", providers)

        receivers = []
        for i in range(1, 21):
            receivers.append((i, receiver_names[i-1], random.choice(receiver_types),
                              random.choice(cities), f"8{random.randint(100000000,999999999)}"))
        cur.executemany("INSERT INTO receivers VALUES (?,?,?,?,?)", receivers)

        base_date = datetime(2025, 1, 1)
        food_listings = []
        for i in range(1, 101):
            expiry = base_date + timedelta(days=random.randint(1, 365))
            p = random.choice(providers)
            food_listings.append((i, random.choice(food_names), random.randint(5,200),
                                  expiry.strftime("%Y-%m-%d"), p[0], p[2], p[4],
                                  random.choice(food_types), random.choice(meal_types)))
        cur.executemany("INSERT INTO food_listings VALUES (?,?,?,?,?,?,?,?,?)", food_listings)

        claims = []
        for i in range(1, 151):
            ts = base_date + timedelta(days=random.randint(0,364), hours=random.randint(0,23))
            claims.append((i, random.randint(1,100), random.randint(1,20),
                           random.choice(statuses), ts.strftime("%Y-%m-%d %H:%M:%S")))
        cur.executemany("INSERT INTO claims VALUES (?,?,?,?,?)", claims)

        conn.commit()
    conn.close()

init_db()

def run_query(query):
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        st.error(f"Query error: {e}")
        return pd.DataFrame()

def execute_dml(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or [])
    conn.commit()
    conn.close()

# ── SIDEBAR ────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/emoji/96/green-salad.png", width=80)
st.sidebar.title("🍛 Food Wastage MS")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", [
    "🏠 Dashboard","📊 SQL Analysis (15 Queries)","🔍 Filter & Search",
    "➕ Add Food Listing","✏️ Update Listing","🗑️ Delete Listing",
    "📋 View All Tables","📞 Contact Directory"
])

# ══════════════════════════════════════════════════════════════
# 1. DASHBOARD
# ══════════════════════════════════════════════════════════════
if menu == "🏠 Dashboard":
    st.title("🍛 Local Food Wastage Management System")
    st.markdown("#### Connecting surplus food providers with those in need")
    st.markdown("---")

    col1,col2,col3,col4 = st.columns(4)
    col1.metric("🏪 Total Providers", run_query("SELECT COUNT(*) as c FROM providers")["c"][0])
    col2.metric("🤝 Total Receivers", run_query("SELECT COUNT(*) as c FROM receivers")["c"][0])
    col3.metric("🍱 Food Listings",   run_query("SELECT COUNT(*) as c FROM food_listings")["c"][0])
    col4.metric("📦 Total Claims",    run_query("SELECT COUNT(*) as c FROM claims")["c"][0])

    st.markdown("---")
    col5,col6 = st.columns(2)
    with col5:
    df = run_query("""
        SELECT location, COUNT(*) AS count
        FROM food_listings
        GROUP BY location
        ORDER BY count DESC
    """)

    st.write("Columns:", df.columns.tolist())

    if not df.empty and "location" in df.columns and "count" in df.columns:
        fig = px.bar(
            df,
            x="location",
            y="count",
            title="📍 Food Listings by City",
            color_discrete_sequence=["#2ecc71"]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"Columns found: {df.columns.tolist()}")

    with col6:
        df2 = run_query("SELECT status, COUNT(*) as count FROM claims GROUP BY status")
        st.plotly_chart(px.pie(df2, names="status", values="count",
                               color_discrete_sequence=["#2ecc71","#e74c3c","#f39c12"],
                               title="📊 Claim Status Distribution"),
                        use_container_width=True)

    col7,col8 = st.columns(2)
    with col7:
        df3 = run_query("SELECT food_type, COUNT(*) as count FROM food_listings GROUP BY food_type")
        st.plotly_chart(px.pie(df3, names="food_type", values="count", title="🍽️ Food Type Distribution"),
                        use_container_width=True)
    with col8:
        df4 = run_query("SELECT meal_type, COUNT(*) as count FROM food_listings GROUP BY meal_type ORDER BY count DESC")
        st.plotly_chart(px.bar(df4, x="meal_type", y="count", title="🥗 Meal Type Distribution", color_discrete_sequence=px.colors.qualitative.Set2),
                        use_container_width=True)

# ══════════════════════════════════════════════════════════════
# 2. SQL ANALYSIS
# ══════════════════════════════════════════════════════════════
elif menu == "📊 SQL Analysis (15 Queries)":
    st.title("📊 SQL Analysis — 15 Key Queries")
    st.markdown("---")

    queries = {
        "Q1: Providers & Receivers per City": {
            "desc": "How many food providers and receivers are there in each city?",
            "sql": """SELECT p.city, COUNT(DISTINCT p.provider_id) AS providers,
                       COUNT(DISTINCT r.receiver_id) AS receivers
                FROM providers p LEFT JOIN receivers r ON p.city=r.city
                GROUP BY p.city ORDER BY providers DESC""",
            "chart":"bar","x":"city","y":["providers","receivers"]},
        "Q2: Provider Type Contributions": {
            "desc": "Which type of food provider contributes the most food?",
            "sql": """SELECT provider_type, COUNT(*) AS total_listings, SUM(quantity) AS total_quantity
                FROM food_listings GROUP BY provider_type ORDER BY total_quantity DESC""",
            "chart":"bar","x":"provider_type","y":"total_quantity"},
        "Q3: Contact Info by City": {
            "desc": "Contact information of food providers in each city.",
            "sql": "SELECT name, type, city, contact, address FROM providers ORDER BY city",
            "chart":None},
        "Q4: Top Receivers by Claims": {
            "desc": "Which receivers have claimed the most food?",
            "sql": """SELECT r.name, r.type, r.city, COUNT(c.claim_id) AS total_claims
                FROM receivers r JOIN claims c ON r.receiver_id=c.receiver_id
                GROUP BY r.name,r.type,r.city ORDER BY total_claims DESC LIMIT 10""",
            "chart":"bar","x":"name","y":"total_claims"},
        "Q5: Total Food Quantity Available": {
            "desc": "What is the total quantity of food available from all providers?",
            "sql": """SELECT SUM(quantity) AS total_quantity, ROUND(AVG(quantity),2) AS avg_quantity,
                       MAX(quantity) AS max_quantity, MIN(quantity) AS min_quantity FROM food_listings""",
            "chart":None},
        "Q6: City with Highest Food Listings": {
            "desc": "Which city has the highest number of food listings?",
            "sql": """SELECT location AS city, COUNT(*) AS listings, SUM(quantity) AS total_quantity
                FROM food_listings GROUP BY location ORDER BY listings DESC""",
            "chart":"bar","x":"city","y":"listings"},
        "Q7: Most Common Food Types": {
            "desc": "What are the most commonly available food types?",
            "sql": """SELECT food_type, COUNT(*) AS count, SUM(quantity) AS total_quantity
                FROM food_listings GROUP BY food_type ORDER BY count DESC""",
            "chart":"pie","names":"food_type","values":"count"},
        "Q8: Claims per Food Item": {
            "desc": "How many food claims have been made for each food item?",
            "sql": """SELECT fl.food_name, COUNT(c.claim_id) AS total_claims
                FROM food_listings fl LEFT JOIN claims c ON fl.food_id=c.food_id
                GROUP BY fl.food_name ORDER BY total_claims DESC LIMIT 15""",
            "chart":"bar","x":"food_name","y":"total_claims"},
        "Q9: Provider with Most Successful Claims": {
            "desc": "Which provider has had the highest number of successful food claims?",
            "sql": """SELECT p.name AS provider, p.type, p.city, COUNT(c.claim_id) AS completed_claims
                FROM providers p JOIN food_listings fl ON p.provider_id=fl.provider_id
                JOIN claims c ON fl.food_id=c.food_id WHERE c.status='Completed'
                GROUP BY p.name,p.type,p.city ORDER BY completed_claims DESC LIMIT 10""",
            "chart":"bar","x":"provider","y":"completed_claims"},
        "Q10: Claim Status Percentage": {
            "desc": "What percentage of food claims are Completed vs Pending vs Cancelled?",
            "sql": """SELECT status, COUNT(*) AS count,
                       ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM claims),2) AS percentage
                FROM claims GROUP BY status ORDER BY count DESC""",
            "chart":"pie","names":"status","values":"count"},
        "Q11: Avg Quantity Claimed per Receiver": {
            "desc": "What is the average quantity of food claimed per receiver?",
            "sql": """SELECT r.name, r.type, COUNT(c.claim_id) AS claims,
                       ROUND(AVG(fl.quantity),2) AS avg_quantity
                FROM receivers r JOIN claims c ON r.receiver_id=c.receiver_id
                JOIN food_listings fl ON c.food_id=fl.food_id
                GROUP BY r.name,r.type ORDER BY avg_quantity DESC LIMIT 10""",
            "chart":"bar","x":"name","y":"avg_quantity"},
        "Q12: Most Claimed Meal Type": {
            "desc": "Which meal type is claimed the most?",
            "sql": """SELECT fl.meal_type, COUNT(c.claim_id) AS total_claims
                FROM food_listings fl JOIN claims c ON fl.food_id=c.food_id
                GROUP BY fl.meal_type ORDER BY total_claims DESC""",
            "chart":"pie","names":"meal_type","values":"total_claims"},
        "Q13: Total Quantity Donated per Provider": {
            "desc": "What is the total quantity of food donated by each provider?",
            "sql": """SELECT p.name AS provider, p.city, SUM(fl.quantity) AS total_donated
                FROM providers p JOIN food_listings fl ON p.provider_id=fl.provider_id
                GROUP BY p.name,p.city ORDER BY total_donated DESC LIMIT 10""",
            "chart":"bar","x":"provider","y":"total_donated"},
        "Q14: Food Expiring Soon": {
            "desc": "Which food items are expiring soon and need urgent distribution?",
            "sql": """SELECT fl.food_name, fl.quantity, fl.expiry_date, fl.location,
                       p.name AS provider, p.contact
                FROM food_listings fl JOIN providers p ON fl.provider_id=p.provider_id
                ORDER BY fl.expiry_date ASC LIMIT 20""",
            "chart":None},
        "Q15: Monthly Claims Trend": {
            "desc": "What is the monthly trend of food claims throughout the year?",
            "sql": """SELECT SUBSTR(timestamp,1,7) AS month, COUNT(*) AS total_claims,
                       SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) AS completed
                FROM claims GROUP BY month ORDER BY month""",
            "chart":"line","x":"month","y":"total_claims"},
    }

    for i,(title,q) in enumerate(queries.items(),1):
        with st.expander(f"**{title}**", expanded=(i==1)):
            st.markdown(f"*{q['desc']}*")
            st.code(q["sql"].strip(), language="sql")
            df = run_query(q["sql"])
            st.dataframe(df, use_container_width=True)
            if q.get("chart")=="bar":
                y_col=q["y"]
                if isinstance(y_col,list):
                    fig=px.bar(df,x=q["x"],y=y_col,barmode="group",color_discrete_sequence=px.colors.qualitative.Set2)
                else:
                    fig=px.bar(df,x=q["x"],y=y_col,color_discrete_sequence=["#2ecc71"])
                st.plotly_chart(fig,use_container_width=True)
            elif q.get("chart")=="pie":
                fig=px.pie(df,names=q["names"],values=q["values"],color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(fig,use_container_width=True)
            elif q.get("chart")=="line":
                fig=px.line(df,x=q["x"],y=q["y"],markers=True,color_discrete_sequence=["#2ecc71"])
                st.plotly_chart(fig,use_container_width=True)

# ══════════════════════════════════════════════════════════════
# 3. FILTER & SEARCH
# ══════════════════════════════════════════════════════════════
elif menu == "🔍 Filter & Search":
    st.title("🔍 Filter Food Listings")
    st.markdown("---")
    cities=["All"]+run_query("SELECT DISTINCT location FROM food_listings ORDER BY location")["location"].tolist()
    ftypes=["All"]+run_query("SELECT DISTINCT food_type FROM food_listings ORDER BY food_type")["food_type"].tolist()
    mtypes=["All"]+run_query("SELECT DISTINCT meal_type FROM food_listings ORDER BY meal_type")["meal_type"].tolist()
    ptypes=["All"]+run_query("SELECT DISTINCT type FROM providers ORDER BY type")["type"].tolist()
    col1,col2,col3,col4=st.columns(4)
    city=col1.selectbox("📍 City",cities); ftype=col2.selectbox("🥗 Food Type",ftypes)
    mtype=col3.selectbox("🍽️ Meal Type",mtypes); ptype=col4.selectbox("🏪 Provider Type",ptypes)
    q="""SELECT fl.food_id,fl.food_name,fl.quantity,fl.expiry_date,fl.food_type,fl.meal_type,
                fl.location,p.name AS provider,p.type AS provider_type,p.contact
         FROM food_listings fl JOIN providers p ON fl.provider_id=p.provider_id WHERE 1=1"""
    if city!="All": q+=f" AND fl.location='{city}'"
    if ftype!="All": q+=f" AND fl.food_type='{ftype}'"
    if mtype!="All": q+=f" AND fl.meal_type='{mtype}'"
    if ptype!="All": q+=f" AND p.type='{ptype}'"
    df=run_query(q+" ORDER BY fl.expiry_date ASC")
    st.markdown(f"**{len(df)} listings found**")
    st.dataframe(df,use_container_width=True)
    if not df.empty:
        c5,c6=st.columns(2)
        with c5: st.plotly_chart(px.bar(df.groupby("location")["quantity"].sum().reset_index(),x="location",y="quantity",title="Quantity by City"),use_container_width=True)
        with c6: st.plotly_chart(px.pie(df,names="food_type",title="Food Type Split"),use_container_width=True)

# ══════════════════════════════════════════════════════════════
# 4. ADD
# ══════════════════════════════════════════════════════════════
elif menu == "➕ Add Food Listing":
    st.title("➕ Add New Food Listing"); st.markdown("---")
    providers_df=run_query("SELECT provider_id,name,city FROM providers ORDER BY name")
    provider_options={f"{row['name']} ({row['city']})":row["provider_id"] for _,row in providers_df.iterrows()}
    with st.form("add_form"):
        c1,c2=st.columns(2)
        food_name=c1.text_input("Food Name"); quantity=c2.number_input("Quantity",min_value=1,value=10)
        expiry_date=c1.date_input("Expiry Date",min_value=date.today())
        food_type=c2.selectbox("Food Type",["Vegetarian","Non-Vegetarian","Vegan"])
        meal_type=c1.selectbox("Meal Type",["Breakfast","Lunch","Dinner","Snacks"])
        provider_sel=c2.selectbox("Provider",list(provider_options.keys()))
        location=c1.text_input("Location / City")
        provider_type=c2.selectbox("Provider Type",["Restaurant","Grocery Store","Supermarket","Hotel","Bakery","Canteen"])
        if st.form_submit_button("✅ Add Listing"):
            if food_name and location:
                pid=provider_options[provider_sel]
                execute_dml("INSERT INTO food_listings (food_name,quantity,expiry_date,provider_id,provider_type,location,food_type,meal_type) VALUES (?,?,?,?,?,?,?,?)",
                            (food_name,quantity,str(expiry_date),pid,provider_type,location,food_type,meal_type))
                st.success(f"✅ '{food_name}' added!")
            else: st.error("Fill all fields.")

# ══════════════════════════════════════════════════════════════
# 5. UPDATE
# ══════════════════════════════════════════════════════════════
elif menu == "✏️ Update Listing":
    st.title("✏️ Update Food Listing"); st.markdown("---")
    df=run_query("SELECT food_id,food_name,quantity,food_type,meal_type FROM food_listings ORDER BY food_id")
    food_options={f"[ID:{row['food_id']}] {row['food_name']}":row["food_id"] for _,row in df.iterrows()}
    selected=st.selectbox("Select Listing",list(food_options.keys()))
    fid=food_options[selected]; row=df[df["food_id"]==fid].iloc[0]
    with st.form("update_form"):
        c1,c2=st.columns(2)
        new_qty=c1.number_input("Quantity",min_value=1,value=int(row["quantity"]))
        new_ftype=c2.selectbox("Food Type",["Vegetarian","Non-Vegetarian","Vegan"],index=["Vegetarian","Non-Vegetarian","Vegan"].index(row["food_type"]))
        new_mtype=c1.selectbox("Meal Type",["Breakfast","Lunch","Dinner","Snacks"],index=["Breakfast","Lunch","Dinner","Snacks"].index(row["meal_type"]))
        if st.form_submit_button("✅ Update"):
            execute_dml("UPDATE food_listings SET quantity=?,food_type=?,meal_type=? WHERE food_id=?",(new_qty,new_ftype,new_mtype,fid))
            st.success("✅ Updated!")

# ══════════════════════════════════════════════════════════════
# 6. DELETE
# ══════════════════════════════════════════════════════════════
elif menu == "🗑️ Delete Listing":
    st.title("🗑️ Delete Food Listing"); st.markdown("---")
    st.warning("⚠️ This will permanently delete the listing.")
    df=run_query("SELECT food_id,food_name,location FROM food_listings ORDER BY food_id")
    food_options={f"[ID:{row['food_id']}] {row['food_name']} — {row['location']}":row["food_id"] for _,row in df.iterrows()}
    selected=st.selectbox("Select Listing",list(food_options.keys()))
    fid=food_options[selected]
    if st.button("🗑️ Delete",type="primary"):
        execute_dml("DELETE FROM claims WHERE food_id=?",(fid,))
        execute_dml("DELETE FROM food_listings WHERE food_id=?",(fid,))
        st.success(f"✅ Deleted ID {fid}.")

# ══════════════════════════════════════════════════════════════
# 7. VIEW ALL TABLES
# ══════════════════════════════════════════════════════════════
elif menu == "📋 View All Tables":
    st.title("📋 All Database Tables"); st.markdown("---")
    tab1,tab2,tab3,tab4=st.tabs(["🏪 Providers","🤝 Receivers","🍱 Food Listings","📦 Claims"])
    with tab1: st.dataframe(run_query("SELECT * FROM providers"),use_container_width=True)
    with tab2: st.dataframe(run_query("SELECT * FROM receivers"),use_container_width=True)
    with tab3: st.dataframe(run_query("SELECT * FROM food_listings"),use_container_width=True)
    with tab4: st.dataframe(run_query("SELECT * FROM claims"),use_container_width=True)

# ══════════════════════════════════════════════════════════════
# 8. CONTACT DIRECTORY
# ══════════════════════════════════════════════════════════════
elif menu == "📞 Contact Directory":
    st.title("📞 Contact Directory"); st.markdown("---")
    tab1,tab2=st.tabs(["🏪 Food Providers","🤝 Receivers / NGOs"])
    with tab1:
        cf=st.selectbox("Filter by City",["All"]+run_query("SELECT DISTINCT city FROM providers ORDER BY city")["city"].tolist())
        q="SELECT name,type,city,contact,address FROM providers"
        if cf!="All": q+=f" WHERE city='{cf}'"
        st.dataframe(run_query(q+" ORDER BY city,name"),use_container_width=True)
    with tab2:
        cf2=st.selectbox("Filter by City ",["All"]+run_query("SELECT DISTINCT city FROM receivers ORDER BY city")["city"].tolist())
        q2="SELECT name,type,city,contact FROM receivers"
        if cf2!="All": q2+=f" WHERE city='{cf2}'"
        st.dataframe(run_query(q2+" ORDER BY city,name"),use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**Local Food Wastage MS**")
st.sidebar.markdown("Built with Python · SQLite · Streamlit")
