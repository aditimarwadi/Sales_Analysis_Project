import pandas as pd
import matplotlib.pyplot as plt

# Data Ingestion & Validation

df = pd.read_csv("sales_data.csv")

df["transaction_time"] = pd.to_datetime(df["transaction_time"], format="mixed")

print(df.info())
print(df.isnull().sum())


# Feature Engineering

df["sales"] = df["transaction_qty"] * df["unit_price"]
df["hour"] = df["transaction_time"].dt.hour
df["day"] = df["transaction_time"].dt.day_name()


# Sales Trend Analysis

df.groupby("year")["sales"].sum().plot(kind="line")
plt.title("Yearly Sales Trend")
plt.show()


# Day-of-Week Analysis

day_sales = df.groupby("day")["sales"].sum()
print(day_sales)

day_sales.plot(kind="bar")
plt.title("Sales by Day of Week")
plt.show()


# Time-of-Day Analysis
hour_sales = df.groupby("hour")["sales"].sum()

hour_sales.plot(kind="line")
plt.title("Hourly Sales Trend")
plt.show()


# Store Comparison

store_sales = df.groupby("store_location")["sales"].sum()
print(store_sales)

store_sales.plot(kind="bar")
plt.title("Sales by Store Location")
plt.show()


# Product Analysis

product_sales = df.groupby("product_type")["sales"].sum()
print(product_sales.sort_values(ascending=False).head())


# Final Key Findings

print("Top Day:", day_sales.idxmax())
print("Peak Hour:", hour_sales.idxmax())
print("Best Store:", store_sales.idxmax())