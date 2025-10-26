# Zeno Coin Analytics Platform - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Data Processing Logic](#data-processing-logic)
3. [Customer Segmentation](#customer-segmentation)
4. [Executive Dashboard](#executive-dashboard)
5. [Funnel Analysis](#funnel-analysis)
6. [Impact Calculator](#impact-calculator)
7. [Calculation Methods](#calculation-methods)

---

## Overview

The Zeno Coin Analytics Platform analyzes customer behavior and revenue impact of the Zeno Coin loyalty program using actual transaction data.

**Key Data Points:**
- Total Transactions: 266,697 rows
- Unique Bills: 135,249
- Unique Customers: 39,037
- Overall Average Basket: ₹288.04

---

## Data Processing Logic

### 1. Data Loading
```python
df = pd.read_csv('data dump for old pilot stores.csv')
```
- Loads raw transaction data with line-item details
- Each row represents a single drug/item in a bill

### 2. Bill Aggregation
```python
bill_data = df.groupby('id').agg({
    'revenue-value': 'sum',      # Total bill amount
    'eligibilty_flag': 'max',    # Has coins (1) or not (0)
    'has_zeno_discount': 'max'   # Used coins (True/False)
})
```
- Groups line items by bill ID
- Creates bill-level summary with total revenue

### 3. Segmentation Logic
```python
if eligibilty_flag == 0:
    segment = "Direct Users"      # No coins
elif has_zeno_discount == True:
    segment = "Coin Users"         # Has and used coins
else:
    segment = "Coin Holders"       # Has but didn't use coins
```

---

## Customer Segmentation

### Three Distinct Segments

| Segment | Count | Percentage | Avg Basket | Description |
|---------|-------|------------|------------|-------------|
| **Direct Users** | 51,714 | 38.2% | ₹264.63 | Customers without Zeno Coins |
| **Coin Holders** | 76,247 | 56.4% | ₹295.96 | Have coins but didn't use them |
| **Coin Users** | 7,288 | 5.4% | ₹371.29 | Have and actively use coins |

### Key Insights
- **Basket Lift Analysis:**
  - Holders spend 11.8% more than Direct Users
  - Users spend 40.3% more than Direct Users
  - Users spend 25.4% more than Holders

---

## Executive Dashboard

### Metrics Displayed

#### 1. Top-Level KPIs
- **Total Bills**: 135,249 transactions
- **Total Revenue**: ₹39.0M
- **Average Basket**: ₹288 (weighted average across all segments)
- **Have Coins**: 61.8% (Holders + Users)

#### 2. Segment Distribution (Pie Chart)
```
Calculation:
Direct: 51,714 / 135,249 = 38.2%
Holders: 76,247 / 135,249 = 56.4%
Users: 7,288 / 135,249 = 5.4%
```

#### 3. Basket Size Comparison (Bar Chart)
Shows average basket by segment with lift percentages

#### 4. Revenue Opportunity
```python
Opportunity = Coin Holders × (User Avg - Holder Avg)
           = 76,247 × (₹371.29 - ₹295.96)
           = ₹5,744,180
```

---

## Funnel Analysis

### Conversion Funnel Stages

#### Stage 1: All Customers
- Count: 135,249 bills (100%)
- Baseline for conversion analysis

#### Stage 2: Have Coins (Eligible)
- Count: 83,535 bills (61.8%)
- Formula: `Holders + Users`
- Activation Rate: 61.8%

#### Stage 3: Use Coins (Active)
- Count: 7,288 bills (5.4%)
- Usage Rate: 8.7% of eligible
- Formula: `Users / (Holders + Users)`

### Drop-off Analysis
```
Major Drop-off Point: Holders → Users
- Holders not converting: 76,247
- Drop-off rate: 91.3%
- Revenue loss: ₹5.7M potential
```

### Conversion Metrics
- **Coin Activation Rate**: 61.8% (have coins / total)
- **Coin Usage Rate**: 8.7% (use coins / have coins)
- **Overall Conversion**: 5.4% (use coins / total)

---

## Impact Calculator

### Core Logic

The calculator uses **weighted average calculations** based on actual segment performance:

#### Current State Calculation
```python
Current Revenue = (Direct% × Direct_Avg) + (Holders% × Holder_Avg) + (Users% × User_Avg)

Example (actual data):
Current = (38.2% × ₹265) + (56.4% × ₹296) + (5.4% × ₹371)
        = ₹101.23 + ₹166.94 + ₹20.05
        = ₹288.22
```

#### Projection Logic

**Step 1: Redistribute Segments**
When slider is moved to target (e.g., 10% users):
```python
# Keep "Have Coins" percentage constant at 61.8%
New_Users% = 10%
New_Holders% = 61.8% - 10% = 51.8%
New_Direct% = 100% - 61.8% = 38.2%
```

**Step 2: Calculate New Revenue**
```python
New_Revenue = (38.2% × ₹265) + (51.8% × ₹296) + (10% × ₹371)
           = ₹101.23 + ₹153.33 + ₹37.13
           = ₹291.69 per bill
```

**Step 3: Calculate Impact**
```python
Basket Increase = ₹291.69 - ₹288.22 = ₹3.47
Revenue Increase = ₹3.47 × Monthly_Bills
Annual Impact = Revenue_Increase × 12
```

### Example Scenarios

#### Scenario 1: Current State (5.4% users)
- Average Basket: ₹288
- Monthly Revenue: ₹8,641,200 (30K bills)

#### Scenario 2: Target 10% users
- Average Basket: ₹292 (+₹4)
- New Distribution: 38.2% Direct, 51.8% Holders, 10% Users
- Monthly Revenue: ₹8,750,700 (30K bills)
- Incremental Revenue: ₹109,500/month
- Annual Impact: ₹1.31M

#### Scenario 3: Target 15% users
- Average Basket: ₹295 (+₹7)
- New Distribution: 38.2% Direct, 46.8% Holders, 15% Users
- Monthly Revenue: ₹8,860,200 (30K bills)
- Incremental Revenue: ₹219,000/month
- Annual Impact: ₹2.63M

---

## Calculation Methods

### 1. Average Basket Size
```python
Overall_Avg = Total_Revenue / Total_Bills
           = ₹38,956,879 / 135,249
           = ₹288.04
```

### 2. Weighted Average (for projections)
```python
Weighted_Avg = Σ(Segment_Percentage × Segment_Avg_Basket)
```

### 3. Conversion Rate
```python
Conversion = (Coin_Users / Eligible_Customers) × 100
          = (7,288 / 83,535) × 100
          = 8.7%
```

### 4. Revenue Impact
```python
Impact = (New_Avg_Basket - Current_Avg_Basket) × Number_of_Bills
```

### 5. ROI Calculation
```python
ROI = (Annual_Incremental_Revenue / Current_Annual_Revenue) × 100
```

---

## Key Business Insights

### Current Performance
1. **61.8% of customers have coins** - Good activation
2. **Only 8.7% of eligible customers use coins** - Major opportunity
3. **40.3% higher basket for coin users** - Strong program impact

### Revenue Opportunities
1. **Immediate**: ₹5.7M from converting existing holders
2. **Monthly**: ₹109K+ per 5% increase in usage
3. **Annual**: ₹1.3M+ per 5% increase in usage

### Focus Areas
1. **Activation Gap**: 38.2% don't have coins
2. **Usage Gap**: 91.3% of coin holders don't use them
3. **Retention**: Maintain the 5.4% active users

---

## Technical Implementation

### Libraries Used
- **pandas**: Data processing and aggregation
- **streamlit**: Web application framework
- **plotly**: Interactive visualizations
- **numpy**: Numerical calculations

### Data Flow
1. CSV → pandas DataFrame
2. Line items → Bill aggregation
3. Bill data → Segment classification
4. Segments → Metrics calculation
5. Metrics → Visualization

### No Machine Learning
- All calculations are deterministic
- Based on actual historical averages
- Linear projections for impact analysis
- No predictive models or algorithms

---

## Validation

### Data Integrity Checks
```python
# Sum of segments should equal total
assert Direct + Holders + Users == Total_Bills

# Weighted average should match overall
calculated_avg = (Direct% × Direct_Avg) + (Holders% × Holder_Avg) + (Users% × User_Avg)
assert abs(calculated_avg - Overall_Avg) < 1  # Allow ₹1 rounding
```

### Calculation Verification
- Direct Users: 51,714 × ₹264.63 = ₹13,685,531
- Coin Holders: 76,247 × ₹295.96 = ₹22,565,882
- Coin Users: 7,288 × ₹371.29 = ₹2,705,762
- **Total**: ₹38,957,175 ✓ (matches actual ₹38,956,879)

---

## Conclusion

The platform provides data-driven insights using straightforward mathematical calculations on actual transaction data. No complex algorithms or predictions - just clear, verifiable metrics to guide business decisions.

**Core Formula:**
```
Revenue = Σ(Segment_Count × Segment_Avg_Basket)
```

This transparent approach ensures all stakeholders can understand and verify the numbers.