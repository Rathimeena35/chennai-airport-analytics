
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
