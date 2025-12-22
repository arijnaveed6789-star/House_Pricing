"""
Housing Price Prediction - Ultra-Modern Web Application
Professional, minimalistic, fully responsive design with edge-to-edge layout.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="House Price Predictor | Pakistan",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-Modern Custom CSS - Edge-to-Edge, Professional
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Lato:wght@300;400;700&family=Inter:wght@300;400;500;600;700&family=Roboto:wght@400;500;600&family=Open+Sans:wght@400;500;600&display=swap');
    
    /* Reset and Base Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body {
        margin: 0;
        padding: 0;
        font-family: 'Inter', 'Poppins', sans-serif;
        background-color: #ffffff;
        color: #2c3e50;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none;}
    
    /* Remove Streamlit default padding and margins */
    .stApp {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
        margin-top: 0 !important;
    }
    
    /* Remove default block spacing */
    .element-container {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Force first element (navbar) to top */
    .block-container > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Ensure no gap for hero section */
    .hero-section {
        margin-top: 0 !important;
    }
    
    /* Remove spacing after columns */
    [data-testid="column"] {
        margin-bottom: 0 !important;
    }
    
    /* Aggressive removal of gaps */
    .block-container > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Main Content - Edge to Edge */
    .main-content {
        margin-top: 0;
        width: 100%;
        padding: 0;
    }
    
    /* Hero Section - Edge to Edge */
    .hero-section {
        width: 100%;
        background: linear-gradient(135deg, #1f3b4d 0%, #2c3e50 100%);
        padding: 3rem 2rem 4rem 2rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    .hero-cta-wrapper {
        margin-top: 3.5rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 50%, rgba(26, 188, 156, 0.1) 0%, transparent 50%);
    }
    
    .hero-title {
        font-size: 4.2rem;
        font-weight: 900;
        margin-bottom: 1rem;
        line-height: 1.2;
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
        color: #000000;
    }
    
    .hero-tagline {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.95;
        line-height: 1.6;
        margin: 1.5rem 0 0 0;
        position: relative;
        z-index: 1;
    }
    
    .hero-cta {
        display: inline-block;
        background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%) !important;
        color: white !important;
        padding: 1.2rem 3rem !important;
        border-radius: 50px !important;
        text-decoration: none !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
        position: relative;
        z-index: 1;
        border: none !important;
        cursor: pointer !important;
    }
    
    .hero-cta:hover {
        background: linear-gradient(135deg, #16a085 0%, #1abc9c 100%) !important;
        transform: translateY(0) !important;
        box-shadow: none !important;
        color: white !important;
    }
    
    /* Section Container - Full Width */
    .section {
        width: 100%;
        padding: 3rem 2rem;
        background: transparent;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    .section-alt {
        background: transparent;
    }
    
    /* Key Metrics Section with color */
    .metrics-section {
        background: linear-gradient(135deg, rgba(26, 188, 156, 0.05) 0%, rgba(16, 160, 133, 0.05) 100%);
    }
    
    /* Key Features Section with color */
    .features-section {
        background: linear-gradient(135deg, rgba(241, 196, 15, 0.05) 0%, rgba(243, 156, 18, 0.05) 100%);
    }
    
    .section-dark {
        background: linear-gradient(135deg, #1f3b4d 0%, #2c3e50 100%);
        color: white;
    }
    
    /* Section Header */
    .section-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f3b4d;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        padding-bottom: 1rem;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, #1abc9c 0%, #f1c40f 100%);
        border-radius: 2px;
    }
    
    .section-dark .section-header {
        color: white;
    }
    
    /* Premium Card */
    .premium-card {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(31, 59, 77, 0.08);
        border: 1px solid rgba(31, 59, 77, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2rem;
    }
    
    .premium-card:hover {
        background: #ffffff;
        box-shadow: 0 8px 30px rgba(31, 59, 77, 0.15);
        transform: translateY(-3px);
        border-color: rgba(26, 188, 156, 0.3);
    }
    
    /* Metric Cards */
    .metric-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(31, 59, 77, 0.08);
        border-left: 4px solid #1abc9c;
        border-top: 1px solid rgba(31, 59, 77, 0.1);
        border-right: 1px solid rgba(31, 59, 77, 0.1);
        border-bottom: 1px solid rgba(31, 59, 77, 0.1);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        background: #ffffff;
        box-shadow: 0 8px 30px rgba(26, 188, 156, 0.2);
        transform: translateY(-3px);
        border-left-width: 5px;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f3b4d;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #7f8c8d;
        font-weight: 500;
    }
    
    /* Prediction Card - More Prominent */
    .prediction-card {
        background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%) !important;
        padding: 4rem 3rem;
        border-radius: 16px;
        color: white !important;
        text-align: center;
        box-shadow: 0 15px 50px rgba(26, 188, 156, 0.5) !important;
        position: relative;
        overflow: hidden;
        animation: subtleGlow 3s ease-in-out infinite;
        border: 3px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    @keyframes subtleGlow {
        0%, 100% { box-shadow: 0 15px 50px rgba(26, 188, 156, 0.5); }
        50% { box-shadow: 0 20px 60px rgba(26, 188, 156, 0.7); }
    }
    
    .prediction-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .prediction-price {
        font-size: 4.5rem;
        font-weight: 800;
        margin: 1.5rem 0;
        position: relative;
        z-index: 1;
        letter-spacing: -2px;
    }
    
    .prediction-label {
        font-size: 1.1rem;
        font-weight: 500;
        opacity: 0.95;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Premium Button */
    .premium-button {
        background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        border: none;
        box-shadow: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        letter-spacing: 0.5px;
        cursor: pointer;
    }
    
    .premium-button:hover {
        transform: translateY(0);
        box-shadow: none;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 1rem 2.5rem !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #16a085 0%, #1abc9c 100%) !important;
        transform: translateY(0) !important;
        box-shadow: none !important;
        color: white !important;
    }
    
    /* Badge */
    .premium-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
        color: #1f3b4d;
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.875rem;
        margin: 0 0.5rem 0 0;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        box-shadow: 0 2px 10px rgba(241, 196, 15, 0.3);
        transition: all 0.3s ease;
        vertical-align: middle;
        white-space: nowrap;
    }
    
    .premium-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(241, 196, 15, 0.5);
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, rgba(26, 188, 156, 0.05) 0%, rgba(241, 196, 15, 0.05) 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 4px solid #1abc9c;
        margin: 1.5rem 0;
    }
    
    /* Input Styling */
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #ecf0f1;
        transition: all 0.3s ease;
    }
    
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #1abc9c;
        box-shadow: 0 0 0 3px rgba(26, 188, 156, 0.1);
    }
    
    /* Fade In Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 3rem;
        }
        .hero-tagline {
            font-size: 1.1rem;
        }
        .prediction-price {
            font-size: 2.5rem;
        }
        .section-header {
            font-size: 2rem;
        }
        .section {
            padding: 2rem 1rem;
        }
        .hero-section {
            padding: 2rem 1rem;
            margin-top: 70px;
        }
        .top-nav {
            padding: 1rem;
        }
    }
    
    /* Chart Styling */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
    
""", unsafe_allow_html=True)

