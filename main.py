import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dataset/ecommerce_sales_dataset_150_orders.csv")

print(df.head())

print("Dataset Shape:", df.shape)

print("Column Names:", df.columns)

print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Order IDs:")
print(df["Order_ID"].duplicated().sum())

print("\nMinimum and Maximum Values:")
print(df[["Quantity", "Unit_Price", "Discount_Percent"]].agg(["min", "max"]))

#Convert Order_Date into datetime format
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
print("\nUpdated Data Types:")
print(df.dtypes)

#Calculate Gross Revenue
df["Gross_Revenue"] = df["Quantity"] * df["Unit_Price"]
#Calculate Discount Amount
df["Discount_Amount"] = (df["Gross_Revenue"] * df["Discount_Percent"] / 100)
#calculate Net Revenue
df["Net_Revenue"] = df["Gross_Revenue"] - df["Discount_Amount"]
#Display revenue columns
print("\nRevenue Calculation:")
print(df[["Quantity", "Unit_Price", "Discount_Percent", "Gross_Revenue", "Discount_Amount", "Net_Revenue"]].head())

print("\nOrder Status Count:")
print(df["Order_Status"].value_counts())

#Filter only delivered orders
delivered_df = df[df["Order_Status"] == "Delivered"].copy()
print("\nDelivered Orders:")
print(delivered_df.head())
print("\nTotal Delivered Order:", len(delivered_df))

#Calculate total delivered sales revenue
total_revenue = delivered_df["Net_Revenue"].sum()
print("\nTotal Delivered Sales Revenue:")
print("Total Revenue", total_revenue)

print("\nProduct-wise Revenue:")
product_sales = delivered_df.groupby("Product")["Net_Revenue"].sum()
print(product_sales)

#sort products by revenue in descending order
product_sales_sorted = product_sales.sort_values(ascending=False)
print("\nProducts Ranked by Revenue:")
print(product_sales_sorted)

#Calculate category-wise revenue
category_sales = delivered_df.groupby("Category")["Net_Revenue"].sum()
#Sort categories by revenue
category_sales_sorted = category_sales.sort_values(ascending=False)
print("\nCategory-wise Revenue:")
print(category_sales_sorted)

#calculate city-wise revenue
city_sales = delivered_df.groupby("City")["Net_Revenue"].sum()
#Sort cities by revenue
city_sales_sorted = city_sales.sort_values(ascending=False)
print("\nCity-wise Revenue:")
print(city_sales_sorted)

#Extract year and month from Order_Date
delivered_df["Year_Month"] = delivered_df["Order_Date"].dt.to_period("M")
#Calculate monthly revenue
monthly_sales = delivered_df.groupby("Year_Month")["Net_Revenue"].sum()
#Sort monthly revenue by date
monthly_sales = monthly_sales.sort_index()
print("\nMonthly Revenue:")
print(monthly_sales)

#Find hightest revenue month
hightest_month = monthly_sales.idxmax()
hightest_revenue = monthly_sales.max()
#Find lowest revenue month
lowest_month = monthly_sales.idxmin()
lowest_revenue = monthly_sales.min()
print("\nHighest Revenue Month:")
print(hightest_month, hightest_revenue)
print("\nLowest Revenue Month:")
print(lowest_month, lowest_revenue)

#Count orders by payment method
payment_counts = delivered_df["Payment_Method"].value_counts()
print("\nPayment Method Analysis:")
print(payment_counts)

#Calculate payment method-wise revenue
payment_revenue = delivered_df.groupby("Payment_Method")["Net_Revenue"].sum()
#Sort revenue from highest to lowest
payment_revenue_sorted = payment_revenue.sort_values(ascending=False)
print("\nPayment Method-wise Revenue:")
print(payment_revenue_sorted)


import matplotlib.pyplot as plt
#Create product revenue chart
plt.figure(figsize=(12, 6))
product_sales_sorted.plot(kind="bar")
plt.title("Product-wise Revenue Analysis")
plt.xlabel("Product")
plt.ylabel("Net Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/product_revenue.png")
plt.show()


#Monthly Revenue Line Chart
plt.figure(figsize=(10, 5))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Net Revenue")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("charts/monthly_revenue.png")
plt.show()


#Category-wise Revenue Chart
plt.figure(figsize=(10, 5))
sns.barplot(
    x=category_sales_sorted.index,
    y=category_sales_sorted.values
)
plt.title("Category-wise Revenue Analysis")
plt.xlabel("Category")
plt.ylabel("Net Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/category_revenue.png")
plt.show()


#Payment Method Revenue Chart
plt.figure(figsize=(10, 5))
sns.barplot(
    x=payment_revenue_sorted.index,
    y=payment_revenue_sorted.values
)
plt.title("Payment Method-wise Revenue")
plt.xlabel("Payment Method")
plt.ylabel("Net Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/payment_revenue.png")
plt.show()


#City-wise Revenue Chart
plt.figure(figsize=(10, 5))
sns.barplot(
    x=city_sales_sorted.index,
    y=city_sales_sorted.values
)
plt.title("city-wise Revenue Analysis")
plt.xlabel("City")
plt.ylabel("Net Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/city_revenue.png")
plt.show()


#Save analysis results
product_sales_sorted.to_csv("outputs/product_revenue.csv")
category_sales_sorted.to_csv("outputs/category_revenue.csv")
city_sales_sorted.to_csv("outputs/city_revenue.csv")
monthly_sales.to_csv("outputs/monthly_revenue.csv")
payment_revenue_sorted.to_csv("outputs/payment_revenue.csv")
print("\nAll analysis result saved successfully!")