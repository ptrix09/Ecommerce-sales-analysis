import pandas as pd
import plotly.express as px
import os

# Paths
raw_data_path = r"C:\Users\bhaga\Desktop\Git projects\Ecommerce sales analysis\data\raw"
charts_path = r"C:\Users\bhaga\Desktop\Git projects\Ecommerce sales analysis\visuals\charts"
os.makedirs(charts_path, exist_ok=True)

# Load datasets
orders = pd.read_csv(os.path.join(raw_data_path, "olist_orders_dataset.csv"))
order_items = pd.read_csv(os.path.join(raw_data_path, "olist_order_items_dataset.csv"))
products = pd.read_csv(os.path.join(raw_data_path, "olist_products_dataset.csv"))
customers = pd.read_csv(os.path.join(raw_data_path, "olist_customers_dataset.csv"))
payments = pd.read_csv(os.path.join(raw_data_path, "olist_order_payments_dataset.csv"))

# 1. Orders by State
orders_state = orders.merge(customers, on="customer_id")
state_counts = orders_state["customer_state"].value_counts().reset_index()
state_counts.columns = ["State", "Orders"]

fig1 = px.bar(state_counts, x="State", y="Orders", title="Orders by State", color="Orders")
fig1.write_html(os.path.join(charts_path, "orders_by_state.html"))

# 2. Sales Over Time
orders_items_sales = orders.merge(order_items, on="order_id")
orders_items_sales["price"] = orders_items_sales["price"].astype(float)
sales_time = orders_items_sales.groupby("order_purchase_timestamp")["price"].sum().reset_index()
sales_time["order_purchase_timestamp"] = pd.to_datetime(sales_time["order_purchase_timestamp"])

fig2 = px.line(sales_time, x="order_purchase_timestamp", y="price", title="Sales Over Time")
fig2.write_html(os.path.join(charts_path, "sales_over_time.html"))

# 3. Payment Type Distribution
payments_type = payments["payment_type"].value_counts().reset_index()
payments_type.columns = ["Payment Type", "Count"]

fig3 = px.pie(payments_type, names="Payment Type", values="Count", title="Payment Type Distribution")
fig3.write_html(os.path.join(charts_path, "payment_type_distribution.html"))

# 4. Average Delivery Time
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
orders["delivery_time_days"] = (orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]).dt.days

fig4 = px.histogram(orders, x="delivery_time_days", nbins=30, title="Average Delivery Time (Days)")
fig4.write_html(os.path.join(charts_path, "average_delivery_time.html"))

# 5. Top Product Categories
order_items_products = order_items.merge(products, on="product_id")
top_categories = order_items_products["product_category_name"].value_counts().head(10).reset_index()
top_categories.columns = ["Category", "Count"]

fig5 = px.bar(top_categories, x="Category", y="Count", title="Top Product Categories", color="Count")
fig5.write_html(os.path.join(charts_path, "top_product_categories.html"))

# 6. Order Status Distribution
status_counts = orders["order_status"].value_counts().reset_index()
status_counts.columns = ["Order Status", "Count"]

fig6 = px.bar(status_counts, x="Order Status", y="Count", title="Order Status Distribution", color="Count")
fig6.write_html(os.path.join(charts_path, "order_status_distribution.html"))

print(f"Charts saved to: {charts_path}")
