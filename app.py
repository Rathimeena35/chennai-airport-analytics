
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
