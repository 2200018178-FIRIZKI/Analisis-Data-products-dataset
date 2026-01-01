# Proyek Analisis Data: E-Commerce Products Dataset

## Deskripsi Proyek
Proyek ini merupakan analisis data komprehensif terhadap dataset produk e-commerce. Analisis mencakup eksplorasi data, visualisasi, dan teknik analisis lanjutan berupa clustering produk berdasarkan karakteristik fisik.

## Struktur Direktori
```
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───products_dataset.csv
├───Copy_of_Proyek_Analisis_Data.ipynb
├───README.md
├───requirements.txt
└───url.txt (opsional - jika di-deploy ke Streamlit Cloud)
```

## Dataset
Dataset yang digunakan adalah **E-Commerce Public Dataset** yang berisi informasi produk dengan fitur:
- `product_id`: ID unik produk
- `product_category_name`: Nama kategori produk
- `product_name_lenght`: Panjang nama produk
- `product_description_lenght`: Panjang deskripsi produk
- `product_photos_qty`: Jumlah foto produk
- `product_weight_g`: Berat produk (gram)
- `product_length_cm`: Panjang produk (cm)
- `product_height_cm`: Tinggi produk (cm)
- `product_width_cm`: Lebar produk (cm)

## Pertanyaan Bisnis
1. **Bagaimana distribusi kategori produk dalam dataset, dan kategori mana yang memiliki jumlah produk terbanyak?**
2. **Apakah terdapat hubungan antara jumlah foto produk dengan karakteristik fisik produk (berat dan dimensi)?**

## Analisis Lanjutan
- **Clustering Produk**: Mengelompokkan produk berdasarkan kombinasi berat dan volume ke dalam 5 cluster untuk optimasi logistik dan strategi penempatan.

## Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi
1. Clone atau download repository ini
2. Buka terminal dan navigasi ke direktori proyek
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Menjalankan Dashboard

### Cara 1: Menjalankan di Local
1. Buka terminal dan navigasi ke folder `dashboard`:
```bash
cd dashboard
```

2. Jalankan aplikasi Streamlit:
```bash
streamlit run dashboard.py
```

3. Buka browser dan akses `http://localhost:8501`

### Cara 2: Akses Online (Jika sudah di-deploy)
Kunjungi URL yang tercantum di file `url.txt`

## Fitur Dashboard
- **Statistik Utama**: Menampilkan total produk, kategori, rata-rata berat, dan rata-rata foto
- **Filter Interaktif**: Filter berdasarkan kategori produk dan rentang berat
- **Visualisasi Distribusi**: Top 15 kategori produk dan distribusi kategori berat
- **Analisis Korelasi**: Heatmap korelasi antara jumlah foto dan karakteristik fisik
- **Clustering Produk**: Visualisasi dan ringkasan cluster produk

## Hasil Analisis
1. Kategori `cama_mesa_banho` merupakan kategori dengan jumlah produk terbanyak
2. Terdapat korelasi positif lemah antara jumlah foto dengan karakteristik fisik produk
3. Berhasil mengidentifikasi 5 cluster produk yang dapat digunakan untuk optimasi operasional

## Teknologi yang Digunakan
- **Python**: Bahasa pemrograman utama
- **Pandas**: Manipulasi dan analisis data
- **NumPy**: Komputasi numerik
- **Matplotlib & Seaborn**: Visualisasi data
- **Streamlit**: Framework dashboard interaktif

## Author
**Shah Firizki Azmi**
- Email: ipengi794@gmail.com
- Dicoding ID: shah_firizki_azmi
