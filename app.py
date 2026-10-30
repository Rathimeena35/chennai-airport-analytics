
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Chennai Airport | Traffic Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f7fb;
}

/* LOGIN */

.login-wrapper {
    max-width: 480px;
    margin: 80px auto;
}

.login-card {
    background: white;
    padding: 45px;
    border-radius: 22px;
    box-shadow: 0 15px 45px rgba(15, 23, 42, 0.12);
    text-align: center;
    border: 1px solid #e5e7eb;
}

.login-icon {
    width: 80px;
    height: 80px;
    margin: auto;
    background: linear-gradient(135deg, #0b3d91, #1677ff);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 42px;
}

.login-title {
    font-size: 32px;
    font-weight: 800;
    color: #102a43;
    margin-top: 20px;
}

.login-subtitle {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 25px;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071b3a 0%, #0b3d91 100%);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    font-size: 23px;
    font-weight: 800;
    padding: 10px 0 4px 0;
}

.sidebar-subtitle {
    font-size: 12px;
    opacity: 0.75;
    margin-bottom: 30px;
}

/* HEADER */

.dashboard-header {
    background: linear-gradient(135deg, #071b3a, #0b3d91, #1677ff);
    padding: 28px 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 12px 30px rgba(11,61,145,0.18);
}

.dashboard-title {
    font-size: 30px;
    font-weight: 800;
}

.dashboard-subtitle {
    font-size: 14px;
    opacity: 0.85;
    margin-top: 6px;
}

/* KPI CARDS */

.kpi-card {
    background: white;
    padding: 22px;
    border-radius: 17px;
    border: 1px solid #e6eaf0;
    box-shadow: 0 7px 20px rgba(15,23,42,0.06);
    min-height: 120px;
}

.kpi-label {
    font-size: 13px;
    color: #64748b;
    font-weight: 600;
}

.kpi-value {
    font-size: 29px;
    font-weight: 800;
    color: #102a43;
    margin-top: 10px;
}

.kpi-icon {
    font-size: 25px;
}

/* SECTION */

.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #102a43;
    margin: 25px 0 12px 0;
}

/* INFO CARD */

.info-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 7px 20px rgba(15,23,42,0.05);
}

/* FOOTER */

