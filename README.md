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
└───url.txt
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
1. **Kategori produk apa yang memiliki jumlah item terbanyak dalam dataset e-commerce, dan berapa persentase kontribusinya terhadap total keseluruhan produk?**
2. **Bagaimana tren rata-rata jumlah foto produk berdasarkan kategori berat produk, dan apakah produk yang lebih berat cenderung memiliki lebih banyak foto?**

## Analisis Lanjutan
- **Clustering Produk**: Mengelompokkan produk berdasarkan kombinasi berat dan volume ke dalam 5 cluster untuk optimasi logistik dan strategi penempatan.

---

## Setup Environment

### Menggunakan Anaconda (Recommended)

1. **Buat environment baru:**
```bash
conda create --name ecommerce-analysis python=3.9
```

2. **Aktivasi environment:**
```bash
conda activate ecommerce-analysis
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Menggunakan venv (Python Virtual Environment)

1. **Buat virtual environment:**
```bash
python -m venv venv
```

2. **Aktivasi virtual environment:**

   - **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   - **Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Menggunakan Pipenv

1. **Install pipenv (jika belum ada):**
```bash
pip install pipenv
```

2. **Install dependencies:**
```bash
pipenv install -r requirements.txt
```

3. **Aktivasi shell:**
```bash
pipenv shell
```

---

## Menjalankan Dashboard Streamlit

### Langkah-langkah:

1. **Pastikan environment sudah aktif** (lihat bagian Setup Environment di atas)

2. **Navigasi ke folder dashboard:**
```bash
cd dashboard
```

3. **Jalankan aplikasi Streamlit:**
```bash
streamlit run dashboard.py
```

4. **Buka browser** dan akses URL yang ditampilkan di terminal (default: `http://localhost:8501`)

### Cara Alternatif (tanpa cd ke folder dashboard):
```bash
streamlit run dashboard/dashboard.py
```

---

## Menjalankan Jupyter Notebook

1. **Pastikan environment sudah aktif**

2. **Jalankan Jupyter Notebook:**
```bash
jupyter notebook
```

3. **Buka file `Copy_of_Proyek_Analisis_Data.ipynb`** di browser

---

## Fitur Dashboard
- **Statistik Utama**: Menampilkan total produk, kategori, rata-rata berat, dan rata-rata foto
- **Filter Interaktif**: Filter berdasarkan kategori produk dan rentang berat
- **Pertanyaan 1**: Visualisasi Top 15 kategori produk dengan persentase kontribusi
- **Pertanyaan 2**: Visualisasi tren rata-rata jumlah foto berdasarkan kategori berat
- **Analisis Lanjutan**: Visualisasi clustering produk berdasarkan karakteristik fisik

---

## Hasil Analisis

### Pertanyaan 1: Distribusi Kategori Produk
- Kategori `cama_mesa_banho` merupakan kategori dengan jumlah produk terbanyak (9.3% dari total)
- Top 10 kategori mencakup sekitar 60% dari total produk
- Distribusi terkonsentrasi pada kategori rumah tangga dan gaya hidup

### Pertanyaan 2: Hubungan Foto dengan Berat Produk
- Produk Sangat Berat (> 5kg) memiliki rata-rata jumlah foto tertinggi
- Produk Ringan (< 500g) memiliki rata-rata jumlah foto terendah
- Tren positif: semakin berat produk, semakin banyak foto

### Analisis Lanjutan: Clustering
- Berhasil mengidentifikasi 5 cluster utama produk
- Cluster A (Ringan & Kompak) merupakan cluster terbesar
- Cluster E (Berat) memiliki karakteristik fisik terbesar

---

## Teknologi yang Digunakan
- **Python 3.9+**: Bahasa pemrograman utama
- **Pandas**: Manipulasi dan analisis data
- **NumPy**: Komputasi numerik
- **Matplotlib**: Visualisasi data
- **Streamlit**: Framework dashboard interaktif

---

## Requirements
Lihat file `requirements.txt` untuk daftar lengkap dependencies.

---

## Author
**Shah Firizki Azmi**
- Email: 2200018178@webmail.uad.ac.id
- Dicoding ID: shah-firizki-azmi
