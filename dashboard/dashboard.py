import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Produk E-Commerce",
    page_icon="🛒",
    layout="wide"
)

# Fungsi untuk load data
@st.cache_data(show_spinner=False)
def load_data():
    data_path = Path(__file__).parent / 'main_data.csv'
    df = pd.read_csv(data_path)
    return df

# Fungsi untuk kategorisasi berat
def categorize_weight(weight):
    if weight < 500:
        return 'Ringan (< 500g)'
    elif weight < 2000:
        return 'Sedang (500g - 2kg)'
    elif weight < 5000:
        return 'Berat (2kg - 5kg)'
    else:
        return 'Sangat Berat (> 5kg)'

# Fungsi untuk clustering produk
def product_cluster(row):
    weight = row['product_weight_g']
    volume = row['product_volume_cm3']
    
    if weight < 500 and volume < 1000:
        return 'Cluster A: Ringan & Kompak'
    elif weight < 500 and volume >= 1000:
        return 'Cluster B: Ringan & Besar'
    elif weight >= 500 and weight < 2000 and volume < 5000:
        return 'Cluster C: Sedang & Kompak'
    elif weight >= 500 and weight < 2000 and volume >= 5000:
        return 'Cluster D: Sedang & Besar'
    elif weight >= 2000:
        return 'Cluster E: Berat'
    else:
        return 'Cluster F: Lainnya'

# Load data
df = load_data()

# Preprocessing
df['product_category_name'].fillna('unknown', inplace=True)
df = df.dropna(subset=['product_weight_g', 'product_length_cm', 
                       'product_height_cm', 'product_width_cm'])
if 'product_volume_cm3' not in df.columns:
    df['product_volume_cm3'] = (df['product_length_cm'] * 
                                 df['product_height_cm'] * 
                                 df['product_width_cm'])
if 'weight_category' not in df.columns:
    df['weight_category'] = df['product_weight_g'].apply(categorize_weight)
if 'product_cluster' not in df.columns:
    df['product_cluster'] = df.apply(product_cluster, axis=1)

# Header
st.title("🛒 Dashboard Analisis Produk E-Commerce")
st.markdown("**Analisis dataset produk e-commerce untuk menjawab pertanyaan bisnis**")
st.markdown("---")

# Sidebar
st.sidebar.header("🔧 Filter Data")
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori Produk:",
    options=df['product_category_name'].unique(),
    default=df['product_category_name'].value_counts().head(5).index.tolist()
)

weight_range = st.sidebar.slider(
    "Rentang Berat Produk (gram):",
    min_value=int(df['product_weight_g'].min()),
    max_value=int(df['product_weight_g'].max()),
    value=(0, 10000)
)

# Filter data
if selected_categories:
    filtered_df = df[df['product_category_name'].isin(selected_categories)]
else:
    filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df['product_weight_g'] >= weight_range[0]) & 
    (filtered_df['product_weight_g'] <= weight_range[1])
]

# Metrics
st.header("📊 Statistik Utama")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Produk", f"{len(filtered_df):,}")
with col2:
    st.metric("Total Kategori", f"{filtered_df['product_category_name'].nunique()}")
with col3:
    st.metric("Rata-rata Berat", f"{filtered_df['product_weight_g'].mean():,.0f} g")
with col4:
    st.metric("Rata-rata Foto", f"{filtered_df['product_photos_qty'].mean():.1f}")

st.markdown("---")

# Tab untuk visualisasi
tab1, tab2, tab3 = st.tabs(["📈 Pertanyaan 1: Distribusi Kategori", "📷 Pertanyaan 2: Foto vs Berat", "🎯 Analisis Lanjutan: Clustering"])

