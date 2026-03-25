import streamlit as st
import numpy as np
import pandas as pd
import pickle

# ================= LOAD MODEL =================
with open('model.pkl', 'rb') as f:
    model, feature_columns = pickle.load(f)

st.set_page_config(page_title="Gaming House Dashboard", layout="wide")

# ================= PARTICLE + UI =================
st.markdown("""
<style>

/* BLACK BACKGROUND */
body {
    background: #000000;
    color: white;
}

/* PARTICLES */
#particles-js {
    position: fixed;
    width: 100%;
    height: 100%;
    z-index: -1;
}

/* TITLE */
.title {
    font-size: 42px;
    text-align: center;
    font-weight: bold;
    color: #00f2fe;
    text-shadow: 0 0 20px #00f2fe;
}

/* CARDS */
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.9);
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.05);
}

/* BUTTON */
.stButton > button {
    background-color: black;
    color: white;
    border: 1px solid #00f2fe;
    border-radius: 10px;
}

</style>

<div id="particles-js"></div>

<script src="https://cdn.jsdelivr.net/npm/particles.js"></script>
<script>
particlesJS("particles-js", {
  "particles": {
    "number": {"value": 80},
    "size": {"value": 3},
    "color": {"value": "#00f2fe"},
    "line_linked": {
      "enable": true,
      "distance": 150,
      "color": "#00f2fe",
      "opacity": 0.4
    },
    "move": {
      "enable": true,
      "speed": 2
    }
  }
});
</script>

""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown('<div class="title">🏡 House Price Predication  </div>', unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.header("📥 Property Details")

cities = ["Mumbai", "Pune", "Nashik"]
location = st.sidebar.selectbox("📍 Select City", cities)

area = st.sidebar.slider("Area", 500, 10000, 2000)
bedrooms = st.sidebar.slider("Bedrooms", 1, 5, 3)
bathrooms = st.sidebar.slider("Bathrooms", 1, 4, 2)
stories = st.sidebar.slider("Stories", 1, 4, 2)
parking = st.sidebar.slider("Parking", 0, 3, 1)

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

    # ================= UNIQUE FEATURES =================
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

        market = avg_price[location]

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
st.caption("🚀 House Price Predication  ")
