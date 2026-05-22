import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# TITLE
st.title("Coffee Sales Analysis Dashboard")

# LOAD DATA
df = pd.read_csv("sales_data.csv")

df["transaction_time"] = pd.to_datetime(df["transaction_time"], format="mixed")

# FEATURE ENGINEERING
df["sales"] = df["transaction_qty"] * df["unit_price"]
df["hour"] = df["transaction_time"].dt.hour
df["day"] = df["transaction_time"].dt.day_name()


# SIDEBAR FILTERS (important)

st.sidebar.header("Filters")

# STORE FILTER
selected_store = st.sidebar.selectbox(
    "Select Store Location",
    df["store_location"].unique()
)

filtered_df = df[df["store_location"] == selected_store]

# DAY FILTER
selected_day = st.sidebar.selectbox("Select Day", df["day"].unique())
filtered_df = filtered_df[filtered_df["day"] == selected_day]

# HOUR RANGE SLIDER
hour_range = st.sidebar.slider("Select Hour Range",0, 23, (6, 18))

filtered_df = filtered_df[
    (filtered_df["hour"] >= hour_range[0]) &
    (filtered_df["hour"] <= hour_range[1])
]

# METRIC TOGGLE
metric = st.selectbox(
    "Select Metric",
    ["Sales", "Quantity"]
)

if metric == "Sales":
    value_col = "sales"
else:
    value_col = "transaction_qty"

# TOTAL VALUE
st.subheader("Total Value")
st.write(filtered_df[value_col].sum())

# HOURLY TREND
st.subheader("Hourly Trend")
hour_sales = filtered_df.groupby("hour")[value_col].sum()
st.line_chart(hour_sales)

# DAY TREND
st.subheader("Day-wise Performance")
day_sales = filtered_df.groupby("day")[value_col].sum()
st.bar_chart(day_sales)

# CATEGORY ANALYSIS
st.subheader("Product Category Analysis")
cat_sales = filtered_df.groupby("product_category")[value_col].sum()
st.bar_chart(cat_sales)

# STORE COMPARISON
st.subheader("Store Comparison")
store_sales = df.groupby("store_location")[value_col].sum()
st.bar_chart(store_sales)

# HEATMAP (TABLE FORMAT)
st.subheader("Heatmap (Hour vs Day)")

pivot = filtered_df.pivot_table(
    values=value_col,
    index="day",
    columns="hour",
    aggfunc="sum"
)

st.write(pivot)