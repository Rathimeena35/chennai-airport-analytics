import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Chennai Airport | Traffic Analytics", page_icon="✈️",
                   layout="wide", initial_sidebar_state="expanded")

def H(s):
    """Strip indentation so Markdown never treats HTML as a code block."""
    return "".join(line.strip() for line in s.splitlines())

# ---------------------------- CSS ----------------------------
st.markdown(H("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f1f5fb; }
#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 1.4rem; padding-bottom: 2rem; }

section[data-testid="stSidebar"] { background: linear-gradient(180deg,#06142e 0%,#0b3d91 100%); }
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] span.st-emotion-cache-ue6h4q,
section[data-testid="stSidebar"] .stRadio div { color: #ffffff !important; }
section[data-testid="stSidebar"] div[data-baseweb="select"] * { color: #102a43 !important; }
.sidebar-title { font-size: 23px; font-weight: 800; color: #fff; padding: 6px 0 2px 0; }
.sidebar-sub { font-size: 12px; color: #cbd5e1; margin-bottom: 8px; }

.dash-header { background: linear-gradient(120deg,#06142e,#0b3d91 55%,#1677ff); padding: 30px 34px;
  border-radius: 22px; color: #fff; margin-bottom: 22px; box-shadow: 0 14px 34px rgba(11,61,145,.22); position: relative; overflow: hidden; }
.dash-header:after { content: "✈"; position: absolute; right: 30px; top: -10px; font-size: 140px; opacity: .08; }
.dash-title { font-size: 31px; font-weight: 800; }
.dash-sub { font-size: 14px; opacity: .85; margin-top: 6px; }
.pill { display:inline-block; background: rgba(255,255,255,.16); padding: 4px 12px; border-radius: 999px;
  font-size: 12px; margin: 10px 6px 0 0; }

.kpi { background:#fff; padding: 18px 20px; border-radius: 18px; border: 1px solid #e3e9f2;
  box-shadow: 0 8px 22px rgba(15,23,42,.06); border-left: 5px solid #1677ff; transition: all .2s; }
.kpi:hover { transform: translateY(-3px); box-shadow: 0 14px 28px rgba(15,23,42,.12); }
.kpi-icon { font-size: 22px; }
.kpi-label { font-size: 11.5px; color:#64748b; font-weight: 700; letter-spacing: .6px; margin-top: 4px; }
.kpi-value { font-size: 26px; font-weight: 800; color:#102a43; margin-top: 4px; }

.section-title { font-size: 21px; font-weight: 800; color:#102a43; margin: 24px 0 10px 0; }
.info-card { background:#fff; padding: 26px 30px; border-radius: 18px; border: 1px solid #e5e7eb;
  box-shadow: 0 8px 22px rgba(15,23,42,.05); margin-bottom: 16px; }
.info-card h2 { color:#0b3d91; margin-top:0; }
.info-card h3 { color:#102a43; }
.info-card p, .info-card li { color:#334155; font-size: 15px; line-height: 1.7; }
.insight { background:#fff; border-left: 5px solid #16a34a; padding: 14px 18px; border-radius: 12px;
  margin-bottom: 10px; box-shadow: 0 5px 14px rgba(15,23,42,.05); color:#1e293b; font-size: 15px; }
.chip { display:inline-block; background:#e8f0ff; color:#0b3d91; padding: 6px 14px; border-radius: 999px;
  font-weight: 600; font-size: 13px; margin: 4px 6px 4px 0; }
.login-card { background:#fff; padding: 36px; border-radius: 22px; box-shadow: 0 16px 46px rgba(15,23,42,.14);
  text-align:center; border: 1px solid #e5e7eb; margin-top: 50px; }
.login-icon { width: 78px; height: 78px; margin: auto; background: linear-gradient(135deg,#0b3d91,#1677ff);
  border-radius: 20px; display:flex; align-items:center; justify-content:center; font-size: 40px; }
.login-title { font-size: 30px; font-weight: 800; color:#102a43; margin-top: 16px; }
.login-sub { color:#64748b; font-size: 14px; }
.footer { text-align:center; padding: 28px; color:#64748b; font-size: 12px; }
</style>
"""), unsafe_allow_html=True)

# ---------------------------- SESSION ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------------------- LOGIN ----------------------------
if not st.session_state.logged_in:
    _, mid, _ = st.columns([1, 1.3, 1])
    with mid:
        st.markdown(H("""
        <div class="login-card">
          <div class="login-icon">✈️</div>
          <div class="login-title">Chennai Airport</div>
          <div class="login-sub">Traffic Analytics Portal</div>
        </div>
        """), unsafe_allow_html=True)
        st.write("")
        with st.form("login_form"):
            u = st.text_input("Username", placeholder="Enter your username")
            p = st.text_input("Password", type="password", placeholder="Enter your password")
            ok = st.form_submit_button("🔐  LOGIN TO DASHBOARD", use_container_width=True)
        if ok:
            if u == "admin" and p == "1234":
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.markdown('<div class="footer">Chennai Airport Traffic Analytics • Academic Project<br>Demo login: admin / 1234</div>',
                    unsafe_allow_html=True)
    st.stop()

# ---------------------------- DATA ----------------------------
CHN_LAT, CHN_LON = 12.9941, 80.1709

MONTHS = ["January","February","March","April","May","June","July","August","September","October"]
SEASON = [1.00, 0.92, 0.98, 1.10, 1.18, 1.08, 0.95, 0.97, 0.99, 1.12]

# name: (lat, lon, state, popularity weight)
DEST = {
    "Delhi":        (28.5562, 77.1000, "Delhi", 1.00),
    "Mumbai":       (19.0896, 72.8656, "Maharashtra", 0.95),
    "Bengaluru":    (13.1986, 77.7066, "Karnataka", 1.05),
    "Hyderabad":    (17.2403, 78.4294, "Telangana", 0.85),
    "Kolkata":      (22.6547, 88.4467, "West Bengal", 0.65),
    "Pune":         (18.5821, 73.9197, "Maharashtra", 0.40),
    "Kochi":        (10.1520, 76.4019, "Kerala", 0.45),
    "Ahmedabad":    (23.0772, 72.6347, "Gujarat", 0.38),
    "Goa":          (15.3808, 73.8314, "Goa", 0.35),
    "Bhubaneswar":  (20.2444, 85.8178, "Odisha", 0.22),
    "Visakhapatnam":(17.7212, 83.2245, "Andhra Pradesh", 0.28),
    "Coimbatore":   (11.0300, 77.0434, "Tamil Nadu", 0.42),
    "Madurai":      (9.8345,  78.0934, "Tamil Nadu", 0.36),
    "Thiruvananthapuram": (8.4821, 76.9201, "Kerala", 0.26),
    "Jaipur":       (26.8242, 75.8122, "Rajasthan", 0.24),
    "Lucknow":      (26.7606, 80.8893, "Uttar Pradesh", 0.23),
    "Guwahati":     (26.1061, 91.5859, "Assam", 0.20),
    "Port Blair":   (11.6412, 92.7297, "A&N Islands", 0.15),
}

@st.cache_data
def build_data():
    rng = np.random.default_rng(42)
    rows = []
    for mi, month in enumerate(MONTHS):
        for d, (lat, lon, state, w) in DEST.items():
            s = SEASON[mi]
            rows.append({
                "Year": 2025, "Month": month, "Origin": "Chennai", "Dest": d, "State": state,
                "Lat": lat, "Lon": lon,
                "Pax From Origin": int(200000 * w * s * rng.uniform(0.85, 1.15)),
                "Pax To Origin":   int(190000 * w * s * rng.uniform(0.85, 1.15)),
                "Freight From Origin": round(1500 * w * s * rng.uniform(0.7, 1.3), 2),
                "Freight To Origin":   round(1300 * w * s * rng.uniform(0.7, 1.3), 2),
                "Mail From Origin": round(90 * w * s * rng.uniform(0.7, 1.3), 2),
                "Mail To Origin":   round(85 * w * s * rng.uniform(0.7, 1.3), 2),
            })
    d = pd.DataFrame(rows)
    d["Total Passenger"] = d["Pax From Origin"] + d["Pax To Origin"]
    d["Total Freight"] = d["Freight From Origin"] + d["Freight To Origin"]
    d["Total Mail"] = d["Mail From Origin"] + d["Mail To Origin"]
    d["Route"] = d["Origin"] + " → " + d["Dest"]
    return d

df = build_data()

METRICS = {"Passengers": "Total Passenger", "Freight (tonnes)": "Total Freight", "Mail (tonnes)": "Total Mail"}

# ---------------------------- SIDEBAR ----------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">✈️ Chennai Airport</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Traffic Analytics Portal</div>', unsafe_allow_html=True)
    st.divider()
    page = st.radio("Navigation", [
        "🏠 Overview", "🗺️ Route Map", "👥 Passenger Analytics", "✈️ Route Analytics",
        "📦 Freight & Mail", "📈 Trends & Seasonality", "⚖️ Compare Destinations",
        "💡 Auto Insights", "🔎 Data Explorer", "ℹ️ About"])
    st.divider()
    st.markdown("### 🎛️ Filters")
    m_from, m_to = st.select_slider("Month range", options=MONTHS, value=(MONTHS[0], MONTHS[-1]))
    sel_dest = st.multiselect("Destinations (empty = all)", sorted(df["Dest"].unique()))
    sel_state = st.multiselect("States (empty = all)", sorted(df["State"].unique()))
    metric_label = st.selectbox("Primary metric", list(METRICS.keys()))
    direction = st.radio("Direction (passengers)", ["Both", "From Chennai", "To Chennai"], horizontal=True)
    top_n = st.slider("Top N destinations", 3, len(DEST), 10)
    st.divider()
    st.write(f"👤 Logged in as: **{st.session_state.username}**")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

metric = METRICS[metric_label]
i1, i2 = MONTHS.index(m_from), MONTHS.index(m_to)
fdf = df[df["Month"].isin(MONTHS[i1:i2 + 1])].copy()
if sel_dest:
    fdf = fdf[fdf["Dest"].isin(sel_dest)]
if sel_state:
    fdf = fdf[fdf["State"].isin(sel_state)]

# direction adjusts passenger totals
if direction == "From Chennai":
    fdf["Total Passenger"] = fdf["Pax From Origin"]
elif direction == "To Chennai":
    fdf["Total Passenger"] = fdf["Pax To Origin"]

if fdf.empty:
    st.warning("No data for the selected filters. Please adjust the filters in the sidebar.")
    st.stop()

def month_order(d):
    d = d.copy()
    d["Month"] = pd.Categorical(d["Month"], categories=MONTHS, ordered=True)
    return d.sort_values("Month")

def style(fig, h=420):
    fig.update_layout(template="plotly_white", height=h, margin=dict(l=20, r=20, t=60, b=20),
                      font=dict(family="Inter"), title_font=dict(size=17))
    return fig

PALETTE = px.colors.sequential.Blues_r

# ---------------------------- HEADER + KPI ----------------------------
st.markdown(H(f"""
<div class="dash-header">
  <div class="dash-title">✈️ Chennai Airport Traffic Analytics</div>
  <div class="dash-sub">Domestic passenger, freight & mail traffic • 2025</div>
  <span class="pill">📅 {m_from} – {m_to}</span>
  <span class="pill">🎯 {metric_label}</span>
  <span class="pill">↔️ {direction}</span>
  <span class="pill">📍 {fdf['Dest'].nunique()} destinations</span>
</div>
"""), unsafe_allow_html=True)

tot_pax = fdf["Total Passenger"].sum()
tot_out = fdf["Pax From Origin"].sum()
tot_in = fdf["Pax To Origin"].sum()
tot_fr = fdf["Total Freight"].sum()
tot_ml = fdf["Total Mail"].sum()
routes = fdf["Route"].nunique()

def kpi(icon, label, value, color="#1677ff"):
    return H(f'<div class="kpi" style="border-left-color:{color}"><div class="kpi-icon">{icon}</div>'
             f'<div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>')

c = st.columns(6)
c[0].markdown(kpi("🛫", "ROUTES", f"{routes}"), unsafe_allow_html=True)
c[1].markdown(kpi("👥", "PASSENGERS", f"{tot_pax/1e6:.2f}M", "#0b3d91"), unsafe_allow_html=True)
c[2].markdown(kpi("➡️", "OUTBOUND PAX", f"{tot_out/1e6:.2f}M", "#16a34a"), unsafe_allow_html=True)
c[3].markdown(kpi("⬅️", "INBOUND PAX", f"{tot_in/1e6:.2f}M", "#f59e0b"), unsafe_allow_html=True)
c[4].markdown(kpi("📦", "FREIGHT (T)", f"{tot_fr:,.0f}", "#8b5cf6"), unsafe_allow_html=True)
c[5].markdown(kpi("✉️", "MAIL (T)", f"{tot_ml:,.0f}", "#ef4444"), unsafe_allow_html=True)

# ---------------------------- MAP HELPERS ----------------------------
def route_map(data, metric, title):
    agg = data.groupby(["Dest", "State", "Lat", "Lon"], as_index=False)[metric].sum()
    mx = agg[metric].max() if agg[metric].max() > 0 else 1
    fig = go.Figure()
    for _, r in agg.iterrows():
        fig.add_trace(go.Scattergeo(
            lon=[CHN_LON, r["Lon"]], lat=[CHN_LAT, r["Lat"]], mode="lines",
            line=dict(width=0.8 + 4.5 * r[metric] / mx, color="rgba(22,119,255,0.45)"),
            hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scattergeo(
        lon=agg["Lon"], lat=agg["Lat"], mode="markers+text", text=agg["Dest"], textposition="top center",
        textfont=dict(size=10, color="#102a43"),
        marker=dict(size=9 + 30 * agg[metric] / mx, color=agg[metric], colorscale="YlOrRd",
                    showscale=True, colorbar=dict(title=metric_label, thickness=12),
                    line=dict(width=1, color="white"), opacity=.9),
        customdata=np.stack([agg["State"], agg[metric]], axis=-1),
        hovertemplate="<b>%{text}</b><br>%{customdata[0]}<br>" + metric_label + ": %{customdata[1]:,.0f}<extra></extra>",
        showlegend=False))
    fig.add_trace(go.Scattergeo(
        lon=[CHN_LON], lat=[CHN_LAT], mode="markers+text", text=["Chennai (MAA)"], textposition="bottom center",
        marker=dict(size=20, color="#dc2626", symbol="star", line=dict(width=1.5, color="white")),
        hovertemplate="<b>Chennai International Airport</b><extra></extra>", showlegend=False))
    fig.update_geos(scope="asia", projection_type="mercator", lonaxis_range=[66, 99], lataxis_range=[5, 35],
                    showland=True, landcolor="#eef2f7", showocean=True, oceancolor="#dbeafe",
                    showcountries=True, countrycolor="#94a3b8", showcoastlines=True, coastlinecolor="#94a3b8",
                    showlakes=False, bgcolor="rgba(0,0,0,0)")
    fig.update_layout(title=title, height=640, margin=dict(l=0, r=0, t=55, b=0), font=dict(family="Inter"))
    return fig

# ============================================================
# PAGES
# ============================================================
if page == "🏠 Overview":
    st.markdown('<div class="section-title">📊 Airport Performance Overview</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        mo = month_order(fdf.groupby("Month", as_index=False)[metric].sum())
        fig = px.area(mo, x="Month", y=metric, markers=True, title=f"Monthly {metric_label}",
                      color_discrete_sequence=["#1677ff"])
        st.plotly_chart(style(fig), use_container_width=True)
    with b:
        dd = fdf.groupby("Dest", as_index=False)[metric].sum().sort_values(metric, ascending=False).head(top_n)
        fig = px.bar(dd.sort_values(metric), x=metric, y="Dest", orientation="h",
                     title=f"Top {top_n} Destinations by {metric_label}", color=metric, color_continuous_scale="Blues")
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(style(fig), use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        tm = fdf.groupby(["State", "Dest"], as_index=False)[metric].sum()
        fig = px.treemap(tm, path=["State", "Dest"], values=metric, title=f"{metric_label} by State & Destination",
                         color=metric, color_continuous_scale="Blues")
        st.plotly_chart(style(fig, 440), use_container_width=True)
    with c2:
        flow = pd.DataFrame({"Flow": ["From Chennai", "To Chennai"], "Passengers": [tot_out, tot_in]})
        fig = px.pie(flow, names="Flow", values="Passengers", hole=.6, title="Passenger Flow: From vs To Chennai",
                     color_discrete_sequence=["#0b3d91", "#f59e0b"])
        st.plotly_chart(style(fig, 440), use_container_width=True)

    st.markdown('<div class="section-title">🌍 Network Snapshot</div>', unsafe_allow_html=True)
    st.plotly_chart(route_map(fdf, metric, f"Chennai Route Network – {metric_label}"), use_container_width=True)

elif page == "🗺️ Route Map":
    st.markdown('<div class="section-title">🗺️ Route Maps</div>', unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["✈️ Route Network", "📍 Street Map", "🏛️ State-wise Traffic"])
    with t1:
        st.plotly_chart(route_map(fdf, metric, f"Chennai Route Network – {metric_label}"), use_container_width=True)
        st.caption("Line thickness and bubble size represent traffic volume. Star = Chennai (MAA).")
    with t2:
        agg = fdf.groupby(["Dest", "Lat", "Lon"], as_index=False)[metric].sum()
        agg["size"] = 8000 + 60000 * agg[metric] / agg[metric].max()
        mp = agg.rename(columns={"Lat": "lat", "Lon": "lon"})
        st.map(mp, latitude="lat", longitude="lon", size="size", color="#1677ff", zoom=4, height=600)
        st.caption("Interactive street map – drag, scroll to zoom. Bubble size ∝ traffic.")
    with t3:
        sd = fdf.groupby("State", as_index=False)[metric].sum().sort_values(metric, ascending=False)
        st_pos = fdf.groupby("State", as_index=False)[["Lat", "Lon"]].mean()
        sd = sd.merge(st_pos, on="State")
        fig = px.scatter_geo(sd, lat="Lat", lon="Lon", size=metric, color=metric, hover_name="State",
                             color_continuous_scale="Turbo", size_max=55, title=f"{metric_label} by State")
        fig.update_geos(scope="asia", projection_type="mercator", lonaxis_range=[66, 99], lataxis_range=[5, 35],
                        showland=True, landcolor="#eef2f7", showocean=True, oceancolor="#dbeafe",
                        showcountries=True, countrycolor="#94a3b8")
        fig.update_layout(height=620, margin=dict(l=0, r=0, t=55, b=0), font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.bar(sd, x="State", y=metric, color=metric, color_continuous_scale="Blues", title="State Ranking")
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(style(fig2), use_container_width=True)

elif page == "👥 Passenger Analytics":
    st.markdown('<div class="section-title">👥 Passenger Analytics</div>', unsafe_allow_html=True)
    dd = fdf.groupby("Dest", as_index=False).agg(
        Outbound=("Pax From Origin", "sum"), Inbound=("Pax To Origin", "sum"), Total=("Total Passenger", "sum")
    ).sort_values("Total", ascending=False)
    top = dd.head(top_n)
    fig = go.Figure()
    fig.add_bar(x=top["Dest"], y=top["Outbound"], name="From Chennai", marker_color="#0b3d91")
    fig.add_bar(x=top["Dest"], y=top["Inbound"], name="To Chennai", marker_color="#f59e0b")
    fig.update_layout(barmode="group", title="Outbound vs Inbound Passengers by Destination")
    st.plotly_chart(style(fig, 470), use_container_width=True)
    a, b = st.columns(2)
    with a:
        fig = px.pie(top, names="Dest", values="Total", hole=.45, title="Passenger Share (Top N)",
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(style(fig, 430), use_container_width=True)
    with b:
        dd["Balance %"] = ((dd["Outbound"] - dd["Inbound"]) / dd["Total"] * 100).round(2)
        fig = px.bar(dd.sort_values("Balance %"), x="Balance %", y="Dest", orientation="h",
                     title="Outbound − Inbound Imbalance (%)", color="Balance %", color_continuous_scale="RdBu")
        st.plotly_chart(style(fig, 430), use_container_width=True)
    st.dataframe(dd, use_container_width=True, hide_index=True)

elif page == "✈️ Route Analytics":
    st.markdown('<div class="section-title">✈️ Route Analytics</div>', unsafe_allow_html=True)
    rd = fdf.groupby("Route", as_index=False).agg({"Total Passenger": "sum", "Total Freight": "sum", "Total Mail": "sum"})
    rd["Freight per 1000 Pax"] = (rd["Total Freight"] / rd["Total Passenger"] * 1000).round(2)
    fig = px.scatter(rd, x="Total Passenger", y="Total Freight", size="Total Mail", color="Freight per 1000 Pax",
                     hover_name="Route", title="Passengers vs Freight (bubble = Mail)", color_continuous_scale="Viridis",
                     size_max=45)
    st.plotly_chart(style(fig, 520), use_container_width=True)
    a, b = st.columns(2)
    with a:
        fig = px.bar(rd.sort_values("Total Passenger", ascending=False).head(top_n), x="Route", y="Total Passenger",
                     title=f"Top {top_n} Busiest Routes", color="Total Passenger", color_continuous_scale="Blues")
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(style(fig), use_container_width=True)
    with b:
        sb = px.sunburst(fdf, path=["State", "Dest"], values=metric, title="Traffic Hierarchy")
        st.plotly_chart(style(sb), use_container_width=True)
    st.dataframe(rd.sort_values("Total Passenger", ascending=False), use_container_width=True, hide_index=True)

elif page == "📦 Freight & Mail":
    st.markdown('<div class="section-title">📦 Freight & Mail Analytics</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        fr = fdf.groupby("Dest", as_index=False).agg(
            From=("Freight From Origin", "sum"), To=("Freight To Origin", "sum"), Total=("Total Freight", "sum")
        ).sort_values("Total", ascending=False).head(top_n)
        fig = go.Figure()
        fig.add_bar(x=fr["Dest"], y=fr["From"], name="From Chennai", marker_color="#8b5cf6")
        fig.add_bar(x=fr["Dest"], y=fr["To"], name="To Chennai", marker_color="#c4b5fd")
        fig.update_layout(barmode="stack", title="Freight Volume (tonnes)")
        st.plotly_chart(style(fig, 450), use_container_width=True)
    with b:
        ml = fdf.groupby("Dest", as_index=False).agg(
            From=("Mail From Origin", "sum"), To=("Mail To Origin", "sum"), Total=("Total Mail", "sum")
        ).sort_values("Total", ascending=False).head(top_n)
        fig = go.Figure()
        fig.add_bar(x=ml["Dest"], y=ml["From"], name="From Chennai", marker_color="#ef4444")
        fig.add_bar(x=ml["Dest"], y=ml["To"], name="To Chennai", marker_color="#fca5a5")
        fig.update_layout(barmode="stack", title="Mail Volume (tonnes)")
        st.plotly_chart(style(fig, 450), use_container_width=True)
    mo = month_order(fdf.groupby("Month", as_index=False).agg({"Total Freight": "sum", "Total Mail": "sum"}))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mo["Month"], y=mo["Total Freight"], name="Freight", mode="lines+markers", line=dict(color="#8b5cf6")))
    fig.add_trace(go.Scatter(x=mo["Month"], y=mo["Total Mail"], name="Mail", mode="lines+markers", yaxis="y2", line=dict(color="#ef4444")))
    fig.update_layout(title="Freight vs Mail – Monthly", yaxis=dict(title="Freight (t)"),
                      yaxis2=dict(title="Mail (t)", overlaying="y", side="right"))
    st.plotly_chart(style(fig, 440), use_container_width=True)
    st.markdown('<div class="section-title">🗺️ Freight Map</div>', unsafe_allow_html=True)
    st.plotly_chart(route_map(fdf, "Total Freight", "Freight Flow Map (tonnes)"), use_container_width=True)

elif page == "📈 Trends & Seasonality":
    st.markdown('<div class="section-title">📈 Traffic Trends & Seasonality</div>', unsafe_allow_html=True)
    mo = month_order(fdf.groupby("Month", as_index=False).agg(
        {"Total Passenger": "sum", "Total Freight": "sum", "Total Mail": "sum"}))
    mo["MoM Growth %"] = mo[metric].pct_change().mul(100).round(2)
    mo["Rolling 3M"] = mo[metric].rolling(3).mean()
    fig = go.Figure()
    fig.add_bar(x=mo["Month"], y=mo[metric], name=metric_label, marker_color="#93c5fd")
    fig.add_trace(go.Scatter(x=mo["Month"], y=mo["Rolling 3M"], name="3-month average", mode="lines+markers",
                             line=dict(color="#0b3d91", width=3)))
    fig.update_layout(title=f"{metric_label} – Monthly Trend with 3-Month Average")
    st.plotly_chart(style(fig, 450), use_container_width=True)
    a, b = st.columns(2)
    with a:
        fig = px.bar(mo, x="Month", y="MoM Growth %", title="Month-over-Month Growth (%)",
                     color="MoM Growth %", color_continuous_scale="RdYlGn")
        st.plotly_chart(style(fig), use_container_width=True)
    with b:
        piv = fdf.pivot_table(index="Dest", columns="Month", values=metric, aggfunc="sum")
        piv = piv[[m for m in MONTHS if m in piv.columns]]
        fig = px.imshow(piv, aspect="auto", color_continuous_scale="YlGnBu", title="Seasonality Heatmap (Destination × Month)")
        st.plotly_chart(style(fig, 520), use_container_width=True)
    cum = mo.copy()
    cum["Cumulative"] = cum[metric].cumsum()
    fig = px.area(cum, x="Month", y="Cumulative", title=f"Cumulative {metric_label}", color_discrete_sequence=["#16a34a"])
    st.plotly_chart(style(fig, 380), use_container_width=True)

elif page == "⚖️ Compare Destinations":
    st.markdown('<div class="section-title">⚖️ Compare Destinations</div>', unsafe_allow_html=True)
    options = sorted(fdf["Dest"].unique())
    default = options[:3] if len(options) >= 3 else options
    picks = st.multiselect("Choose 2–5 destinations to compare", options, default=default, max_selections=5)
    if len(picks) < 2:
        st.info("Select at least two destinations to compare.")
    else:
        cdf = fdf[fdf["Dest"].isin(picks)]
        mo = month_order(cdf.groupby(["Month", "Dest"], as_index=False)[metric].sum())
        fig = px.line(mo, x="Month", y=metric, color="Dest", markers=True, title=f"{metric_label} – Monthly Comparison")
        st.plotly_chart(style(fig, 450), use_container_width=True)
        sm = cdf.groupby("Dest").agg(
            Passengers=("Total Passenger", "sum"), Freight=("Total Freight", "sum"), Mail=("Total Mail", "sum"))
        norm = sm / sm.max()
        radar = go.Figure()
        for d in norm.index:
            radar.add_trace(go.Scatterpolar(r=norm.loc[d].tolist() + [norm.loc[d].iloc[0]],
                                            theta=list(norm.columns) + [norm.columns[0]], fill="toself", name=d))
        radar.update_layout(title="Normalised Profile (Radar)", polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
        a, b = st.columns(2)
        with a:
            st.plotly_chart(style(radar, 440), use_container_width=True)
        with b:
            st.markdown("**Summary table**")
            st.dataframe(sm.round(0).astype(int), use_container_width=True)

elif page == "💡 Auto Insights":
    st.markdown('<div class="section-title">💡 Auto-Generated Insights</div>', unsafe_allow_html=True)
    dd = fdf.groupby("Dest")[metric].sum().sort_values(ascending=False)
    mm = fdf.groupby("Month")[metric].sum()
    best_m, worst_m = mm.idxmax(), mm.idxmin()
    top3_share = dd.head(3).sum() / dd.sum() * 100
    imb = (tot_out - tot_in) / (tot_out + tot_in) * 100
    fpp = tot_fr / tot_pax * 1000 if tot_pax else 0
    st_top = fdf.groupby("State")[metric].sum().idxmax()
    insights = [
        f"🏆 <b>{dd.index[0]}</b> is the busiest destination with <b>{dd.iloc[0]:,.0f}</b> ({metric_label.lower()}).",
        f"📅 Peak month is <b>{best_m}</b> ({mm.max():,.0f}); lowest month is <b>{worst_m}</b> ({mm.min():,.0f}).",
        f"🔝 The top 3 destinations contribute <b>{top3_share:.1f}%</b> of total {metric_label.lower()}.",
        f"↔️ Outbound traffic is <b>{abs(imb):.2f}%</b> {'higher' if imb > 0 else 'lower'} than inbound traffic.",
        f"📦 On average, <b>{fpp:.1f} tonnes</b> of freight move per 1,000 passengers.",
        f"🏛️ <b>{st_top}</b> is the leading state by {metric_label.lower()}.",
        f"🛫 The filtered network covers <b>{routes}</b> routes across <b>{fdf['State'].nunique()}</b> states/UTs.",
    ]
    for t in insights:
        st.markdown(f'<div class="insight">{t}</div>', unsafe_allow_html=True)
    st.plotly_chart(route_map(fdf, metric, "Where the traffic goes"), use_container_width=True)

elif page == "🔎 Data Explorer":
    st.markdown('<div class="section-title">🔎 Data Explorer</div>', unsafe_allow_html=True)
    cols_all = ["Month", "Origin", "Dest", "State", "Pax From Origin", "Pax To Origin", "Total Passenger",
                "Freight From Origin", "Freight To Origin", "Total Freight",
                "Mail From Origin", "Mail To Origin", "Total Mail", "Route"]
    cols = st.multiselect("Columns to display", cols_all, default=["Month", "Dest", "State", "Total Passenger", "Total Freight", "Total Mail"])
    q = st.text_input("🔍 Search destination / state / route")
    view = fdf[cols] if cols else fdf[cols_all]
    if q:
        mask = fdf[["Dest", "State", "Route"]].apply(lambda s: s.str.contains(q, case=False, na=False)).any(axis=1)
        view = view[mask.values]
    sort_col = st.selectbox("Sort by", view.columns.tolist(), index=0)
    view = view.sort_values(sort_col, ascending=False)
    st.dataframe(view, use_container_width=True, hide_index=True, height=480)
    st.caption(f"{len(view):,} rows")
    st.download_button("⬇️ Download filtered data (CSV)", view.to_csv(index=False).encode("utf-8"),
                       "chennai_airport_filtered.csv", "text/csv")
    st.markdown('<div class="section-title">📊 Statistical Summary</div>', unsafe_allow_html=True)
    st.dataframe(fdf[["Total Passenger", "Total Freight", "Total Mail"]].describe().round(2), use_container_width=True)

elif page == "ℹ️ About":
    st.markdown('<div class="section-title">ℹ️ About the Application</div>', unsafe_allow_html=True)
    st.markdown(H("""
    <div class="info-card">
      <h2>Chennai Airport Traffic Analytics</h2>
      <p>An interactive analytical dashboard for domestic aviation traffic associated with Chennai International Airport (MAA),
      covering passengers, freight and mail across major Indian destinations.</p>
    </div>
    """), unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.markdown(H("""
        <div class="info-card">
          <h3>📌 Key Analytical Areas</h3>
          <ul>
            <li>Passenger traffic analysis (inbound / outbound)</li>
            <li>Destination, state and route analysis</li>
            <li>Interactive route maps</li>
            <li>Freight and mail volume analysis</li>
            <li>Monthly trends, growth and seasonality</li>
            <li>Destination comparison and auto-generated insights</li>
          </ul>
        </div>
        """), unsafe_allow_html=True)
    with b:
        st.markdown(H("""
        <div class="info-card">
          <h3>🛠️ Technology Stack</h3>
          <span class="chip">Python</span><span class="chip">Streamlit</span><span class="chip">Pandas</span>
          <span class="chip">NumPy</span><span class="chip">Plotly</span><span class="chip">Google Colab</span>
          <span class="chip">ngrok</span>
          <h3 style="margin-top:18px">🎛️ Features</h3>
          <span class="chip">Secure login</span><span class="chip">Multi-filters</span><span class="chip">Maps</span>
          <span class="chip">CSV export</span><span class="chip">Radar compare</span><span class="chip">Heatmaps</span>
        </div>
        """), unsafe_allow_html=True)
    st.markdown(H("""
    <div class="info-card">
      <h3>⚠️ Data Note</h3>
      <p>The dataset in this academic demonstration is simulated (seeded, with realistic seasonality) for 18 destinations
      from January to October 2025. It can be replaced with official AAI traffic data without changing the dashboard logic.</p>
    </div>
    """), unsafe_allow_html=True)

st.markdown(H("""
<div class="footer">Chennai Airport Traffic Analytics • MSc Data Science Mini Project<br>Interactive Analytics Application</div>
"""), unsafe_allow_html=True)
