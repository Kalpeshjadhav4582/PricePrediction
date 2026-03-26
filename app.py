import streamlit as st
import numpy as np
import pandas as pd
import pickle

# ================= LOAD MODEL =================
with open('model.pkl', 'rb') as f:
    model, feature_columns = pickle.load(f)

st.set_page_config(page_title="Gaming House Dashboard", layout="wide")

# ================= ADVANCED UI =================
st.markdown("""
<style>

/* BACKGROUND */
body {
    background: radial-gradient(circle at top, #0f2027, #000000);
    color: white;
}

/* TITLE */
.title {
    font-size: 50px;
    text-align: center;
    font-weight: bold;
    color: #00f2fe;
    text-shadow: 0 0 25px #00f2fe, 0 0 50px #00f2fe;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px #00f2fe; }
    to { text-shadow: 0 0 40px #00f2fe; }
}

/* 3D CARD */
.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    text-align: center;
    box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    transform-style: preserve-3d;
    transition: transform 0.4s, box-shadow 0.4s;
}

/* 3D HOVER */
.card:hover {
    transform: rotateY(15deg) rotateX(10deg) scale(1.08);
    box-shadow: 0 0 40px #00f2fe;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(45deg, #00f2fe, #4facfe);
    color: black;
    border-radius: 12px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.1);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.8);
    box-shadow: 0 0 20px #00f2fe;
}

</style>

<script>
// MOUSE PARALLAX EFFECT
document.addEventListener("mousemove", (e) => {
    let x = (window.innerWidth / 2 - e.pageX) / 25;
    let y = (window.innerHeight / 2 - e.pageY) / 25;

    document.querySelectorAll(".card").forEach(card => {
        card.style.transform = `rotateY(${x}deg) rotateX(${y}deg)`;
    });
});
</script>

""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown('<div class="title">🏡 3D House Price Predictor</div>', unsafe_allow_html=True)

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

# ================= INPUT =================
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

    col1.markdown(f"""
    <div class="card">
    <h3>💰 Price</h3>
    <h2 id="price">0</h2>
    </div>

    <script>
    let target = {round(prediction)};
    let count = 0;
    let speed = target / 50;

    let interval = setInterval(() => {{
        count += speed;
        if(count >= target) {{
            count = target;
            clearInterval(interval);
        }}
        document.getElementById("price").innerText = "₹ " + Math.floor(count).toLocaleString();
    }}, 20);
    </script>
    """, unsafe_allow_html=True)

    col2.markdown(f'<div class="card"><h3>📐 Area</h3><h2>{area}</h2></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card"><h3>🛏 Bedrooms</h3><h2>{bedrooms}</h2></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="card"><h3>📍 Location</h3><h2>{location}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ================= 3D MODEL =================
    st.markdown("### 🏠 3D House View")

    st.components.v1.html("""
    <iframe src="https://my.spline.design/housemodel/"
    frameborder="0"
    width="100%"
    height="500px"></iframe>
    """, height=500)

    # ================= TABS =================
    tab1, tab2, tab3 = st.tabs(["💡 Price Breakdown", "📊 Market Compare", "🧾 Report"])

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
st.caption("🚀 Advanced 3D House Price Prediction Dashboard")