with tab1:
    st.header("Pertanyaan 1: Kategori Produk dengan Jumlah Terbanyak")
    st.markdown("**Kategori produk apa yang memiliki jumlah item terbanyak, dan berapa persentase kontribusinya?**")
    
    # Bar Chart - Top 15 Kategori
    st.subheader("Top 15 Kategori Produk")
    top_15 = filtered_df['product_category_name'].value_counts().head(15)
    total_products = len(filtered_df)
    percentages = (top_15 / total_products * 100).round(2)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 0.8, 15))
    bars = ax.barh(range(len(top_15)), top_15.values, color=colors)
    ax.set_yticks(range(len(top_15)))
    ax.set_yticklabels(top_15.index)
    ax.invert_yaxis()
    ax.set_xlabel('Jumlah Produk', fontsize=12)
    ax.set_ylabel('Kategori Produk', fontsize=12)
    ax.set_title('Top 15 Kategori Produk dengan Jumlah Terbanyak', fontsize=14, fontweight='bold')
    
    # Menambahkan label nilai dan persentase
    for i, (bar, value, pct) in enumerate(zip(bars, top_15.values, percentages.values)):
        ax.text(value + 20, i, f'{value:,} ({pct}%)', va='center', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Insight
    st.markdown("---")
    st.subheader("💡 Insight")
    top_category = top_15.index[0]
    top_count = top_15.values[0]
    top_pct = percentages.values[0]
    st.markdown(f"""
    - Kategori **{top_category}** merupakan kategori dengan jumlah produk terbanyak ({top_count:,} produk / {top_pct}%).
    - Top 10 kategori mencakup sekitar **{(top_15.head(10).sum() / total_products * 100):.1f}%** dari total produk.
    - Distribusi produk terkonsentrasi pada kategori rumah tangga dan gaya hidup.
    """)

with tab2:
    st.header("Pertanyaan 2: Tren Jumlah Foto vs Kategori Berat")
    st.markdown("**Bagaimana tren rata-rata jumlah foto produk berdasarkan kategori berat produk?**")
    
    col1, col2 = st.columns(2)
    
    # Definisikan urutan kategori berat
    weight_order = ['Ringan (< 500g)', 'Sedang (500g - 2kg)', 'Berat (2kg - 5kg)', 'Sangat Berat (> 5kg)']
    
    with col1:
        st.subheader("Rata-rata Jumlah Foto per Kategori Berat")
        photo_by_weight = filtered_df.groupby('weight_category')['product_photos_qty'].mean()
        photo_by_weight = photo_by_weight.reindex(weight_order).dropna()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6'][:len(photo_by_weight)]
        bars = ax.bar(range(len(photo_by_weight)), photo_by_weight.values, color=colors, edgecolor='black', linewidth=1.2)
        ax.set_xticks(range(len(photo_by_weight)))
        ax.set_xticklabels(photo_by_weight.index, rotation=15, ha='right')
        ax.set_xlabel('Kategori Berat Produk', fontsize=12)
        ax.set_ylabel('Rata-rata Jumlah Foto', fontsize=12)
        ax.set_title('Rata-rata Jumlah Foto per Kategori Berat', fontsize=14, fontweight='bold')
        
        for bar, value in zip(bars, photo_by_weight.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                    f'{value:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Distribusi Jumlah Produk per Kategori Berat")
        product_count = filtered_df['weight_category'].value_counts()
        product_count = product_count.reindex(weight_order).dropna()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6'][:len(product_count)]
        bars = ax.bar(range(len(product_count)), product_count.values, color=colors, edgecolor='black', linewidth=1.2)
        ax.set_xticks(range(len(product_count)))
        ax.set_xticklabels(product_count.index, rotation=15, ha='right')
        ax.set_xlabel('Kategori Berat Produk', fontsize=12)
        ax.set_ylabel('Jumlah Produk', fontsize=12)
        ax.set_title('Distribusi Jumlah Produk per Kategori Berat', fontsize=14, fontweight='bold')
        
        for bar, value in zip(bars, product_count.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                    f'{value:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # Visualisasi tren
    st.subheader("Tren Rata-rata Berat per Jumlah Foto")
    photo_stats = filtered_df[filtered_df['product_photos_qty'] <= 10].groupby('product_photos_qty').agg({
        'product_weight_g': 'mean',
        'product_id': 'count'
    }).rename(columns={'product_id': 'count'})
    
    fig, ax = plt.subplots(figsize=(12, 5))
    color1 = 'steelblue'
    ax.set_xlabel('Jumlah Foto Produk', fontsize=12)
    ax.set_ylabel('Rata-rata Berat (gram)', color=color1, fontsize=12)
    line1 = ax.plot(photo_stats.index, photo_stats['product_weight_g'], 
                    color=color1, marker='o', linewidth=2, markersize=8, label='Rata-rata Berat')
    ax.tick_params(axis='y', labelcolor=color1)
    ax.set_xticks(photo_stats.index)
    
    ax2 = ax.twinx()
    color2 = 'forestgreen'
    ax2.set_ylabel('Jumlah Produk', color=color2, fontsize=12)
    bars = ax2.bar(photo_stats.index, photo_stats['count'], alpha=0.3, color=color2, label='Jumlah Produk')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    ax.set_title('Tren Rata-rata Berat dan Distribusi Produk per Jumlah Foto', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Insight
    st.markdown("---")
    st.subheader("💡 Insight")
    st.markdown("""
    - Produk dengan kategori **Sangat Berat (> 5kg)** memiliki rata-rata jumlah foto tertinggi.
    - Produk **Ringan (< 500g)** memiliki rata-rata jumlah foto terendah.
    - Tren ini menunjukkan seller memahami bahwa produk besar/berat memerlukan lebih banyak dokumentasi visual.
    - Mayoritas produk berada pada kategori Ringan dan Sedang.
    """)

with tab3:
    st.header("Analisis Lanjutan: Clustering Produk")
    st.markdown("**Mengelompokkan produk berdasarkan karakteristik fisik (berat dan volume)**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi Cluster Produk")
        cluster_counts = filtered_df['product_cluster'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.Set2(np.linspace(0, 1, len(cluster_counts)))
        bars = ax.barh(cluster_counts.index, cluster_counts.values, color=colors, edgecolor='black')
        ax.set_xlabel('Jumlah Produk', fontsize=12)
        ax.set_title('Distribusi Jumlah Produk per Cluster', fontsize=14, fontweight='bold')
        
        total = len(filtered_df)
        for bar, value in zip(bars, cluster_counts.values):
            pct = value / total * 100
            ax.text(value + 50, bar.get_y() + bar.get_height()/2, 
                    f'{value:,} ({pct:.1f}%)', va='center', fontsize=9)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Rata-rata Berat per Cluster")
        cluster_stats = filtered_df.groupby('product_cluster').agg({
            'product_weight_g': 'mean',
            'product_photos_qty': 'mean'
        }).round(2)
        
        clusters = cluster_stats.index.tolist()
        colors = plt.cm.Set2(np.linspace(0, 1, len(clusters)))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(clusters)), cluster_stats['product_weight_g'].values, color=colors, edgecolor='black')
        ax.set_xticks(range(len(clusters)))
        ax.set_xticklabels([c.split(':')[0] for c in clusters], rotation=45, ha='right')
        ax.set_xlabel('Cluster', fontsize=12)
        ax.set_ylabel('Rata-rata Berat (gram)', fontsize=12)
        ax.set_title('Rata-rata Berat Produk per Cluster', fontsize=14, fontweight='bold')
        
        for bar, value in zip(bars, cluster_stats['product_weight_g'].values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                    f'{value:,.0f}g', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # Insight
    st.markdown("---")
    st.subheader("💡 Insight")
    st.markdown("""
    - **Cluster A (Ringan & Kompak)** merupakan cluster terbesar, mencakup produk-produk kecil.
    - **Cluster E (Berat)** memiliki karakteristik fisik terbesar dengan rata-rata berat tertinggi.
    - Clustering ini dapat digunakan untuk optimasi logistik dan strategi penetapan harga pengiriman.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Dashboard Analisis Produk E-Commerce</strong> | Proyek Dicoding</p>
    <p>Created by Shah Firizki Azmi</p>
</div>
""", unsafe_allow_html=True)