# Load data and models
@st.cache_data
def load_data():
    """Load the housing dataset"""
    return pd.read_csv('Housing.csv')

@st.cache_resource
def load_model():
    """Load the trained model and preprocessing objects"""
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('label_encoders.pkl', 'rb') as f:
            label_encoders = pickle.load(f)
        with open('feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        return model, scaler, label_encoders, feature_names
    except FileNotFoundError:
        return None, None, None, None

# Load data
df = load_data()
model, scaler, label_encoders, feature_names = load_model()

# ============================================================================
# PAGE SELECTION (Using URL hash or session state)
# ============================================================================

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Use session state page
current_page = st.session_state.page

# ============================================================================
# NAVIGATION BAR
# ============================================================================

# Navigation Bar CSS
st.markdown("""
    <style>
    /* Navigation Bar Container */
    .navbar-wrapper {
        background: linear-gradient(135deg, #1a1f2e 0%, #2c3542 50%, #1a1f2e 100%);
        padding: 0 2rem 0.75rem 2rem;
        padding-top: 0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 0;
        margin-top: 0 !important;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 3rem;
        position: relative;
        top: 0;
    }
    
    /* Logo Styling - Brand Logo */
    .navbar-logo {
        font-size: 1.4rem;
        font-weight: 800;
        color: #000000;
        letter-spacing: 0.5px;
        white-space: nowrap;
        font-family: 'Inter', 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .navbar-logo:hover {
        transform: scale(1.05);
        color: #1a1a1a;
    }
    
    /* Logo Icon */
    .navbar-logo-icon {
        font-size: 1.8rem;
        display: inline-block;
        vertical-align: middle;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
        transition: transform 0.3s ease;
    }
    
    .navbar-logo:hover .navbar-logo-icon {
        transform: scale(1.1) rotate(5deg);
    }
    
    /* Logo Text */
    .navbar-logo-text {
        color: #000000;
        font-weight: 800;
        letter-spacing: 1px;
    }
    
    /* Navigation Buttons Container */
    .nav-buttons-wrapper {
        display: flex;
        align-items: center;
        gap: 2rem;
        flex-wrap: nowrap;
    }
    
    /* Navigation Button Styling */
    button[key^="nav_"] {
        background: transparent !important;
        color: rgba(255, 255, 255, 0.85) !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        padding: 0.5rem 1.2rem !important;
        border-radius: 6px !important;
        border: none !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        font-family: 'Inter', 'Roboto', sans-serif !important;
        margin: 0 !important;
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
        text-overflow: clip !important;
        overflow: visible !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
    }
    
    button[key^="nav_"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
    }
    
    button[key^="nav_"]:active,
    button[key^="nav_"]:focus {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        outline: none !important;
    }
    
    /* Active Page Button */
    button[key^="nav_"].nav-active {
        background: rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
    }
    
    /* Streamlit button wrapper styling */
    .nav-buttons-wrapper .stButton {
        margin: 0 !important;
        padding: 0 !important;
        width: auto !important;
        flex-shrink: 0;
    }
    
    /* Ensure buttons don't wrap - CRITICAL */
    .nav-buttons-wrapper .stButton button,
    button[key^="nav_"] {
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
        display: inline-block !important;
    }
    
    /* Force single line for all button text */
    button[key^="nav_"] * {
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
    }
    
    /* Laptop Screen Spacing (1024px - 1440px) - PRIMARY STYLING */
    @media (min-width: 1024px) and (max-width: 1440px) {
        .navbar-wrapper {
            padding: 0 2rem 0.7rem 2rem;
            gap: 2.5rem;
        }
        .navbar-logo {
            font-size: 1.3rem;
        }
        .navbar-logo-icon {
            font-size: 1.6rem;
        }
        .navbar-logo-text {
            letter-spacing: 0.8px;
        }
        .nav-buttons-wrapper {
            gap: 2rem;
        }
        button[key^="nav_"] {
            font-size: 0.9rem !important;
            padding: 0.5rem 1.1rem !important;
        }
    }
    
    /* Desktop/Large Laptop (1440px+) */
    @media (min-width: 1440px) {
        .navbar-wrapper {
            padding: 0 2.5rem 0.8rem 2.5rem;
            gap: 3rem;
        }
        .navbar-logo {
            font-size: 1.5rem;
    }
        .navbar-logo-icon {
            font-size: 1.9rem;
        }
        .navbar-logo-text {
            letter-spacing: 1.2px;
        }
        .nav-buttons-wrapper {
            gap: 2.5rem;
        }
    button[key^="nav_"] {
            font-size: 1rem !important;
            padding: 0.6rem 1.3rem !important;
        }
    }
    
    /* Tablet (768px - 1024px) */
    @media (max-width: 1023px) and (min-width: 768px) {
        .navbar-wrapper {
            padding: 0 1.5rem 0.6rem 1.5rem;
            gap: 2rem;
        }
        .navbar-logo {
            font-size: 1.2rem;
    }
        .navbar-logo-icon {
            font-size: 1.5rem;
    }
        .navbar-logo-text {
            letter-spacing: 0.6px;
        }
        .nav-buttons-wrapper {
            gap: 1.5rem;
    }
    button[key^="nav_"] {
        font-size: 0.85rem !important;
            padding: 0.45rem 1rem !important;
        }
    }
    
    /* Mobile */
    @media (max-width: 767px) {
        .navbar-wrapper {
            flex-direction: column;
            gap: 0.75rem;
            padding: 0 1rem 0.75rem 1rem;
        }
        .navbar-logo {
            font-size: 1.1rem;
        }
        .navbar-logo-icon {
            font-size: 1.4rem;
    }
        .navbar-logo-text {
            letter-spacing: 0.5px;
    }
        .nav-buttons-wrapper {
            gap: 0.75rem;
            flex-wrap: wrap;
            justify-content: center;
        }
        button[key^="nav_"] {
            font-size: 0.75rem !important;
            padding: 0.4rem 0.85rem !important;
        }
    }
    
    /* Override Streamlit column spacing */
    div:has(.navbar-logo) ~ div:has([data-testid="column"]) {
        background: linear-gradient(135deg, #1a1f2e 0%, #2c3542 50%, #1a1f2e 100%) !important;
        padding: 0 2rem 0.75rem 2rem !important;
        padding-top: 0 !important;
        margin: 0 !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 2rem !important;
    }
    
    /* Force navbar to top of page - Remove all top spacing */
    div:has(.navbar-logo),
    div:has(.navbar-logo) ~ div:has([data-testid="column"]),
    div:has(button[key^="nav_"]) {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove spacing from first element if it's navbar */
    .block-container > div:first-child:has(.navbar-logo),
    .block-container > div:first-child:has(button[key^="nav_"]),
    .block-container > div:first-child [data-testid="column"]:has(.navbar-logo) {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Ensure navbar container starts at top */
    div:has(.navbar-logo) {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Ensure columns don't wrap */
    div:has(.navbar-logo) ~ div:has([data-testid="column"]) [data-testid="column"] {
        flex-shrink: 0 !important;
        flex-grow: 0 !important;
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
    }
    
    /* Specific fix for Model Performance button - prevent wrapping */
    button[key="nav_Model Performance"] {
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
        display: inline-block !important;
        line-height: 1.2 !important;
    }
    
    /* Specific fix for Price Prediction button - prevent wrapping */
    button[key="nav_Price Prediction"] {
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
        display: inline-block !important;
        line-height: 1.2 !important;
    }
    
    /* Force column for Model Performance to be wider */
    div:has(button[key="nav_Model Performance"]) [data-testid="column"] {
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
        flex-basis: auto !important;
        flex-grow: 0 !important;
        flex-shrink: 0 !important;
    }
    
    /* Force column for Price Prediction to be wider */
    div:has(button[key="nav_Price Prediction"]) [data-testid="column"] {
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
        flex-basis: auto !important;
        flex-grow: 0 !important;
        flex-shrink: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Create navigation bar
nav_pages = ["Home", "Data Analysis", "Model Performance", "Price Prediction", "Conclusion"]

# Create navbar with logo and buttons in same row - wider columns for longer button names
navbar_cols = st.columns([1.5, 1, 1.4, 1.4, 1.2, 1], gap="medium")

# Logo column
with navbar_cols[0]:
    st.markdown("""
        <div class="navbar-logo" onclick="window.location.reload()" style="cursor: pointer;">
            <span class="navbar-logo-icon">🏠</span>
            <span class="navbar-logo-text">Dream Home</span>
        </div>
    """, unsafe_allow_html=True)

# Navigation buttons in remaining columns
for idx, page_name in enumerate(nav_pages):
    with navbar_cols[idx + 1]:
        if st.button(page_name, key=f"nav_{page_name}", use_container_width=False):
            st.session_state.page = page_name
            st.rerun()

# Additional CSS to ensure proper layout and prevent text wrapping
st.markdown("""
    <style>
    /* Force navbar row to stay horizontal */
    div:has(.navbar-logo) ~ div:has([data-testid="column"]) {
        flex-wrap: nowrap !important;
        overflow-x: visible !important;
    }
    
    /* Prevent button text wrapping - AGGRESSIVE */
    div:has(button[key^="nav_"]) button[key^="nav_"],
    button[key^="nav_"] {
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
        text-overflow: clip !important;
        display: inline-block !important;
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
    }
    
    /* Force all button content to single line */
    button[key^="nav_"] *,
    button[key^="nav_"] span,
    button[key^="nav_"] div,
    button[key^="nav_"] p {
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
        display: inline !important;
    }
    
    /* Button wrapper - prevent width constraints */
    div:has(button[key^="nav_"]) .stButton {
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
        flex-shrink: 0 !important;
    }
    
    /* Column constraints - allow content-based width */
    div:has(button[key^="nav_"]) [data-testid="column"] {
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
        flex-basis: auto !important;
        flex-grow: 0 !important;
            flex-shrink: 0 !important;
        }
    
    /* CRITICAL: Remove all width constraints from button columns */
    div:has(button[key^="nav_"]) [data-testid="column"],
    div:has(button[key^="nav_"]) [data-testid="column"] > div {
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
        flex-basis: auto !important;
        flex-grow: 0 !important;
            flex-shrink: 0 !important;
        }
    
    /* Force Model Performance button to stay on one line */
    button[key="nav_Model Performance"],
    button[key="nav_Model Performance"] * {
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
        display: inline-block !important;
        width: auto !important;
        min-width: max-content !important;
        max-width: none !important;
        }
    
    /* Force Price Prediction button to stay on one line */
    button[key="nav_Price Prediction"],
    button[key="nav_Price Prediction"] * {
            white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
        display: inline-block !important;
        width: auto !important;
            min-width: max-content !important;
        max-width: none !important;
    }
    
    /* Laptop-specific spacing adjustments */
    @media (min-width: 1024px) and (max-width: 1440px) {
        div:has(.navbar-logo) ~ div:has([data-testid="column"]) {
            gap: 2rem !important;
        }
        div:has(button[key^="nav_"]) [data-testid="column"] {
            margin-right: 0 !important;
            padding: 0 0.5rem !important;
        }
        
        /* Ensure Model Performance button has enough space on laptop */
        button[key="nav_Model Performance"] {
            font-size: 0.9rem !important;
            padding: 0.5rem 1.1rem !important;
            white-space: nowrap !important;
        }
        
        /* Ensure Price Prediction button has enough space on laptop */
        button[key="nav_Price Prediction"] {
            font-size: 0.9rem !important;
            padding: 0.5rem 1.1rem !important;
            white-space: nowrap !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript to handle active state and force single-line buttons
st.markdown(f"""
    <script>
    (function() {{
        function updateNavButtons() {{
            const currentPage = '{current_page}';
            const navButtons = document.querySelectorAll('button[key^="nav_"]');
            
            navButtons.forEach(btn => {{
                const buttonText = btn.textContent.trim();
                btn.classList.remove('nav-active');
                
                // Force single line - AGGRESSIVE
                btn.style.whiteSpace = 'nowrap';
                btn.style.wordBreak = 'keep-all';
                btn.style.overflowWrap = 'normal';
                btn.style.width = 'auto';
                btn.style.minWidth = 'max-content';
                btn.style.maxWidth = 'none';
                btn.style.display = 'inline-block';
                btn.style.lineHeight = '1.2';
                
                // Force all child elements to single line
                const children = btn.querySelectorAll('*');
                children.forEach(child => {{
                    child.style.whiteSpace = 'nowrap';
                    child.style.wordBreak = 'keep-all';
                    child.style.overflowWrap = 'normal';
                    child.style.display = 'inline';
                }});
                
                // Special handling for Model Performance and Price Prediction
                if (buttonText === 'Model Performance' || buttonText === 'Price Prediction') {{
                    btn.style.fontSize = '0.9rem';
                    btn.style.padding = '0.5rem 1.1rem';
                    btn.style.width = 'auto';
                    btn.style.minWidth = 'max-content';
                    
                    // Force parent column to not constrain
                const column = btn.closest('[data-testid="column"]');
                if (column) {{
                        column.style.width = 'auto';
                        column.style.minWidth = 'max-content';
                        column.style.maxWidth = 'none';
                        column.style.flexBasis = 'auto';
                        column.style.flexGrow = '0';
                        column.style.flexShrink = '0';
                    }}
                }}
                
                if (buttonText === currentPage) {{
                    btn.classList.add('nav-active');
                }}
            }});
        }}
        
        // Run on load
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', updateNavButtons);
        }} else {{
            updateNavButtons();
        }}
        
        // Update after Streamlit reruns
        const observer = new MutationObserver(function(mutations) {{
            updateNavButtons();
        }});
        
        observer.observe(document.body, {{
            childList: true,
            subtree: true
        }});
    }})();
    </script>
""", unsafe_allow_html=True)

# ============================================================================
# HOME PAGE
# ============================================================================

if current_page == "Home":
    # Hero Section - Title and tagline
    st.markdown("""
        <div class="hero-section fade-in">
            <h1 class="hero-title">House Price Predictor</h1>
            <p class="hero-tagline">
            Predict your dream home's price with elegance, accuracy, and style.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics Section - Edge to Edge
    st.markdown("""
        <div class="section metrics-section fade-in">
            <h2 class="section-header" style="color: #000000;">Key Metrics</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card fade-in">
                <div class="metric-value">{len(df):,}</div>
                <div class="metric-label">Properties Analyzed</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card fade-in">
                <div class="metric-value">{len(df.columns)}</div>
                <div class="metric-label">Features Analyzed</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_price = df['price'].mean()
        st.markdown(f"""
            <div class="metric-card fade-in">
                <div class="metric-value">PKR {avg_price/1e6:.1f}M</div>
                <div class="metric-label">Average Price</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        price_range = df['price'].max() - df['price'].min()
        st.markdown(f"""
            <div class="metric-card fade-in">
                <div class="metric-value">PKR {price_range/1e6:.1f}M</div>
                <div class="metric-label">Price Range</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
        <div class="section features-section fade-in">
            <h2 class="section-header" style="color: #000000;">Key Features</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="premium-card fade-in">
                <h3 style='color: #1f3b4d; font-size: 1.4rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem;'>
                Accurate Predictions
                </h3>
                <p style='color: #7f8c8d; line-height: 1.8; margin: 0;'>
                Advanced machine learning models provide highly accurate price predictions based on comprehensive data analysis.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="premium-card fade-in">
                <h3 style='color: #1f3b4d; font-size: 1.4rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem;'>
                Data Insights
                </h3>
                <p style='color: #7f8c8d; line-height: 1.8; margin: 0;'>
                Explore comprehensive data visualizations and understand market trends through interactive charts.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="premium-card fade-in">
                <h3 style='color: #1f3b4d; font-size: 1.4rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem;'>
                Instant Results
                </h3>
                <p style='color: #7f8c8d; line-height: 1.8; margin: 0;'>
                Get real-time price predictions in seconds. No waiting, no delays - just instant accurate results.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="premium-card fade-in">
                <h3 style='color: #1f3b4d; font-size: 1.4rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem;'>
                Comprehensive Analysis
                </h3>
                <p style='color: #7f8c8d; line-height: 1.8; margin: 0;'>
                Analyze 12+ property features including location, size, amenities, and furnishing status.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="premium-card fade-in">
                <h3 style='color: #1f3b4d; font-size: 1.4rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem;'>
                AI-Powered
                </h3>
                <p style='color: #7f8c8d; line-height: 1.8; margin: 0;'>
                Leveraging state-of-the-art machine learning algorithms for optimal accuracy.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="premium-card fade-in">
                <h3 style='color: #1f3b4d; font-size: 1.4rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem;'>
                User-Friendly
                </h3>
                <p style='color: #7f8c8d; line-height: 1.8; margin: 0;'>
                Beautiful, intuitive interface designed for ease of use. Professional and trustworthy.
                </p>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# DATA ANALYSIS PAGE
# ============================================================================

elif current_page == "Data Analysis":
    st.markdown("""
        <div class="section fade-in">
            <h2 class="section-header">Data Analysis</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Overview Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{df.shape[0]:,}")
    col2.metric("Features", len(df.columns))
    col3.metric("Numerical", len(df.select_dtypes(include=[np.number]).columns))
    col4.metric("Categorical", len(df.select_dtypes(include=['object']).columns))
    
    # Summary Statistics
    st.markdown("""
        <div class="section section-alt fade-in">
            <h2 class="section-header">Summary Statistics</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="premium-card fade-in">
    """, unsafe_allow_html=True)
    st.dataframe(df.describe().style.background_gradient(cmap='viridis'), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Price Distribution
    st.markdown("""
        <div class="section fade-in">
            <h2 class="section-header">Price Distribution</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="premium-card fade-in">
    """, unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(df['price'], bins=50, edgecolor='white', alpha=0.85, color='#1abc9c', linewidth=1.5)
    ax.axvline(df['price'].mean(), color='#e67e22', linestyle='--', linewidth=3, 
               label=f'Mean: PKR {df["price"].mean():,.0f}')
    ax.axvline(df['price'].median(), color='#f1c40f', linestyle='--', linewidth=3, 
               label=f'Median: PKR {df["price"].median():,.0f}')
    ax.set_xlabel('Price (PKR)', fontsize=13, fontweight=600)
    ax.set_ylabel('Frequency', fontsize=13, fontweight=600)
    ax.set_title('Distribution of House Prices', fontsize=15, fontweight=700, pad=20)
    ax.legend(fontsize=11, frameon=True, fancybox=True, shadow=True)
    ax.grid(alpha=0.2, linestyle='--')
    ax.set_facecolor('#f5f5f5')
    st.pyplot(fig)
    plt.close()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Correlation Heatmap
    st.markdown("""
        <div class="section section-alt fade-in">
            <h2 class="section-header">Feature Correlations</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="premium-card fade-in">
    """, unsafe_allow_html=True)
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numerical_cols].corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=2, cbar_kws={"shrink": 0.8}, fmt='.2f', 
                ax=ax, vmin=-1, vmax=1, annot_kws={'size': 10, 'weight': 'bold'})
    ax.set_title('Correlation Matrix Heatmap', fontsize=16, fontweight=700, pad=20)
    st.pyplot(fig)
    plt.close()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Interactive Feature Relationships
    st.markdown("""
        <div class="section fade-in">
            <h2 class="section-header">Feature Relationships</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="premium-card fade-in">
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        feature1 = st.selectbox("X-axis Feature", numerical_cols, key='x_feature')
    with col2:
        feature2 = st.selectbox("Y-axis Feature", numerical_cols, key='y_feature', index=0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    scatter = ax.scatter(df[feature1], df[feature2], c=df['price'], cmap='viridis', 
                        alpha=0.7, s=60, edgecolors='white', linewidth=0.5)
    ax.set_xlabel(feature1, fontsize=13, fontweight=600)
    ax.set_ylabel(feature2, fontsize=13, fontweight=600)
    ax.set_title(f'{feature2} vs {feature1} (Color = Price)', fontsize=15, fontweight=700, pad=20)
    plt.colorbar(scatter, ax=ax, label='Price (PKR)')
    ax.grid(alpha=0.2, linestyle='--')
    ax.set_facecolor('#f5f5f5')
    st.pyplot(fig)
    plt.close()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Categorical Analysis
    st.markdown("""
        <div class="section section-alt fade-in">
            <h2 class="section-header">Categorical Feature Analysis</h2>
        </div>
    """, unsafe_allow_html=True)
    categorical_cols = df.select_dtypes(include=['object']).columns
    selected_cat = st.selectbox("Select Categorical Feature", categorical_cols, key='cat_feature')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="premium-card fade-in">
        """, unsafe_allow_html=True)
        value_counts = df[selected_cat].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#1abc9c', '#2c3e50', '#f1c40f', '#e67e22', '#3498db']
        bars = ax.bar(value_counts.index, value_counts.values, 
                     color=colors[:len(value_counts)], edgecolor='white', linewidth=2)
        ax.set_title(f'{selected_cat} Distribution', fontsize=14, fontweight=700, pad=15)
        ax.set_xlabel(selected_cat, fontsize=12, fontweight=600)
        ax.set_ylabel('Count', fontsize=12, fontweight=600)
        plt.xticks(rotation=45)
        ax.grid(axis='y', alpha=0.2, linestyle='--')
        ax.set_facecolor('#f5f5f5')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontweight=700, fontsize=11)
        st.pyplot(fig)
        plt.close()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="premium-card fade-in">
        """, unsafe_allow_html=True)
        price_by_cat = df.groupby(selected_cat)['price'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#1abc9c', '#2c3e50', '#f1c40f', '#e67e22', '#3498db']
        bars = ax.bar(price_by_cat.index, price_by_cat.values, 
                     color=colors[:len(price_by_cat)], edgecolor='white', linewidth=2)
        ax.set_title(f'Average Price by {selected_cat}', fontsize=14, fontweight=700, pad=15)
        ax.set_xlabel(selected_cat, fontsize=12, fontweight=600)
        ax.set_ylabel('Average Price (PKR)', fontsize=12, fontweight=600)
        plt.xticks(rotation=45)
        ax.grid(axis='y', alpha=0.2, linestyle='--')
        ax.set_facecolor('#f5f5f5')
        for i, (bar, v) in enumerate(zip(bars, price_by_cat.values)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'PKR {v/1e6:.1f}M', ha='center', va='bottom', fontweight=700, fontsize=10)
        st.pyplot(fig)
        plt.close()
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MODEL PERFORMANCE PAGE
# ============================================================================

elif current_page == "Model Performance":
    st.markdown("""
        <div class="section fade-in">
            <h2 class="section-header">Model Performance</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if model is None:
        st.error("Model files not found. Please run 'housing_analysis.py' first to train the models.")
        st.info("To train the models, run: `python housing_analysis.py`")
    else:
        try:
            results_df = pd.read_csv('model_results.csv')
            
            st.markdown("""
                <div class="section section-alt fade-in">
                    <h2 class="section-header">Model Comparison</h2>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("""
                <div class="premium-card fade-in">
            """, unsafe_allow_html=True)
            
            styled_df = results_df.style.format({
                'Train_RMSE': '{:,.2f}',
                'Test_RMSE': '{:,.2f}',
                'Train_R2': '{:.4f}',
                'Test_R2': '{:.4f}',
                'Train_MAE': '{:,.2f}',
                'Test_MAE': '{:,.2f}'
            }).background_gradient(subset=['Test_R2'], cmap='Greens')
            
            st.dataframe(styled_df, use_container_width=True, height=200)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Performance Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div class="section fade-in">
                        <h3 style='color: #2c3e50; font-size: 1.3rem; font-weight: 700; margin-bottom: 1.5rem; text-align: center;'>
                        R² Score Comparison
                        </h3>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="premium-card fade-in">
                """, unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(10, 6))
                x = np.arange(len(results_df))
                width = 0.35
                bars1 = ax.bar(x - width/2, results_df['Train_R2'], width, label='Train R²', 
                              color='#1abc9c', edgecolor='white', linewidth=2)
                bars2 = ax.bar(x + width/2, results_df['Test_R2'], width, label='Test R²', 
                              color='#2c3e50', edgecolor='white', linewidth=2)
                ax.set_xlabel('Models', fontsize=12, fontweight=600)
                ax.set_ylabel('R² Score', fontsize=12, fontweight=600)
                ax.set_title('R² Score Comparison', fontsize=14, fontweight=700, pad=15)
                ax.set_xticks(x)
                ax.set_xticklabels(results_df['Model'], rotation=45, ha='right')
                ax.legend(fontsize=11, frameon=True, fancybox=True, shadow=True)
                ax.grid(axis='y', alpha=0.2, linestyle='--')
                ax.set_facecolor('#f5f5f5')
                for bars in [bars1, bars2]:
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{height:.3f}', ha='center', va='bottom', fontsize=9, fontweight=700)
                st.pyplot(fig)
                plt.close()
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div class="section fade-in">
                        <h3 style='color: #2c3e50; font-size: 1.3rem; font-weight: 700; margin-bottom: 1.5rem; text-align: center;'>
                        RMSE Comparison
                        </h3>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="premium-card fade-in">
                """, unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(10, 6))
                x = np.arange(len(results_df))
                width = 0.35
                bars1 = ax.bar(x - width/2, results_df['Train_RMSE'], width, label='Train RMSE', 
                              color='#f1c40f', edgecolor='white', linewidth=2)
                bars2 = ax.bar(x + width/2, results_df['Test_RMSE'], width, label='Test RMSE', 
                              color='#e67e22', edgecolor='white', linewidth=2)
                ax.set_xlabel('Models', fontsize=12, fontweight=600)
                ax.set_ylabel('RMSE', fontsize=12, fontweight=600)
                ax.set_title('RMSE Comparison', fontsize=14, fontweight=700, pad=15)
                ax.set_xticks(x)
                ax.set_xticklabels(results_df['Model'], rotation=45, ha='right')
                ax.legend(fontsize=11, frameon=True, fancybox=True, shadow=True)
                ax.grid(axis='y', alpha=0.2, linestyle='--')
                ax.set_facecolor('#f5f5f5')
                for bars in [bars1, bars2]:
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{height/1e6:.2f}M', ha='center', va='bottom', fontsize=9, fontweight=700)
                st.pyplot(fig)
                plt.close()
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Best Model
            best_model_idx = results_df['Test_R2'].idxmax()
            best_model_name = results_df.loc[best_model_idx, 'Model']
            
            st.markdown("""
                <div class="section section-alt fade-in">
                    <h2 class="section-header">Best Performing Model</h2>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div class="info-box fade-in">
                    <h3 style='color: #2c3e50; margin-top: 0; font-size: 1.5rem; font-weight: 700;'>
                    {best_model_name}
                    </h3>
                    <p style='color: #7f8c8d; font-size: 1rem; line-height: 1.8; margin-bottom: 0;'>
                    Selected as the best model based on highest Test R² score, indicating superior predictive performance.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Test R² Score", f"{results_df.loc[best_model_idx, 'Test_R2']:.4f}", 
                       delta=f"{results_df.loc[best_model_idx, 'Test_R2']*100:.2f}% accuracy")
            col2.metric("Test RMSE", f"PKR {results_df.loc[best_model_idx, 'Test_RMSE']:,.2f}")
            col3.metric("Test MAE", f"PKR {results_df.loc[best_model_idx, 'Test_MAE']:,.2f}")
            col4.metric("Model Type", best_model_name.split()[0])

        except FileNotFoundError:
            st.warning("Model results file not found. Please run 'housing_analysis.py' to generate results.")

# ============================================================================
# PRICE PREDICTION PAGE
# ============================================================================

elif current_page == "Price Prediction":
    st.markdown("""
        <div class="section section-dark fade-in">
            <h2 class="section-header" style="color: white;">Price Prediction</h2>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; text-align: center; margin-top: 1rem;'>
            Enter your property details below and receive an accurate price prediction powered by advanced machine learning.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if model is None:
        st.error("Model not found. Please run 'housing_analysis.py' first to train the model.")
        st.info("To train the model, run: `python housing_analysis.py`")
    else:
        # Input form
        st.markdown("""
            <div class="section fade-in">
                <h2 class="section-header">Property Details</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("prediction_form", clear_on_submit=False):
            st.markdown("""
                <div class="premium-card fade-in">
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                    <h3 style='color: #2c3e50; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;'>
                    Basic Information
                    </h3>
                """, unsafe_allow_html=True)
                area = st.number_input("Area (sq ft)", min_value=0, value=6000, step=100)
                bedrooms = st.number_input("Number of Bedrooms", min_value=0, max_value=10, value=3, step=1)
                bathrooms = st.number_input("Number of Bathrooms", min_value=0, max_value=10, value=2, step=1)
                stories = st.number_input("Number of Stories", min_value=0, max_value=10, value=2, step=1)
                parking = st.number_input("Parking Spaces", min_value=0, max_value=5, value=2, step=1)
            
            with col2:
                st.markdown("""
                    <h3 style='color: #2c3e50; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;'>
                    Location & Area
                    </h3>
                """, unsafe_allow_html=True)
                mainroad = st.selectbox("Main Road Access", ["yes", "no"], index=0)
                prefarea = st.selectbox("Preferred Area", ["yes", "no"], index=0)
                furnishingstatus = st.selectbox("Furnishing Status", 
                                               ["furnished", "semi-furnished", "unfurnished"], 
                                               index=0)
            
            with col3:
                st.markdown("""
                    <h3 style='color: #2c3e50; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;'>
                    Amenities
                    </h3>
                """, unsafe_allow_html=True)
                guestroom = st.selectbox("Guest Room", ["yes", "no"], index=0)
                basement = st.selectbox("Basement", ["yes", "no"], index=0)
                hotwaterheating = st.selectbox("Hot Water Heating", ["yes", "no"], index=1)
                airconditioning = st.selectbox("Air Conditioning", ["yes", "no"], index=0)
            
            st.markdown("</div>", unsafe_allow_html=True)
            submit_button = st.form_submit_button("Predict Price", use_container_width=True)
        
        if submit_button:
            try:
                with st.spinner('Analyzing property features and calculating price...'):
                    # Prepare input data
                    input_data = {
                        'area': area,
                        'bedrooms': bedrooms,
                        'bathrooms': bathrooms,
                        'stories': stories,
                        'mainroad': mainroad,
                        'guestroom': guestroom,
                        'basement': basement,
                        'hotwaterheating': hotwaterheating,
                        'airconditioning': airconditioning,
                        'parking': parking,
                        'prefarea': prefarea,
                        'furnishingstatus': furnishingstatus
                    }
                    
                    # Create DataFrame
                    input_df = pd.DataFrame([input_data])
                    
                    # Encode categorical variables
                    for col in ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']:
                        if col in label_encoders:
                            input_df[col] = label_encoders[col].transform([input_data[col]])[0]
                    
                    # One-hot encode furnishing status
                    furnishing_dummies = pd.get_dummies(pd.DataFrame([{'furnishingstatus': furnishingstatus}]), 
                                                       columns=['furnishingstatus'], 
                                                       prefix='furnishing', 
                                                       drop_first=True)
                    input_df = pd.concat([input_df.drop('furnishingstatus', axis=1), furnishing_dummies], axis=1)
                    
                    # Ensure all feature columns are present
                    for col in feature_names:
                        if col not in input_df.columns:
                            input_df[col] = 0
                    
                    # Reorder columns to match training data
                    input_df = input_df[feature_names]
                    
                    # Scale features
                    input_scaled = scaler.transform(input_df)
                    
                    # Make prediction
                    prediction = model.predict(input_scaled)[0]
                    
                    # Calculate prediction range
                    lower_bound = prediction * 0.9
                    upper_bound = prediction * 1.1
                
                # Display result
                st.markdown("""
                    <div class="section section-alt fade-in">
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="prediction-card fade-in">
                        <p class="prediction-label">Predicted House Price</p>
                        <h1 class="prediction-price">PKR {prediction:,.0f}</h1>
                        <p style='color: rgba(255,255,255,0.9); font-size: 1rem; margin-top: 1rem; position: relative; z-index: 1;'>
                        Estimated Range: PKR {lower_bound:,.0f} - PKR {upper_bound:,.0f}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Property Summary
                st.markdown("""
                    <div class="section fade-in">
                        <h2 class="section-header">Property Summary</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Area", f"{area:,} sq ft")
                col2.metric("Bedrooms", bedrooms)
                col3.metric("Bathrooms", bathrooms)
                col4.metric("Stories", stories)
                
                # Feature highlights
                st.markdown("### Key Features")
                feature_list = []
                if mainroad == "yes":
                    feature_list.append("Main Road Access")
                if prefarea == "yes":
                    feature_list.append("Preferred Area")
                if guestroom == "yes":
                    feature_list.append("Guest Room")
                if basement == "yes":
                    feature_list.append("Basement")
                if airconditioning == "yes":
                    feature_list.append("Air Conditioning")
                if hotwaterheating == "yes":
                    feature_list.append("Hot Water Heating")
                if parking > 0:
                    feature_list.append(f"{parking} Parking Space(s)")
                feature_list.append(furnishingstatus.title())
                
                # Create all badges in a single markdown call for horizontal display
                badges_html = ''.join([f'<span class="premium-badge">{feature}</span>' for feature in feature_list])
                st.markdown(f"""
                    <div style='display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1.5rem 0; align-items: center;'>
                        {badges_html}
                    </div>
                """, unsafe_allow_html=True)
                
                # Comparison with average
                avg_price = df['price'].mean()
                price_diff = prediction - avg_price
                price_diff_pct = (price_diff / avg_price) * 100
                
                st.markdown("### Market Comparison")
                st.markdown("""
                    <div class="premium-card fade-in">
                """, unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Market Average", f"PKR {avg_price:,.0f}")
                with col2:
                    if price_diff > 0:
                        st.metric("Your Property", f"PKR {prediction:,.0f}", 
                                delta=f"+{price_diff_pct:.1f}% above average", delta_color="normal")
                    else:
                        st.metric("Your Property", f"PKR {prediction:,.0f}", 
                                delta=f"{price_diff_pct:.1f}% below average", delta_color="inverse")
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")
                st.info("Please ensure all fields are filled correctly and try again.")

# ============================================================================
# CONCLUSION PAGE
# ============================================================================

elif current_page == "Conclusion":
    st.markdown("""
        <div class="section fade-in">
            <h2 class="section-header">Project Conclusion</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="section section-alt fade-in">
            <h2 class="section-header">Key Findings</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box fade-in">
            <ul style='font-size: 1.05rem; line-height: 2; color: #7f8c8d; margin: 0; padding-left: 1.5rem;'>
                <li style='margin-bottom: 0.8rem;'><strong style='color: #2c3e50;'>Price Distribution:</strong> The dataset shows a right-skewed distribution of house prices, with most properties concentrated in the mid-range price segment.</li>
                <li style='margin-bottom: 0.8rem;'><strong style='color: #2c3e50;'>Feature Correlations:</strong> Area has the strongest positive correlation with price, followed by number of bedrooms, bathrooms, and parking spaces.</li>
                <li style='margin-bottom: 0.8rem;'><strong style='color: #2c3e50;'>Location Impact:</strong> Properties with main road access and in preferred areas command significantly higher prices.</li>
                <li style='margin-bottom: 0.8rem;'><strong style='color: #2c3e50;'>Furnishing Status:</strong> Fully furnished properties are priced higher than semi-furnished or unfurnished ones.</li>
                <li style='margin-bottom: 0;'><strong style='color: #2c3e50;'>Amenities Value:</strong> Air conditioning and parking spaces are highly valued features that positively impact house prices.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="section fade-in">
            <h2 class="section-header">Model Effectiveness</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box fade-in">
            <p style='font-size: 1.05rem; line-height: 1.8; color: #7f8c8d; margin: 0;'>
            The machine learning models successfully learned patterns from the housing data, with Random Forest Regressor typically achieving the best performance. 
            The models correctly identify area, location, and amenities as key price determinants, and show reasonable performance on test data, suggesting 
            they can generalize to new properties. The deployed model enables instant price predictions based on user input, making it practical for real-world applications.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="section section-alt fade-in">
            <h2 class="section-header">Future Improvements</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box fade-in">
            <ul style='font-size: 1.05rem; line-height: 2; color: #7f8c8d; margin: 0; padding-left: 1.5rem;'>
                <li style='margin-bottom: 0.8rem;'><strong style='color: #2c3e50;'>Enhanced Features:</strong> Add property age, condition, nearby amenities, and location coordinates for geographic analysis</li>
                <li style='margin-bottom: 0.8rem;'><strong style='color: #2c3e50;'>Advanced Models:</strong> Experiment with XGBoost, LightGBM, and deep learning models for complex pattern recognition</li>
                <li style='margin-bottom: 0.8rem;'><strong style='color: #2c3e50;'>Data Enhancement:</strong> Collect more data points for better model training and include temporal market trends</li>
                <li style='margin-bottom: 0.8rem;'><strong style='color: #2c3e50;'>Model Interpretability:</strong> Add SHAP values and feature importance visualizations for better model explanation</li>
                <li style='margin-bottom: 0;'><strong style='color: #2c3e50;'>Application Features:</strong> Property comparison functionality, historical price trends, and export capabilities</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="section section-dark fade-in">
            <h2 class="section-header" style="color: white;">Thank You</h2>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; text-align: center; margin-top: 1rem; line-height: 1.8;'>
            This project demonstrates the application of data science techniques to solve real-world problems in the Pakistani real estate market.
            </p>
        </div>
    """, unsafe_allow_html=True)
