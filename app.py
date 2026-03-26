import streamlit as st
import numpy as np
import pandas as pd
import pickle

# ================= LOAD MODEL =================
with open('model.pkl', 'rb') as f:
    model, feature_columns = pickle.load(f)

st.set_page_config(page_title="Gaming House Dashboard", layout="wide")

# ================= UI STYLE =================
st.markdown("""
<style>
body {
    background: #000000;
    color: white;
}
.title {
    font-size: 42px;
    text-align: center;
    font-weight: bold;
    color: #00f2fe;
    text-shadow: 0 0 20px #00f2fe;
}
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    text-align: center;
}
.stButton > button {
    background-color: black;
    color: white;
    border: 1px solid #00f2fe;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown('<div class="title">🏡 House Price Prediction</div>', unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.header("📥 Property Details")

# 🌍 City Selection (Improved)
cities = ["Mumbai", "Pune", "Nashik", "Other"]
location = st.sidebar.selectbox("📍 Select City", cities)

if location == "Other":
    custom_city = st.sidebar.text_input("Enter Your City")

# 🔢 Manual Input with +/- buttons
area = st.sidebar.number_input("📐 Area (sq.ft)", min_value=100, max_value=20000, value=2000, step=100)
bedrooms = st.sidebar.number_input("🛏 Bedrooms", min_value=1, max_value=10, value=3, step=1)
bathrooms = st.sidebar.number_input("🛁 Bathrooms", min_value=1, max_value=10, value=2, step=1)
stories = st.sidebar.number_input("🏢 Stories", min_value=1, max_value=10, value=2, step=1)
parking = st.sidebar.number_input("🚗 Parking", min_value=0, max_value=10, value=1, step=1)

mainroad = st.sidebar.selectbox("Main Road", ['yes', 'no'])
guestroom = st.sidebar.selectbox("Guest Room", ['yes', 'no'])
basement = st.sidebar.selectbox("Basement", ['yes', 'no'])
airconditioning = st.sidebar.selectbox("AC", ['yes', 'no'])
prefarea = st.sidebar.selectbox("Preferred Area", ['yes', 'no'])
furnishingstatus = st.sidebar.selectbox("Furnishing", ['furnished', 'semi-furnished', 'unfurnished'])

# ================= INPUT DATA =================
input_data = {
    'area': area,
    'bedrooms': bedrooms,
    'bathrooms': bathrooms,
    'stories': stories,
    'parking': parking,
    'mainroad_yes': int(mainroad == 'yes'),
    'guestroom_yes': int(guestroom == 'yes'),
    'basement_yes': int(basement == 'yes'),
    'airconditioning_yes': int(airconditioning == 'yes'),
    'prefarea_yes': int(prefarea == 'yes'),
    'furnishingstatus_semi-furnished': int(furnishingstatus == 'semi-furnished'),
    'furnishingstatus_unfurnished': int(furnishingstatus == 'unfurnished'),

    # Default encoding
    'location_Mumbai': int(location == "Mumbai"),
    'location_Pune': int(location == "Pune"),
    'location_Nashik': int(location == "Nashik")
}

input_df = pd.DataFrame([input_data])
input_df = input_df.reindex(columns=feature_columns, fill_value=0)

# ================= PREDICT =================
if st.sidebar.button("🔍 Predict Price"):

    prediction = model.predict(input_df)[0]

    st.balloons()

    # ================= KPI =================
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f'<div class="card"><h3>💰 Price</h3><h2>₹ {round(prediction):,}</h2></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card"><h3>📐 Area</h3><h2>{area}</h2></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card"><h3>🛏 Bedrooms</h3><h2>{bedrooms}</h2></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="card"><h3>📍 Location</h3><h2>{location}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ================= TABS =================
    tab1, tab2, tab3 = st.tabs(["💡 Price Breakdown", "📊 Market Compare", "🧾 Report"])

    # 💡 PRICE BREAKDOWN
    with tab1:
        st.subheader("💡 Feature Impact")

        impact = {
            "Area": area * 10,
            "Bedrooms": bedrooms * 50000,
            "Bathrooms": bathrooms * 30000,
            "Parking": parking * 20000
        }

        df_imp = pd.DataFrame(list(impact.items()), columns=["Feature", "Impact"])
        st.bar_chart(df_imp.set_index("Feature"))

    # 📊 MARKET COMPARISON
    with tab2:
        st.subheader("📊 Market Comparison")

        avg_price = {
            "Mumbai": 8000000,
            "Pune": 6000000,
            "Nashik": 4000000
        }

        market = avg_price.get(location, 5000000)

        st.metric("Your Price", f"₹ {round(prediction):,}")
        st.metric("Market Avg", f"₹ {market:,}")

        if prediction > market:
            st.warning("⚠ Above Market Price")
        else:
            st.success("✅ Good Deal")

    # 🧾 REPORT
    with tab3:
        st.subheader("🧾 Property Report")

        report = f"""
Location: {location}
Area: {area}
Bedrooms: {bedrooms}
Bathrooms: {bathrooms}
Price: ₹ {round(prediction):,}
"""

        st.text(report)
        st.download_button("📥 Download Report", report)

# ================= FOOTER =================
st.markdown("---")
st.caption("🚀 House Price Prediction Model")
