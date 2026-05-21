import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Coffee Sales Analysis Dashboard")

# Load Data
df = pd.read_csv("sales_data.csv")

df["transaction_time"] = pd.to_datetime(df["transaction_time"], format="mixed")

# Feature Engineering
df["sales"] = df["transaction_qty"] * df["unit_price"]
df["hour"] = df["transaction_time"].dt.hour
df["day"] = df["transaction_time"].dt.day_name()


# FILTERS (important)

st.sidebar.header("Filters")

selected_store = st.sidebar.selectbox(
    "Select Store Location",
    df["store_location"].unique()
)

filtered_df = df[df["store_location"] == selected_store]

selected_day = st.sidebar.selectbox("Select Day", df["day"].unique())
filtered_df = filtered_df[filtered_df["day"] == selected_day]


# TOTAL SALES

st.subheader("Total Sales")
st.write(filtered_df["sales"].sum())


# HOURLY TREND

st.subheader("Hourly Sales Trend")

hour_sales = filtered_df.groupby("hour")["sales"].sum()
st.line_chart(hour_sales)


# DAY OF WEEK

st.subheader("Sales by Day")

day_sales = filtered_df.groupby("day")["sales"].sum()
st.bar_chart(day_sales)


# PRODUCT CATEGORY

st.subheader("Sales by Category")

cat_sales = filtered_df.groupby("product_category")["sales"].sum()
st.bar_chart(cat_sales)