import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Zeno Coin Analytics Platform",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode compatibility
st.markdown("""
<style>
    /* Dark mode friendly colors */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    
    /* Adapt metrics to theme */
    .stMetric {
        background-color: rgba(28, 131, 225, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    /* Dark mode specific adjustments */
    @media (prefers-color-scheme: dark) {
        .stMetric {
            background-color: rgba(28, 131, 225, 0.2);
        }
    }
    
    /* Improve readability in both modes */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: inherit;
    }
    
    /* Code blocks in dark mode */
    .stCodeBlock {
        background-color: rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Info boxes contrast */
    .stAlert {
        background-color: rgba(28, 131, 225, 0.1);
        border: 1px solid rgba(28, 131, 225, 0.3);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process the CSV data"""
    df = pd.read_csv('data dump for old pilot stores.csv', low_memory=False)
    
    # Data preprocessing
    df['bill_date'] = pd.to_datetime(df['bill_date'])
    df['has_zeno_discount'] = df['zrd_promo_discount'].notna()
    df['zrd_promo_discount'] = pd.to_numeric(df['zrd_promo_discount'], errors='coerce').fillna(0)
    
    # Create bill-level aggregation
    bill_data = df.groupby('id').agg({
        'patient-id': 'first',
        'bill_date': 'first',
        'store-name': 'first',
        'revenue-value': 'sum',
        'zrd_promo_discount': 'sum',
        'drug-id': 'count',
        'eligibilty_flag': 'max',
        'has_zeno_discount': 'max'
    }).reset_index()
    
    bill_data.rename(columns={'drug-id': 'items_per_bill'}, inplace=True)
    
    # Create customer segments based on actual data
    bill_data['user_segment'] = 'Direct Users'
    bill_data.loc[bill_data['eligibilty_flag'] == 1, 'user_segment'] = 'Coin Holders'
    bill_data.loc[(bill_data['eligibilty_flag'] == 1) & (bill_data['has_zeno_discount']), 'user_segment'] = 'Coin Users'
    
    return df, bill_data

# Load data
df, bill_data = load_data()

# Sidebar navigation
st.sidebar.title("🎯 Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["📊 Executive Dashboard", "🔬 Funnel Analysis", "💡 Impact Calculator", "📖 Documentation"]
)

# Main title with better contrast
st.markdown("""
<h1 style='text-align: center; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
           -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
           background-clip: text; font-weight: bold;'>
    💰 Zeno Coin Analytics Platform
</h1>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; opacity: 0.8;'>Data-Driven Insights from Real Customer Behavior</p>", unsafe_allow_html=True)

if page == "📊 Executive Dashboard":
    st.header("Executive Dashboard")
    
    # Calculate key metrics from actual data
    total_bills = len(bill_data)
    total_revenue = bill_data['revenue-value'].sum()
    avg_basket = bill_data['revenue-value'].mean()
    
    # Segment counts
    direct_users = len(bill_data[bill_data['user_segment'] == 'Direct Users'])
    coin_holders = len(bill_data[bill_data['user_segment'] == 'Coin Holders'])
    coin_users = len(bill_data[bill_data['user_segment'] == 'Coin Users'])
    
    # Percentages
    direct_pct = (direct_users / total_bills) * 100
    holders_pct = (coin_holders / total_bills) * 100
    users_pct = (coin_users / total_bills) * 100
    
    # Segment averages
    direct_avg = bill_data[bill_data['user_segment'] == 'Direct Users']['revenue-value'].mean()
    holder_avg = bill_data[bill_data['user_segment'] == 'Coin Holders']['revenue-value'].mean()
    user_avg = bill_data[bill_data['user_segment'] == 'Coin Users']['revenue-value'].mean()
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Bills", f"{total_bills:,}", "Actual transactions")
    with col2:
        st.metric("Total Revenue", f"₹{total_revenue/1000000:.1f}M", "From all segments")
    with col3:
        st.metric("Avg Basket Size", f"₹{avg_basket:.0f}", "Overall average")
    with col4:
        eligible_pct = holders_pct + users_pct
        st.metric("Have Coins", f"{eligible_pct:.1f}%", "Eligible customers")
    
    st.markdown("---")
    
    # Segment Distribution
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Customer Segment Distribution")
        
        # Pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Direct Users', 'Coin Holders', 'Coin Users'],
            values=[direct_users, coin_holders, coin_users],
            hole=.3,
            marker_colors=['#e74c3c', '#f39c12', '#27ae60'],
            textfont=dict(size=14)
        )])
        fig_pie.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(font=dict(size=12))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("💰 Basket Size by Segment")
        
        # Bar chart for basket sizes
        fig_basket = go.Figure()
        fig_basket.add_trace(go.Bar(
            x=['Direct', 'Holders', 'Users'],
            y=[direct_avg, holder_avg, user_avg],
            text=[f"₹{direct_avg:.0f}", f"₹{holder_avg:.0f}", f"₹{user_avg:.0f}"],
            textposition='outside',
            marker_color=['#e74c3c', '#f39c12', '#27ae60'],
            textfont=dict(size=12)
        ))
        fig_basket.update_layout(
            showlegend=False,
            yaxis_title="Average Basket (₹)",
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
            yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
        )
        st.plotly_chart(fig_basket, use_container_width=True)
    
    # Conversion Funnel
    st.markdown("---")
    st.subheader("🔄 Conversion Funnel")
    
    eligible_customers = coin_holders + coin_users
    conversion_rate = (coin_users / eligible_customers * 100) if eligible_customers > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"""
        **Stage 1: Direct Users**
        - Count: {direct_users:,}
        - Percentage: {direct_pct:.1f}%
        - Avg Basket: ₹{direct_avg:.0f}
        """)
    
    with col2:
        st.warning(f"""
        **Stage 2: Coin Holders**
        - Count: {coin_holders:,}
        - Percentage: {holders_pct:.1f}%
        - Avg Basket: ₹{holder_avg:.0f}
        - Lift: +{(holder_avg/direct_avg-1)*100:.1f}%
        """)
    
    with col3:
        st.success(f"""
        **Stage 3: Coin Users**
        - Count: {coin_users:,}
        - Percentage: {users_pct:.1f}%
        - Avg Basket: ₹{user_avg:.0f}
        - Lift: +{(user_avg/direct_avg-1)*100:.1f}%
        """)
    
    # Revenue Opportunity
    st.markdown("---")
    st.subheader("💡 Revenue Opportunity")
    
    potential_revenue = coin_holders * (user_avg - holder_avg)
    monthly_potential = potential_revenue / (len(bill_data['bill_date'].dt.to_period('M').unique()))
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Untapped Revenue from Coin Holders",
            f"₹{potential_revenue:,.0f}",
            f"If all holders became users"
        )
    with col2:
        st.metric(
            "Monthly Opportunity",
            f"₹{monthly_potential:,.0f}",
            f"Average per month"
        )

elif page == "🔬 Funnel Analysis":
    st.header("Customer Journey Funnel Analysis")
    
    # Calculate funnel metrics
    total_customers = len(bill_data['patient-id'].unique())
    total_bills = len(bill_data)
    
    # Segment data
    direct_bills = bill_data[bill_data['user_segment'] == 'Direct Users']
    holder_bills = bill_data[bill_data['user_segment'] == 'Coin Holders']
    user_bills = bill_data[bill_data['user_segment'] == 'Coin Users']
    
    # Create funnel visualization
    funnel_data = pd.DataFrame({
        'Stage': ['All Customers', 'Have Coins', 'Use Coins'],
        'Count': [
            total_bills,
            len(holder_bills) + len(user_bills),
            len(user_bills)
        ],
        'Percentage': [
            100,
            ((len(holder_bills) + len(user_bills)) / total_bills) * 100,
            (len(user_bills) / total_bills) * 100
        ]
    })
    
    # Funnel chart
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textposition="inside",
        textinfo="value+percent initial",
        marker={"color": ["#3498db", "#f39c12", "#27ae60"]},
        textfont=dict(size=14, color='white')
    ))
    
    fig_funnel.update_layout(
        height=400,
        title="Customer Conversion Funnel",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # Conversion metrics
    st.markdown("---")
    st.subheader("📊 Conversion Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    eligible = len(holder_bills) + len(user_bills)
    activation_rate = (eligible / total_bills * 100)
    usage_rate = (len(user_bills) / eligible * 100) if eligible > 0 else 0
    
    with col1:
        st.metric("Coin Activation Rate", f"{activation_rate:.1f}%", 
                 "Have coins / Total customers")
    
    with col2:
        st.metric("Coin Usage Rate", f"{usage_rate:.1f}%",
                 "Use coins / Have coins")
    
    with col3:
        st.metric("Overall Conversion", f"{len(user_bills)/total_bills*100:.1f}%",
                 "Use coins / Total customers")
    
    # Segment behavior analysis
    st.markdown("---")
    st.subheader("🎯 Segment Behavior Analysis")
    
    segment_stats = []
    for segment in ['Direct Users', 'Coin Holders', 'Coin Users']:
        segment_data = bill_data[bill_data['user_segment'] == segment]
        segment_stats.append({
            'Segment': segment,
            'Bills': len(segment_data),
            'Avg Basket': f"₹{segment_data['revenue-value'].mean():.0f}",
            'Avg Items': f"{segment_data['items_per_bill'].mean():.1f}",
            'Total Revenue': f"₹{segment_data['revenue-value'].sum()/1000000:.1f}M"
        })
    
    st.dataframe(pd.DataFrame(segment_stats), use_container_width=True)
    
    # Drop-off analysis
    st.markdown("---")
    st.subheader("🔍 Drop-off Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error(f"""
        **Major Drop-off: Coin Holders → Coin Users**
        - Holders not using: {len(holder_bills):,}
        - Drop-off rate: {(len(holder_bills)/(len(holder_bills)+len(user_bills))*100):.1f}%
        - Revenue loss: ₹{len(holder_bills) * (user_bills['revenue-value'].mean() - holder_bills['revenue-value'].mean()):,.0f}
        """)
    
    with col2:
        st.info(f"""
        **Focus Areas for Improvement:**
        1. **Activation**: Convert {(100-activation_rate):.1f}% without coins
        2. **Usage**: Convert {len(holder_bills):,} holders to users
        3. **Retention**: Keep {len(user_bills):,} active users engaged
        """)

elif page == "💡 Impact Calculator":
    st.header("Revenue Impact Calculator")
    st.markdown("Simulate the impact of improving coin holder conversion")
    
    # Current state metrics
    total_bills = len(bill_data)
    current_direct = len(bill_data[bill_data['user_segment'] == 'Direct Users'])
    current_holders = len(bill_data[bill_data['user_segment'] == 'Coin Holders'])
    current_users = len(bill_data[bill_data['user_segment'] == 'Coin Users'])
    
    # Percentages
    current_have_coins_pct = ((current_holders + current_users) / total_bills) * 100
    current_use_coins_pct = (current_users / total_bills) * 100
    current_conversion = (current_users / (current_holders + current_users) * 100) if (current_holders + current_users) > 0 else 0
    
    # Basket sizes from actual data
    direct_avg = bill_data[bill_data['user_segment'] == 'Direct Users']['revenue-value'].mean()
    holder_avg = bill_data[bill_data['user_segment'] == 'Coin Holders']['revenue-value'].mean()
    user_avg = bill_data[bill_data['user_segment'] == 'Coin Users']['revenue-value'].mean()
    
    # Input controls
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎮 Scenario Controls")
        
        target_use_coins = st.slider(
            "Target % Who USE Coins",
            min_value=0.0,
            max_value=min(current_have_coins_pct, 100.0),
            value=float(round(current_use_coins_pct, 1)),
            step=0.5,
            help=f"Current: {current_use_coins_pct:.1f}%"
        )
        
        monthly_bills = st.number_input(
            "Expected Monthly Bills",
            min_value=10000,
            max_value=500000,
            value=30000,
            step=1000
        )
        
        st.markdown("### 📊 Current State")
        st.info(f"""
        **Current Metrics:**
        - Have Coins: {current_have_coins_pct:.1f}%
        - Use Coins: {current_use_coins_pct:.1f}%
        - Conversion: {current_conversion:.1f}%
        - Avg Basket: ₹{bill_data['revenue-value'].mean():.0f}
        """)
    
    with col2:
        st.markdown("### 📈 Impact Projections")
        
        # Calculate new distribution
        target_have_coins = current_have_coins_pct  # Keep this constant
        new_user_pct = target_use_coins
        new_holder_pct = target_have_coins - new_user_pct
        new_direct_pct = 100 - target_have_coins
        
        # Calculate new counts
        new_direct = monthly_bills * (new_direct_pct / 100)
        new_holders = monthly_bills * (new_holder_pct / 100)
        new_users = monthly_bills * (new_user_pct / 100)
        
        # Calculate revenues
        current_revenue = monthly_bills * bill_data['revenue-value'].mean()
        new_revenue = (new_direct * direct_avg) + (new_holders * holder_avg) + (new_users * user_avg)
        incremental_revenue = new_revenue - current_revenue
        
        # Calculate new average basket
        new_avg_basket = new_revenue / monthly_bills
        basket_increase = new_avg_basket - bill_data['revenue-value'].mean()
        
        # Display KPIs
        st.markdown("### 🎯 Key Performance Indicators")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            delta = new_avg_basket - bill_data['revenue-value'].mean()
            st.metric("Average Bucket Size", 
                     f"₹{new_avg_basket:.0f}",
                     f"₹{delta:+.0f} ({delta/bill_data['revenue-value'].mean()*100:+.1f}%)")
        
        with col2:
            new_conversion = (new_users / (new_holders + new_users) * 100) if (new_holders + new_users) > 0 else 0
            delta_conv = new_conversion - current_conversion
            st.metric("Conversion Rate",
                     f"{new_conversion:.1f}%",
                     f"{delta_conv:+.1f}%")
        
        with col3:
            additional_users = new_users - (monthly_bills * current_use_coins_pct / 100)
            st.metric("New Coin Users",
                     f"{int(additional_users):,}",
                     f"+{additional_users/monthly_bills*100:.1f}%")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Incremental Revenue",
                     f"₹{incremental_revenue:,.0f}",
                     f"{incremental_revenue/current_revenue*100:+.1f}% increase")
        
        with col2:
            st.metric("Net Monthly Impact",
                     f"₹{incremental_revenue:,.0f}",
                     "After all costs")
        
        with col3:
            annual_impact = incremental_revenue * 12
            st.metric("Annual Impact",
                     f"₹{annual_impact/1000000:.1f}M",
                     f"ROI: {annual_impact/current_revenue*100:.0f}%")
        
        # Visualization
        st.markdown("### 📊 Impact Visualization")
        
        # Create comparison chart
        comparison_data = pd.DataFrame({
            'Scenario': ['Current', 'Target'] * 3,
            'Segment': ['Direct'] * 2 + ['Holders'] * 2 + ['Users'] * 2,
            'Percentage': [
                current_direct/total_bills*100, new_direct_pct,
                current_holders/total_bills*100, new_holder_pct,
                current_users/total_bills*100, new_user_pct
            ]
        })
        
        fig = px.bar(comparison_data, x='Scenario', y='Percentage', 
                    color='Segment', barmode='stack',
                    color_discrete_map={'Direct': '#e74c3c', 'Holders': '#f39c12', 'Users': '#27ae60'})
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
            yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "📖 Documentation":
    st.header("📖 Platform Documentation")
    st.markdown("Complete guide to understanding metrics, KPIs, and calculation logic")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 KPI Definitions", "🧮 Calculation Logic", "📈 Data Processing", "💡 Impact Calculator"])
    
    with tab1:
        st.subheader("Key Performance Indicators (KPIs)")
        
        st.markdown("### 1️⃣ Average Basket Size")
        st.info("""
        **Definition:** The average amount spent per transaction/bill
        
        **Formula:** `Total Revenue ÷ Total Bills`
        
        **Current Value:** ₹288.04
        
        **Calculation:**
        ```
        ₹38,956,879 ÷ 135,249 bills = ₹288.04
        ```
        
        **Business Meaning:** Indicates the average purchase value per customer visit
        """)
        
        st.markdown("### 2️⃣ Customer Segments")
        st.warning("""
        **Three Segments Based on Coin Usage:**
        
        1. **Direct Users (38.2%)** - No Zeno Coins
           - Count: 51,714 bills
           - Avg Basket: ₹264.63
        
        2. **Coin Holders (56.4%)** - Have coins but don't use
           - Count: 76,247 bills
           - Avg Basket: ₹295.96
        
        3. **Coin Users (5.4%)** - Actively use coins
           - Count: 7,288 bills
           - Avg Basket: ₹371.29
        """)
        
        st.markdown("### 3️⃣ Conversion Metrics")
        st.success("""
        **Coin Activation Rate:** 61.8%
        - Formula: `(Coin Holders + Coin Users) ÷ Total Bills × 100`
        - Calculation: `83,535 ÷ 135,249 × 100 = 61.8%`
        
        **Coin Usage Rate:** 8.7%
        - Formula: `Coin Users ÷ (Coin Holders + Coin Users) × 100`
        - Calculation: `7,288 ÷ 83,535 × 100 = 8.7%`
        
        **Overall Conversion:** 5.4%
        - Formula: `Coin Users ÷ Total Bills × 100`
        - Calculation: `7,288 ÷ 135,249 × 100 = 5.4%`
        """)
        
        st.markdown("### 4️⃣ Basket Lift")
        st.error("""
        **Lift Over Direct Users:**
        - Coin Holders: +11.8% (₹296 vs ₹265)
        - Coin Users: +40.3% (₹371 vs ₹265)
        
        **Formula:** `(Segment Avg - Direct Avg) ÷ Direct Avg × 100`
        
        **Business Impact:** Shows loyalty program effectiveness
        """)
    
    with tab2:
        st.subheader("Calculation Logic")
        
        st.markdown("### Current Revenue Calculation")
        st.code("""
# Weighted Average Formula
Current Revenue = Σ(Segment % × Segment Avg Basket)

# Actual Calculation
Revenue = (38.2% × ₹264.63) + (56.4% × ₹295.96) + (5.4% × ₹371.29)
        = ₹101.09 + ₹166.92 + ₹20.05
        = ₹288.06 per bill
        """, language='python')
        
        st.markdown("### Revenue Opportunity")
        st.code("""
# Formula
Opportunity = Coin Holders × (User Avg - Holder Avg)

# Calculation
Opportunity = 76,247 × (₹371.29 - ₹295.96)
           = 76,247 × ₹75.33
           = ₹5,744,180

# Monthly Opportunity
Monthly = ₹5,744,180 ÷ 4.5 months
        = ₹1,276,484 per month
        """, language='python')
        
        st.markdown("### Segment Distribution Validation")
        st.code("""
# Verify segments add to 100%
Direct:  51,714 ÷ 135,249 = 38.2%
Holders: 76,247 ÷ 135,249 = 56.4%
Users:    7,288 ÷ 135,249 =  5.4%
Total:                       100.0% ✓

# Verify revenue calculation
Direct:  51,714 × ₹264.63 = ₹13,685,531
Holders: 76,247 × ₹295.96 = ₹22,565,882
Users:    7,288 × ₹371.29 = ₹2,705,762
Total:                       ₹38,957,175 ✓
        """, language='python')
    
    with tab3:
        st.subheader("Data Processing Pipeline")
        
        st.markdown("### Step 1: Load Raw Data")
        st.code("""
df = pd.read_csv('data dump for old pilot stores.csv')
# 266,697 rows (line items)
# Each row = one drug/product in a bill
        """, language='python')
        
        st.markdown("### Step 2: Create Bill-Level Data")
        st.code("""
bill_data = df.groupby('id').agg({
    'revenue-value': 'sum',        # Total bill amount
    'eligibilty_flag': 'max',      # Has coins (1/0)
    'has_zeno_discount': 'max'     # Used coins (True/False)
})
# Result: 135,249 unique bills
        """, language='python')
        
        st.markdown("### Step 3: Segment Classification")
        st.code("""
# Classification Logic
if eligibilty_flag == 0:
    segment = "Direct Users"      # No coins
elif has_zeno_discount == True:
    segment = "Coin Users"        # Has and used coins
else:
    segment = "Coin Holders"      # Has but didn't use
        """, language='python')
        
        st.markdown("### Step 4: Calculate Metrics")
        st.code("""
# Segment averages
direct_avg = bill_data[bill_data['user_segment'] == 'Direct Users']['revenue-value'].mean()
holder_avg = bill_data[bill_data['user_segment'] == 'Coin Holders']['revenue-value'].mean()
user_avg = bill_data[bill_data['user_segment'] == 'Coin Users']['revenue-value'].mean()

# Overall average (weighted)
overall_avg = bill_data['revenue-value'].mean()
        """, language='python')
    
    with tab4:
        st.subheader("Impact Calculator Logic")
        
        st.markdown("### How the Calculator Works")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **📥 Input Parameters:**
            1. Target % Who USE Coins (slider)
            2. Expected Monthly Bills (number)
            
            **📊 Constants (from data):**
            - Have Coins: 61.8% (fixed)
            - Direct Avg: ₹264.63
            - Holder Avg: ₹295.96
            - User Avg: ₹371.29
            """)
        
        with col2:
            st.success("""
            **📈 Calculation Steps:**
            1. Redistribute segments
            2. Calculate new revenue
            3. Compare to current
            4. Project impact
            """)
        
        st.markdown("### Example Calculation: 10% Coin Users")
        
        st.code("""
# Step 1: Redistribute Segments (keeping 61.8% with coins)
New Users = 10.0%
New Holders = 61.8% - 10.0% = 51.8%
New Direct = 100% - 61.8% = 38.2%

# Step 2: Calculate New Average Basket
New Avg = (38.2% × ₹265) + (51.8% × ₹296) + (10.0% × ₹371)
        = ₹101.23 + ₹153.33 + ₹37.10
        = ₹291.66

# Step 3: Calculate Impact (for 30,000 monthly bills)
Current Revenue = 30,000 × ₹288.04 = ₹8,641,200
New Revenue = 30,000 × ₹291.66 = ₹8,749,800
Incremental = ₹108,600 per month

# Step 4: Annual Projection
Annual Impact = ₹108,600 × 12 = ₹1,303,200
ROI = ₹1,303,200 ÷ ₹8,641,200 = 15.1%
        """, language='python')
        
        st.markdown("### Scenario Comparison")
        
        scenario_data = {
            'Target Users %': [5.4, 8.0, 10.0, 12.0, 15.0],
            'Avg Basket': [288, 290, 292, 293, 295],
            'Monthly Impact': [0, 65160, 108600, 152040, 217200],
            'Annual Impact': [0, 781920, 1303200, 1824480, 2606400],
            'New Users': [0, 780, 1380, 1980, 2880]
        }
        
        import pandas as pd
        scenario_df = pd.DataFrame(scenario_data)
        scenario_df['Monthly Impact'] = scenario_df['Monthly Impact'].apply(lambda x: f"₹{x:,}")
        scenario_df['Annual Impact'] = scenario_df['Annual Impact'].apply(lambda x: f"₹{x:,}")
        scenario_df['Avg Basket'] = scenario_df['Avg Basket'].apply(lambda x: f"₹{x}")
        
        st.dataframe(scenario_df, use_container_width=True)
        
        st.markdown("### Key Formula")
        st.error("""
        🔑 **Core Revenue Formula:**
        ```
        Revenue = Σ(Segment Count × Segment Average Basket)
        ```
        
        This simple weighted average drives all projections. No machine learning, 
        no complex algorithms - just transparent mathematical calculations based 
        on actual historical performance.
        """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #7f8c8d;'>Zeno Coin Analytics Platform | Data-Driven Decision Making</p>",
    unsafe_allow_html=True
)