.footer {
    text-align: center;
    padding: 30px;
    color: #64748b;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-icon">✈️</div>
            <div class="login-title">Chennai Airport</div>
            <div class="login-subtitle">Traffic Analytics Portal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        login = st.button("🔐  LOGIN TO DASHBOARD", use_container_width=True)
        if login:
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

    st.markdown("""
    <div class="footer">
        Chennai Airport Traffic Analytics • Academic Project
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================================
# DATA
# ============================================================
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
destinations = ["Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Kolkata", "Pune", "Kochi", "Ahmedabad", "Goa", "Bhubaneswar"]

np.random.seed(42)
rows = []
for month_index, month in enumerate(months):
    for destination in destinations:
        passenger_from = int(np.random.randint(50000, 120000))
        passenger_to = int(np.random.randint(45000, 115000))
        freight_from = round(np.random.uniform(200, 1200), 2)
        freight_to = round(np.random.uniform(200, 1100), 2)
        mail_from = round(np.random.uniform(10, 80), 2)
        mail_to = round(np.random.uniform(10, 80), 2)
        rows.append({
            "Year": 2025,
            "Month": month,
            "Origin": "Chennai",
            "Dest": destination,
            "Pax From Origin": passenger_from,
            "Pax To Origin": passenger_to,
            "Freight From Origin": freight_from,
            "Freight To Origin": freight_to,
            "Mail From Origin": mail_from,
            "Mail To Origin": mail_to
        })

df = pd.DataFrame(rows)

# ============================================================
# OPTIONAL CSV UPLOAD
# ============================================================
uploaded_file = None
with st.sidebar:
    st.markdown('<div class="sidebar-title">✈️ Chennai Airport</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Traffic Analytics Portal</div>', unsafe_allow_html=True)
    st.divider()
    page = st.radio("Navigation", ["🏠 Overview", "👥 Passenger Analytics", "✈️ Route Analytics", "📦 Freight & Mail", "📈 Trends", "ℹ️ About"])
    st.divider()
    uploaded_file = st.file_uploader("Upload Chennai Airport CSV", type=["csv"])
    st.divider()
    st.write(f"👤 Logged in as: **{st.session_state.username}**")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

if uploaded_file is not None:
    try:
        uploaded_df = pd.read_csv(uploaded_file)
        uploaded_df.columns = uploaded_df.columns.str.strip()
        if "Frieght To Origin" in uploaded_df.columns:
            uploaded_df.rename(columns={"Frieght To Origin": "Freight To Origin"}, inplace=True)
        required_columns = ["Month", "Dest", "Pax From Origin", "Pax To Origin", "Freight From Origin", "Freight To Origin", "Mail From Origin", "Mail To Origin"]
        if all(column in uploaded_df.columns for column in required_columns):
            df = uploaded_df.copy()
            st.sidebar.success("CSV loaded successfully!")
        else:
            st.sidebar.warning("CSV structure differs from expected dataset. Demo data is being used.")
    except Exception as e:
        st.sidebar.error("Could not read CSV.")

# ============================================================
# CALCULATED COLUMNS
# ============================================================
df["Total Passenger"] = pd.to_numeric(df["Pax From Origin"], errors="coerce").fillna(0) + pd.to_numeric(df["Pax To Origin"], errors="coerce").fillna(0)
df["Total Freight"] = pd.to_numeric(df["Freight From Origin"], errors="coerce").fillna(0) + pd.to_numeric(df["Freight To Origin"], errors="coerce").fillna(0)
df["Total Mail"] = pd.to_numeric(df["Mail From Origin"], errors="coerce").fillna(0) + pd.to_numeric(df["Mail To Origin"], errors="coerce").fillna(0)
df["Route"] = df["Origin"].astype(str) + " → " + df["Dest"].astype(str)

# ============================================================
# FILTERS
# ============================================================
with st.sidebar:
    st.markdown("### 🎛️ Filters")
    selected_month = st.selectbox("Month", ["All"] + sorted(df["Month"].dropna().unique().tolist()))
    selected_destination = st.selectbox("Destination", ["All"] + sorted(df["Dest"].dropna().unique().tolist()))

filtered_df = df.copy()
if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month"] == selected_month]
if selected_destination != "All":
    filtered_df = filtered_df[filtered_df["Dest"] == selected_destination]

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="dashboard-header">
<div class="dashboard-title">✈️ Chennai Airport Traffic Analytics</div>
<div class="dashboard-subtitle">Domestic Passenger & Aviation Traffic • 2025</div>
</div>
""", unsafe_allow_html=True)

total_routes = filtered_df["Route"].nunique()
total_passengers = filtered_df["Total Passenger"].sum()
total_freight = filtered_df["Total Freight"].sum()
total_mail = filtered_df["Total Mail"].sum()

# ============================================================
# KPI CARDS
# ============================================================
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-icon">🛫</div><div class="kpi-label">TOTAL ROUTES</div><div class="kpi-value">{total_routes:,}</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-icon">👥</div><div class="kpi-label">PASSENGER TRAFFIC</div><div class="kpi-value">{total_passengers/1_000_000:.2f}M</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-icon">📦</div><div class="kpi-label">TOTAL FREIGHT</div><div class="kpi-value">{total_freight:,.0f}</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-icon">✉️</div><div class="kpi-label">TOTAL MAIL</div><div class="kpi-value">{total_mail:,.0f}</div></div>', unsafe_allow_html=True)

# ============================================================
# OVERVIEW
# ============================================================
if page == "🏠 Overview":
    st.markdown("<div class=\"section-title\">📊 Airport Performance Overview</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        monthly = filtered_df.groupby("Month", as_index=False)["Total Passenger"].sum()
        monthly["Month"] = pd.Categorical(monthly["Month"], categories=months, ordered=True)
        monthly = monthly.sort_values("Month")
        fig = px.line(monthly, x="Month", y="Total Passenger", markers=True, title="Monthly Passenger Traffic")
        fig.update_layout(template="plotly_white", height=400, margin=dict(l=20,r=20,t=60,b=20), xaxis_title="Month", yaxis_title="Passengers")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        destination_data = filtered_df.groupby("Dest", as_index=False)["Total Passenger"].sum().sort_values("Total Passenger", ascending=False).head(10)
        fig = px.bar(destination_data, x="Total Passenger", y="Dest", orientation="h", title="Top 10 Destinations by Passenger Traffic")
        fig.update_layout(template="plotly_white", height=400, margin=dict(l=20,r=20,t=60,b=20), yaxis_title="Destination", xaxis_title="Passengers")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        freight_data = filtered_df.groupby("Dest", as_index=False)["Total Freight"].sum().sort_values("Total Freight", ascending=False).head(10)
        fig = px.treemap(freight_data, path=["Dest"], values="Total Freight", title="Top 10 Destinations by Freight")
        fig.update_layout(height=430, margin=dict(l=10,r=10,t=60,b=10))
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        flow_data = pd.DataFrame({"Flow": ["Passengers From Chennai", "Passengers To Chennai"], "Passengers": [filtered_df["Pax From Origin"].sum(), filtered_df["Pax To Origin"].sum()]})
        fig = px.pie(flow_data, names="Flow", values="Passengers", hole=0.55, title="Passenger Flow: From vs To Chennai")
        fig.update_layout(height=430, margin=dict(l=10,r=10,t=60,b=10))
        st.plotly_chart(fig, use_container_width=True)

elif page == "👥 Passenger Analytics":
    st.markdown("<div class=\"section-title\">👥 Passenger Analytics</div>", unsafe_allow_html=True)
    destination_data = filtered_df.groupby("Dest", as_index=False)["Total Passenger"].sum().sort_values("Total Passenger", ascending=False)
    fig = px.bar(destination_data.head(15), x="Dest", y="Total Passenger", title="Passenger Traffic by Destination")
    fig.update_layout(template="plotly_white", height=480)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(destination_data, use_container_width=True, hide_index=True)

elif page == "✈️ Route Analytics":
    st.markdown("<div class=\"section-title\">✈️ Route Analytics</div>", unsafe_allow_html=True)
    route_data = filtered_df.groupby("Route", as_index=False).agg({"Total Passenger": "sum", "Total Freight": "sum"})
    fig = px.scatter(route_data, x="Total Passenger", y="Total Freight", size="Total Passenger", hover_name="Route", title="Passenger Traffic vs Freight by Route")
    fig.update_layout(template="plotly_white", height=520)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(route_data.sort_values("Total Passenger", ascending=False), use_container_width=True, hide_index=True)

elif page == "📦 Freight & Mail":
    st.markdown("<div class=\"section-title\">📦 Freight & Mail Analytics</div>", unsafe_allow_html=True)
    freight = filtered_df.groupby("Dest", as_index=False)["Total Freight"].sum().sort_values("Total Freight", ascending=False).head(15)
    fig = px.bar(freight, x="Dest", y="Total Freight", title="Freight Volume by Destination")
    fig.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig, use_container_width=True)

    mail = filtered_df.groupby("Dest", as_index=False)["Total Mail"].sum().sort_values("Total Mail", ascending=False).head(15)
    fig2 = px.bar(mail, x="Dest", y="Total Mail", title="Mail Volume by Destination")
    fig2.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig2, use_container_width=True)

