import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Nexus Investment Pro", layout="wide", initial_sidebar_state="expanded")

# --- HIGH-TECH CUSTOM CSS ---
# This injects a dark theme with neon accents and smooth transitions
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .css-1d391kg, .css-1lcbmhc {
        background-color: #161b22;
    }
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        background-color: transparent;
        color: #58a6ff;
        border: 1px solid #58a6ff;
        border-radius: 5px;
        transition: all 0.3s ease;
        box-shadow: 0 0 5px #58a6ff20;
    }
    .stButton>button:hover {
        background-color: #58a6ff;
        color: #0d1117;
        box-shadow: 0 0 15px #58a6ff;
        transform: scale(1.02);
    }
    .metric-container {
        background: #161b22;
        border-left: 4px solid #3fb950;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def generate_chart(df, title):
    """Generates a high-tech Plotly chart with hover interactions."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Total Invested'], 
                             mode='lines', name='Total Invested', 
                             line=dict(color='#8b949e', width=3, dash='dash')))
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Portfolio Value'], 
                             mode='lines+markers', name='Portfolio Value',
                             line=dict(color='#58a6ff', width=4),
                             marker=dict(size=6, color='#58a6ff', line=dict(width=2, color='white'))))
    
    fig.update_layout(
        title=title,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c9d1d9'),
        xaxis=dict(showgrid=True, gridcolor='#30363d'),
        yaxis=dict(showgrid=True, gridcolor='#30363d', tickprefix="₹"),
        hovermode="x unified"
    )
    return fig

# --- MAIN APP UI ---
st.title("⚡ Nexus Investment Pro Dashboard")
st.markdown("Advanced analytical suite for forecasting asset growth across multiple financial instruments.")

# Sidebar Navigation
st.sidebar.header("Navigation System")
asset_class = st.sidebar.radio(
    "Select Asset Class",
    ("Stocks (Equity)", "Bonds (Debt)", "Mutual Funds (SIP)", "Real Estate", 
     "Cash Equivalents", "Government Schemes (India)", "Alternative Investments")
)

st.sidebar.markdown("---")
st.sidebar.info("Adjust the sliders in the main panel to run real-time simulations.")

# --- CALCULATORS ---

if asset_class == "Stocks (Equity)":
    st.header("📈 Equity Forecasting Engine")
    st.markdown("High-risk, high-return projections based on capital appreciation and dividends.")
    
    col1, col2, col3 = st.columns(3)
    initial_inv = col1.number_input("Initial Investment (₹)", value=100000, step=10000)
    monthly_add = col2.number_input("Monthly Contribution (₹)", value=5000, step=1000)
    years = col3.slider("Investment Horizon (Years)", 1, 40, 10)
    
    cagr = st.slider("Expected Annual Return (CAGR %)", 1.0, 30.0, 12.0)
    
    # Calculation
    data = []
    current_val = initial_inv
    total_inv = initial_inv
    for year in range(1, years + 1):
        for month in range(12):
            current_val = current_val * (1 + (cagr/100)/12) + monthly_add
            total_inv += monthly_add
        data.append([year, total_inv, current_val])
    
    df = pd.DataFrame(data, columns=['Year', 'Total Invested', 'Portfolio Value'])
    
    st.plotly_chart(generate_chart(df, "Projected Stock Portfolio Value"), use_container_width=True)
    st.success(f"Estimated Final Value: **₹{current_val:,.2f}**")

elif asset_class == "Bonds (Debt)":
    st.header("🏛️ Fixed-Income (Bonds) Simulator")
    st.markdown("Predictable, lower-risk returns through government or corporate debt.")
    
    col1, col2 = st.columns(2)
    face_value = col1.number_input("Total Bond Investment (₹)", value=500000, step=50000)
    coupon_rate = col2.slider("Annual Coupon Rate (%)", 1.0, 15.0, 7.5)
    years = st.slider("Holding Period (Years)", 1, 30, 10)
    
    data = []
    for year in range(1, years + 1):
        # Simple interest for standard bonds paying out annually
        annual_payout = face_value * (coupon_rate / 100)
        cumulative_payout = annual_payout * year
        data.append([year, face_value, face_value + cumulative_payout])
        
    df = pd.DataFrame(data, columns=['Year', 'Total Invested', 'Portfolio Value'])
    st.plotly_chart(generate_chart(df, "Bond Value + Cumulative Interest"), use_container_width=True)
    st.success(f"Total Interest Earned: **₹{(face_value * (coupon_rate / 100) * years):,.2f}**")

elif asset_class == "Mutual Funds (SIP)":
    st.header("📊 Mutual Fund SIP Calculator")
    st.markdown("Pooled professional investments. Assumes monthly compounding.")
    
    col1, col2 = st.columns(2)
    sip_amount = col1.number_input("Monthly SIP Amount (₹)", value=10000, step=1000)
    years = col2.slider("Investment Horizon (Years)", 1, 35, 15)
    expected_return = st.slider("Expected Return (%)", 5.0, 25.0, 12.0)
    
    data = []
    total_inv = 0
    future_value = 0
    monthly_rate = (expected_return / 100) / 12
    
    for year in range(1, years + 1):
        months = year * 12
        # SIP Formula: P × ({[1 + i]^n - 1} / i) × (1 + i)
        future_value = sip_amount * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
        total_inv = sip_amount * months
        data.append([year, total_inv, future_value])
        
    df = pd.DataFrame(data, columns=['Year', 'Total Invested', 'Portfolio Value'])
    st.plotly_chart(generate_chart(df, "SIP Wealth Accumulation"), use_container_width=True)
    st.success(f"Estimated Final Value: **₹{future_value:,.2f}**")

elif asset_class == "Government Schemes (India)":
    st.header("🇮🇳 Government Schemes (PPF/NPS/SCSS)")
    st.markdown("Tax-advantaged, highly secure retirement and savings vehicles.")
    
    scheme = st.selectbox("Select Scheme", ["Public Provident Fund (PPF)", "National Pension System (NPS)", "Senior Citizen Savings Scheme (SCSS)"])
    
    if scheme == "Public Provident Fund (PPF)":
        yearly_inv = st.number_input("Yearly Contribution (₹ max 1.5L)", min_value=500, max_value=150000, value=150000)
        rate = 7.1 # Fixed PPF rate approx
        st.info(f"Current Assumed PPF Rate: {rate}% | Lock-in: 15 Years")
        years = st.slider("Years", 15, 30, 15, step=5) # PPF extends in blocks of 5
        
        data = []
        current_val = 0
        for year in range(1, years + 1):
            current_val = (current_val + yearly_inv) * (1 + rate/100)
            data.append([year, yearly_inv * year, current_val])
            
        df = pd.DataFrame(data, columns=['Year', 'Total Invested', 'Portfolio Value'])
        st.plotly_chart(generate_chart(df, "PPF Growth Trajectory"), use_container_width=True)
        
    elif scheme == "National Pension System (NPS)":
        monthly_inv = st.number_input("Monthly Contribution (₹)", value=5000, step=1000)
        age = st.slider("Current Age", 18, 60, 30)
        years = 60 - age
        rate = st.slider("Expected Market Return (NPS Blended)", 8.0, 12.0, 10.0)
        
        st.info(f"NPS matures at age 60. Remaining years: {years}")
        
        # Similar to SIP calculation
        monthly_rate = (rate / 100) / 12
        months = years * 12
        future_value = monthly_inv * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
        
        st.metric("Estimated Corpus at Age 60", f"₹{future_value:,.2f}")
        st.success(f"Mandatory Annuity (Min 40%): **₹{future_value * 0.4:,.2f}** | Tax-Free Withdrawal (Max 60%): **₹{future_value * 0.6:,.2f}**")

elif asset_class == "Real Estate":
    st.header("🏢 Real Estate & REITs Analyzer")
    st.markdown("Physical property or REITs offering capital appreciation and rental yield.")
    
    col1, col2 = st.columns(2)
    prop_val = col1.number_input("Property/REIT Value (₹)", value=5000000, step=500000)
    years = col2.slider("Holding Period (Years)", 5, 30, 10)
    
    app_rate = st.slider("Capital Appreciation Rate (%)", 1.0, 15.0, 6.0)
    rent_yield = st.slider("Rental/Dividend Yield (%)", 1.0, 10.0, 3.0)
    
    data = []
    current_val = prop_val
    for year in range(1, years + 1):
        current_val *= (1 + app_rate/100)
        total_rent = current_val * (rent_yield/100)
        data.append([year, prop_val, current_val + total_rent])
        
    df = pd.DataFrame(data, columns=['Year', 'Total Invested', 'Portfolio Value'])
    st.plotly_chart(generate_chart(df, "Property Value + Cumulative Rent"), use_container_width=True)

elif asset_class == "Cash Equivalents":
    st.header("💵 High-Liquidity Deposits (FDs/T-Bills)")
    st.markdown("Low-risk, highly liquid instruments offering guaranteed returns.")
    
    col1, col2 = st.columns(2)
    principal = col1.number_input("Principal Amount (₹)", value=100000, step=10000)
    years = col2.slider("Tenure (Years)", 1, 10, 5)
    rate = st.slider("Fixed Interest Rate (%)", 3.0, 9.0, 7.0)
    
    data = []
    for year in range(1, years + 1):
        # Quarterly compounding standard for Indian FDs
        amt = principal * (1 + (rate/100)/4)**(4*year)
        data.append([year, principal, amt])
        
    df = pd.DataFrame(data, columns=['Year', 'Total Invested', 'Portfolio Value'])
    st.plotly_chart(generate_chart(df, "Fixed Deposit Compounding"), use_container_width=True)
    
elif asset_class == "Alternative Investments":
    st.header("🪙 Alternative Assets (Gold/Crypto)")
    st.markdown("High-volatility assets like digital currencies, commodities, or derivatives.")
    
    st.warning("Alternative investments carry significant risk and volatility. Projections here are highly speculative.")
    
    col1, col2 = st.columns(2)
    investment = col1.number_input("Investment Amount (₹)", value=50000, step=5000)
    years = col2.slider("Holding Period (Years)", 1, 10, 5)
    
    # Highly speculative slider
    scenario = st.select_slider(
        "Market Scenario Forecast",
        options=["Bear Market (-20% YoY)", "Stagnant (0% YoY)", "Bull Market (20% YoY)", "Hyper Growth (50% YoY)"]
    )
    
    rates = {"Bear Market (-20% YoY)": -20, "Stagnant (0% YoY)": 0, "Bull Market (20% YoY)": 20, "Hyper Growth (50% YoY)": 50}
    rate = rates[scenario]
    
    data = []
    current_val = investment
    for year in range(1, years + 1):
        current_val *= (1 + rate/100)
        data.append([year, investment, current_val])
        
    df = pd.DataFrame(data, columns=['Year', 'Total Invested', 'Portfolio Value'])
    st.plotly_chart(generate_chart(df, "Speculative Asset Trajectory"), use_container_width=True)
    st.info(f"Final Value Under {scenario}: **₹{current_val:,.2f}**")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #8b949e;'>Nexus Investment Pro V1.0 | Data is for simulation purposes only.</div>", unsafe_allow_html=True)