import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

all_df = pd.read_csv("dashboard/main_data.csv")

# Fix datetime columns list - it appears to have a duplicate
datetime_columns = ["order_delivered_customer_date", "review_creation_date"]
all_df.sort_values(by="order_delivered_customer_date", inplace=True)
all_df.reset_index(inplace=True, drop=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_delivered_customer_date"].min()
max_date = all_df["order_delivered_customer_date"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/naozumi-nao.png")
    st.write(
    """
    Oleh: **Bima Adityo Kurniawan (naozumi)**
    """
    )
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data based on the date range
# Changed to filter on order_delivered_customer_date to match the date picker
main_df = all_df[(all_df["order_delivered_customer_date"] >= pd.Timestamp(start_date)) & 
                (all_df["order_delivered_customer_date"] <= pd.Timestamp(end_date))]

# Helper function for histogram & KDE
def plot_delivery_distribution(df):
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    
    # Histogram with KDE
    sns.histplot(df["delivery_time"], kde=True, color="steelblue", ax=ax[0])
    ax[0].set_title("Distribusi Waktu Pengiriman")
    ax[0].set_xlabel("Waktu Pengiriman (hari)")
    ax[0].set_ylabel("Frekuensi")
    
    # CDF plot
    count, bins_count = np.histogram(df["delivery_time"], bins=30)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    ax[1].plot(bins_count[1:], cdf, label="CDF", marker=".", color="steelblue")
    ax[1].axhline(y=0.5, color="red", linestyle="--", label="50% pesanan")
    ax[1].axhline(y=0.8, color="green", linestyle="--", label="80% pesanan")
    ax[1].axhline(y=0.95, color="orange", linestyle="--", label="95% pesanan")
    ax[1].set_title("Distribusi Kumulatif Waktu Pengiriman")
    ax[1].set_xlabel("Waktu Pengiriman (hari)")
    ax[1].set_ylabel("Persentase Kumulatif")
    ax[1].legend()
    
    plt.subplots_adjust(hspace=0.5)
    return fig

def compute_correlation(df):
    return df['review_score'].corr(df['delivery_time'])

def create_visualizations(df):
    fig, axes = plt.subplots(3, 1, figsize=(12, 12))
    
    # Boxplot
    sns.boxplot(x='review_score', y='delivery_time', data=df, ax=axes[0])
    axes[0].set_title('Distribusi Waktu Pengiriman per Nilai Ulasan')
    axes[0].set_xlabel('Nilai Ulasan')
    axes[0].set_ylabel('Waktu Pengiriman (hari)')
    
    # Grouped Barplot
    avg_delivery_by_score = df.groupby('review_score')['delivery_time'].mean().reset_index()
    sns.barplot(x='review_score', y='delivery_time', data=avg_delivery_by_score, ax=axes[1])
    axes[1].set_title('Rata-rata Waktu Pengiriman per Nilai Ulasan')
    axes[1].set_xlabel('Nilai Ulasan')
    axes[1].set_ylabel('Rata-rata Waktu Pengiriman (hari)')
    
    # Heatmap
    df['delivery_time_category'] = pd.cut(df['delivery_time'],
                                          bins=[0, 5, 10, 15, 20, 25, 30],
                                          labels=['1-5', '6-10', '11-15', '16-20', '21-25', '26-30'])
    heatmap_data = pd.crosstab(df['review_score'], df['delivery_time_category'])
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt='d', ax=axes[2])
    axes[2].set_title('Distribusi Ulasan berdasarkan Waktu Pengiriman')
    axes[2].set_xlabel('Kategori Waktu Pengiriman (hari)')
    axes[2].set_ylabel('Nilai Ulasan')
    
    plt.tight_layout()
    return fig

# Streamlit UI
st.header("Brazilian E-Commerce Delivery Report Dashboard")
st.title("Analisis Waktu Pengiriman")

# Add date range information
st.write(f"Data ditampilkan untuk periode: **{start_date.strftime('%d %B %Y')}** hingga **{end_date.strftime('%d %B %Y')}**")
st.write(f"Jumlah data dalam rentang waktu: **{len(main_df)}**")

st.subheader("Visualisasi Distribusi Waktu Pengiriman")
# Use main_df (filtered data) instead of all_df
st.pyplot(plot_delivery_distribution(main_df))
st.divider()
st.subheader("Analisis Korelasi antara Nilai Ulasan & Waktu Pengiriman")
# Use main_df (filtered data) instead of all_df
correlation = compute_correlation(main_df)
st.write(f"**Korelasi antara nilai ulasan & waktu pengiriman:** {correlation:.4f}")

# Use main_df (filtered data) instead of all_df
fig = create_visualizations(main_df)
st.pyplot(fig)