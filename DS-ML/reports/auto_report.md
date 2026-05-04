# Automated EDA Report

## Dataset Overview
- Rows: 200
- Columns: 15

## Column Types
- Numerical: ['Distance', 'Delivery_Person_Experience', 'Restaurant_Rating', 'Customer_Rating', 'Delivery_Time', 'Order_Cost', 'Tip_Amount']
- Categorical: ['Order_ID', 'Customer_Location', 'Restaurant_Location', 'Weather_Conditions', 'Traffic_Conditions', 'Order_Priority', 'Order_Time', 'Vehicle_Type']
- Datetime: []

## Missing Values
No missing values detected.

## Special Columns
- Constant columns: []
- High cardinality columns: ['Order_ID', 'Customer_Location', 'Restaurant_Location']

## Visualizations
All plots saved in `reports/figures/`

## Feature Importance
- Distance
- Tip_Amount
- Restaurant_Rating
- Customer_Rating
- Delivery_Time
- Delivery_Person_Experience
- Order_Priority_Medium
- Order_Priority_Low
- Weather_Conditions_Snowy
- Order_Time_Evening
