import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Produk E-Commerce",
    page_icon="🛒",
    layout="wide"
)

# Fungsi untuk load data
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
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
df['product_volume_cm3'] = (df['product_length_cm'] * 
                             df['product_height_cm'] * 
                             df['product_width_cm'])
df['weight_category'] = df['product_weight_g'].apply(categorize_weight)
df['product_cluster'] = df.apply(product_cluster, axis=1)

# Header
st.title("🛒 Dashboard Analisis Produk E-Commerce")
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
tab1, tab2, tab3 = st.tabs(["📈 Distribusi Kategori", "🔗 Analisis Korelasi", "🎯 Clustering Produk"])

with tab1:
    st.header("Distribusi Kategori Produk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 15 Kategori Produk")
        top_15 = filtered_df['product_category_name'].value_counts().head(15)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.viridis(np.linspace(0, 0.8, 15))
        bars = ax.barh(range(len(top_15)), top_15.values, color=colors)
        ax.set_yticks(range(len(top_15)))
        ax.set_yticklabels(top_15.index)
        ax.invert_yaxis()
        ax.set_xlabel('Jumlah Produk')
        ax.set_title('Top 15 Kategori Produk')
        
        for i, (bar, value) in enumerate(zip(bars, top_15.values)):
            ax.text(value + 20, i, f'{value:,}', va='center')
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Distribusi Kategori Berat")
        weight_dist = filtered_df['weight_category'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(weight_dist)))
        ax.pie(weight_dist.values, labels=weight_dist.index, autopct='%1.1f%%',
               colors=colors, explode=[0.02]*len(weight_dist))
        ax.set_title('Distribusi Kategori Berat Produk')
        st.pyplot(fig)
        plt.close()

with tab2:
    st.header("Analisis Korelasi: Jumlah Foto vs Karakteristik Fisik")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rata-rata Berat per Jumlah Foto")
        photo_stats = filtered_df[filtered_df['product_photos_qty'] <= 10].groupby('product_photos_qty').agg({
            'product_weight_g': 'mean',
            'product_volume_cm3': 'mean'
        })
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(photo_stats.index, photo_stats['product_weight_g'], color='steelblue', alpha=0.8)
        ax.set_xlabel('Jumlah Foto Produk')
        ax.set_ylabel('Rata-rata Berat (gram)')
        ax.set_title('Rata-rata Berat Produk per Jumlah Foto')
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Heatmap Korelasi")
        corr_cols = ['product_photos_qty', 'product_weight_g', 'product_length_cm', 
                     'product_height_cm', 'product_width_cm', 'product_volume_cm3']
        corr_matrix = filtered_df[corr_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0, 
                    fmt='.3f', ax=ax, square=True,
                    xticklabels=['Foto', 'Berat', 'Panjang', 'Tinggi', 'Lebar', 'Volume'],
                    yticklabels=['Foto', 'Berat', 'Panjang', 'Tinggi', 'Lebar', 'Volume'])
        ax.set_title('Matriks Korelasi')
        st.pyplot(fig)
        plt.close()

with tab3:
    st.header("Clustering Produk Berdasarkan Karakteristik Fisik")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi Cluster")
        cluster_counts = filtered_df['product_cluster'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.Set2(np.linspace(0, 1, len(cluster_counts)))
        bars = ax.barh(cluster_counts.index, cluster_counts.values, color=colors)
        ax.set_xlabel('Jumlah Produk')
        ax.set_title('Distribusi Cluster Produk')
        
        for bar, value in zip(bars, cluster_counts.values):
            ax.text(value + 50, bar.get_y() + bar.get_height()/2, 
                    f'{value:,} ({value/len(filtered_df)*100:.1f}%)', va='center')
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Scatter Plot: Berat vs Volume")
        sample_df = filtered_df.sample(min(2000, len(filtered_df)), random_state=42)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        cluster_colors = {'Cluster A: Ringan & Kompak': 'blue', 
                          'Cluster B: Ringan & Besar': 'green',
                          'Cluster C: Sedang & Kompak': 'orange', 
                          'Cluster D: Sedang & Besar': 'red',
                          'Cluster E: Berat': 'purple',
                          'Cluster F: Lainnya': 'gray'}
        
        for cluster, color in cluster_colors.items():
            cluster_data = sample_df[sample_df['product_cluster'] == cluster]
            if len(cluster_data) > 0:
                ax.scatter(cluster_data['product_weight_g'], cluster_data['product_volume_cm3'],
                           c=color, label=cluster.split(':')[0], alpha=0.6, s=30)
        
        ax.set_xlabel('Berat Produk (gram)')
        ax.set_ylabel('Volume Produk (cm³)')
        ax.set_title('Scatter Plot: Berat vs Volume per Cluster')
        ax.legend(loc='upper right')
        ax.set_xlim(0, 15000)
        ax.set_ylim(0, 100000)
        st.pyplot(fig)
        plt.close()

# Ringkasan Cluster
st.markdown("---")
st.header("📋 Ringkasan Cluster Produk")

cluster_stats = filtered_df.groupby('product_cluster').agg({
    'product_weight_g': 'mean',
    'product_volume_cm3': 'mean',
    'product_photos_qty': 'mean',
    'product_id': 'count'
}).rename(columns={
    'product_id': 'Jumlah Produk',
    'product_weight_g': 'Rata-rata Berat (g)',
    'product_volume_cm3': 'Rata-rata Volume (cm³)',
    'product_photos_qty': 'Rata-rata Foto'
}).round(2)

st.dataframe(cluster_stats, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Dashboard Analisis Produk E-Commerce | Proyek Dicoding</p>
    <p>Created by Shah Firizki Azmi</p>
</div>
""", unsafe_allow_html=True)
