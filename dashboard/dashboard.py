import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')


def create_monthly_orders(df):
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    filtered_data = df[df['order_purchase_timestamp'].dt.year.isin([2016, 2017, 2018])]

    filtered_data['month'] = filtered_data['order_purchase_timestamp'].dt.month
    filtered_data['year'] = filtered_data['order_purchase_timestamp'].dt.year

    monthly_data = (
        filtered_data.groupby(['year', 'month'])
        .agg(order_count=('order_id', 'count'), revenue=('payment_value', 'sum'))
        .reset_index()
    )
    return monthly_data

def best_worst_selling_prod(df):
    tot_prod_count = df.groupby("product_category_name_english")["product_id"].count().reset_index()
    tot_prod_count.rename(columns={
        "product_id": "products"
    }, inplace=True)
    tot_prod_count = tot_prod_count.sort_values(by='products', ascending=False)

    return tot_prod_count


def get_review_scores_df(df):
    scores_count = df['review_score'].value_counts().sort_values(ascending=False)
    most_frequent_score = scores_count.idxmax()

    return scores_count, most_frequent_score

def create_payment_type_summary(df):
    agg_payment_type = df.groupby(by=["payment_type"]).agg({
        "order_id": "count"
    }).reset_index()
    agg_payment_type = agg_payment_type.sort_values(by="order_id", ascending=False)

    return agg_payment_type

all_data_df = pd.read_csv("dashboard/all_data.csv")
# all_data_df = pd.read_csv("https://media.githubusercontent.com/rizkaindahp/sub_project_analisis_data/main/dashboard/all_data.csv")


# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_data_df.sort_values(by="order_approved_at", inplace=True)
all_data_df.reset_index(inplace=True)

for col in datetime_cols:
    all_data_df[col] = pd.to_datetime(all_data_df[col])

min_date = all_data_df["order_approved_at"].min()
max_date = all_data_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.markdown("### Rizka Indah Puspita - B244031F")

    st.markdown("<hr style='margin: 15px 0; border-color: #47663B;'>", unsafe_allow_html=True)

    st.markdown("### Contact Me")

    st.markdown(
        """
        - Email: rizkaindahpuspita@gmail.com
        - Github: [rizkaindahp](https://github.com/rizkaindahp)
        - Linkedin: [Rizka Indah Puspita](https://linkedin.com/in/rizka-indah-puspita)
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr style='margin: 15px 0; border-color: #47663B;'>", unsafe_allow_html=True)

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_data_df[(all_data_df["order_approved_at"] >= str(start_date)) & (all_data_df["order_approved_at"] <= str(end_date))]

tot_prod_count = best_worst_selling_prod(main_df)
scores_count, most_frequent_score = get_review_scores_df(main_df)
monthly_orders_df = create_monthly_orders(main_df)
payment_type_summary = create_payment_type_summary(main_df)

# Title
# st.header("E-Commerce Public Dashboard")
# Header
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='color: #47663B;'>E-Commerce Public Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Monthly Order 
# ================= Monthly Order Count (2016-2018) =================
st.subheader("Monthly Purchase Order (2016-2018)")

fig, ax = plt.subplots(figsize=(12, 8))

for year in [2016, 2017, 2018]:
    # Filter data untuk setiap tahun
    yearly_data = monthly_orders_df[monthly_orders_df['year'] == year]

    # Plot data
    ax.plot(
        yearly_data['month'],
        yearly_data['order_count'],
        marker='o',
        label=f'Order Count {year}'
    )

# Tambahkan detail grafik
ax.set_title("Monthly Purchase Order Count (2016-2018)", fontsize=14)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Purchase Order Count", fontsize=12)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.legend(title="Year")
ax.grid(alpha=0.5)
plt.tight_layout()

st.pyplot(fig)

st.markdown("<hr style='margin: 15px 0; border-color: #47663B;'>", unsafe_allow_html=True)

# Order Items
# ================= Best and Worst Selling Products ====================
st.subheader("Best and Worst Selling Products")

# Aggregating product sales
tot_order_product_df = all_data_df.groupby("product_category_name_english")["product_id"].count().reset_index()
tot_order_product_df = tot_order_product_df.rename(columns={"product_id": "products"})

# Top 10 Products
top_10_product = tot_order_product_df.sort_values(by="products", ascending=False).head(10)

# Bottom 10 Products
bottom_10_product = tot_order_product_df.sort_values(by="products", ascending=True).head(10)

# Plotting Top and Bottom Products
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 8))  

# Color palettes
top_colors = ['#72BCD4'] + ['#D3D3D3'] * (len(top_10_product) - 1)  # Highlight the top product
bottom_colors = ['#FF6347'] + ['#D3D3D3'] * (len(bottom_10_product) - 1)  # Highlight the lowest product

# Top Products Bar Chart
sns.barplot(data=top_10_product, x='product_category_name_english', y='products', ax=ax[0], palette=top_colors)
ax[0].set_title('Top 10 Best Selling Products')
ax[0].set_xlabel('Product Name')
ax[0].set_ylabel('Total Order')
ax[0].tick_params(axis='x', rotation=45)

# Bottom Products Bar Chart
sns.barplot(data=bottom_10_product, x='product_category_name_english', y='products', ax=ax[1], palette=bottom_colors)
ax[1].set_title('Bottom 10 Worst Selling Products')
ax[1].set_xlabel('Product Name')
ax[1].set_ylabel('Total Order')
ax[1].tick_params(axis='x', rotation=45)

# Adjust layout
plt.tight_layout()
st.pyplot(fig)

st.markdown("<hr style='margin: 15px 0; border-color: #47663B;'>", unsafe_allow_html=True)

# ============  Customer Ratings Distribution =============
st.subheader("Customer Review Rating Score Patterns")

# Count review scores
score_review_count = all_data_df['review_score'].value_counts().sort_values(ascending=False)

# Bar colors for ratings
bar_colors = ["#EAEAEA", "#EAEAEA", "#EAEAEA", "#EAEAEA", "#4C8BF5"]

# Plotting Customer Ratings
fig = plt.figure(figsize=(10, 5))
sns.barplot(x=score_review_count.index, y=score_review_count.values, palette=bar_colors)

plt.title("Distribution of Review Ratings Across Products", fontsize=15)
plt.xlabel("Rating", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.xticks(fontsize=12)
plt.tight_layout()
st.pyplot(fig)

st.markdown("<hr style='margin: 15px 0; border-color: #47663B;'>", unsafe_allow_html=True)

# Payment Type
# ================== Payment Type Distribution =================
st.subheader("Distribution of Orders by Payment Method")

fig, ax = plt.subplots(figsize=(10, 5))

# Bar Chart
# ax.bar(payment_type_summary["payment_type"], payment_type_summary["order_id"], color="#90CAF9")
sns.barplot(
    data=payment_type_summary,
    x="payment_type",
    y="order_id",
    palette="Blues_d",
    ax=ax
)

ax.set_xlabel("Payment Types", fontsize=12)
ax.set_ylabel("Total Order", fontsize=12)
ax.set_title("Orders by Payment Types", fontsize=15)
ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
st.pyplot(fig)
