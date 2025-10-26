# Zeno Coin Analytics Platform

A comprehensive analytics dashboard for analyzing the Zeno Coin loyalty program's impact on customer behavior and revenue.

## 🚀 Features

- **Executive Dashboard**: Real-time KPIs and segment distribution analysis
- **Funnel Analysis**: Customer conversion journey from Direct Users → Coin Holders → Coin Users  
- **Impact Calculator**: Revenue projections based on conversion improvements
- **Documentation**: Built-in documentation with KPI definitions and calculation logic
- **Dark Mode**: Full dark mode support for better visibility

## 📊 Key Metrics

- **Average Basket Size**: ₹288
- **Customer Segments**:
  - Direct Users: 38.2% (₹265 avg basket)
  - Coin Holders: 56.4% (₹296 avg basket)  
  - Coin Users: 5.4% (₹371 avg basket)
- **Conversion Rate**: 8.7% of coin holders actually use coins
- **Revenue Opportunity**: ₹5.7M from converting holders to users

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/prsuman1/Zeno-Health-coin1.git
cd Zeno-Health-coin1
```

2. Install dependencies:
```bash
pip install streamlit pandas numpy plotly
```

3. Run the application:
```bash
streamlit run zeno_analytics_app.py
```

## 📁 Project Structure

```
├── zeno_analytics_app.py     # Main application file
├── data dump for old pilot stores.csv  # Transaction data
├── DOCUMENTATION.md           # Detailed documentation
├── .streamlit/
│   └── config.toml           # Dark mode configuration
└── README.md                 # This file
```

## 💡 How It Works

The platform uses **weighted average calculations** based on actual transaction data:

```python
Revenue = Σ(Segment Count × Segment Average Basket)
```

### Example Calculation (10% Coin Users):
- Direct: 38.2% × ₹265 = ₹101
- Holders: 51.8% × ₹296 = ₹153
- Users: 10.0% × ₹371 = ₹37
- **Total**: ₹291 average basket

## 📈 Impact Calculator Logic

1. **Input**: Target % of customers who use coins
2. **Processing**: Redistributes customers between segments
3. **Output**: Projects new revenue and ROI

**No machine learning** - just transparent mathematical calculations based on historical performance.

## 🎨 Dark Mode

The app includes full dark mode support with:
- Dark background (#0e1117)
- Purple accent (#667eea)
- Optimized chart colors
- Adaptive text contrast

## 📝 Data Processing

1. **Load CSV**: 266,697 transaction rows
2. **Aggregate**: Group by bill ID → 135,249 unique bills
3. **Segment**: Classify based on coin eligibility and usage
4. **Calculate**: Derive metrics and averages per segment

## 🔑 Key Insights

- **61.8%** of customers have coins (good activation)
- Only **8.7%** of eligible customers use coins (major opportunity)
- Coin users spend **40.3%** more than direct users
- **₹1.3M** annual impact per 5% increase in usage

## 📊 Business Value

The platform enables data-driven decisions by:
- Identifying conversion bottlenecks
- Quantifying revenue opportunities
- Projecting ROI of loyalty initiatives
- Tracking segment performance

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the platform.

## 📄 License

MIT License - feel free to use and modify as needed.

---

Built with ❤️ using Streamlit and Plotly