elif page == "📈 Trends":
    st.markdown("<div class=\"section-title\">📈 Traffic Trends</div>", unsafe_allow_html=True)
    monthly = filtered_df.groupby("Month", as_index=False).agg({"Total Passenger": "sum", "Total Freight": "sum", "Total Mail": "sum"})
    monthly["Month"] = pd.Categorical(monthly["Month"], categories=months, ordered=True)
    monthly = monthly.sort_values("Month")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Total Passenger"], mode="lines+markers", name="Passengers"))
    fig.update_layout(title="Passenger Traffic Trend", template="plotly_white", height=450)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Total Freight"], mode="lines+markers", name="Freight"))
    fig2.update_layout(title="Freight Trend", template="plotly_white", height=450)
    st.plotly_chart(fig2, use_container_width=True)

elif page == "ℹ️ About":
    st.markdown("<div class=\"section-title\">ℹ️ About the Application</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
    <h2>Chennai Airport Traffic Analytics</h2>
    <p>This application provides an interactive analytical view of domestic aviation traffic associated with Chennai Airport.</p>
    <h3>Key analytical areas</h3>
    <ul>
        <li>Passenger traffic analysis</li>
        <li>Destination and route analysis</li>
        <li>Freight volume analysis</li>
        <li>Mail traffic analysis</li>
        <li>Monthly traffic trends</li>
        <li>Passenger flow analysis</li>
    </ul>
    <h3>Technology Stack</h3>
    <p>Python • Streamlit • Pandas • Plotly • Data Visualization</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Chennai Airport Traffic Analytics • MSc Data Science Mini Project<br>Interactive Analytics Application
</div>
""", unsafe_allow_html=True)