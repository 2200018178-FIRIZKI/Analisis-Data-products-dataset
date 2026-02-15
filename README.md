# Proyek Analisis Data: E-Commerce Products Dataset 🛒

## Deskripsi
Analisis dataset produk e-commerce untuk mengidentifikasi distribusi kategori produk dan hubungan antara berat produk dengan jumlah foto. Dilengkapi dengan analisis clustering dan dashboard interaktif.

## Struktur Direktori
```
├── dashboard/
│   ├── dashboard.py          # Dashboard Streamlit
│   └── main_data.csv         # Data hasil cleaning
├── Copy_of_Proyek_Analisis_Data.ipynb  # Notebook analisis
├── products_dataset.csv      # Dataset mentah
├── requirements.txt
├── README.md
└── url.txt
```

## Pertanyaan Bisnis
1. Kategori produk apa yang memiliki jumlah item terbanyak, dan berapa persentase kontribusinya?
2. Bagaimana tren rata-rata jumlah foto produk berdasarkan kategori berat?

## Hasil Analisis
| Temuan | Detail |
|--------|--------|
| Kategori terbanyak | **cama_mesa_banho** — 3.029 produk (9.19%) |
| Konsentrasi | Top 10 kategori = **62.96%** total produk |
| Tren foto | Produk lebih berat → lebih banyak foto (Ringan: 2.12, Sangat Berat: 2.40) |
| Clustering | 5 cluster — terbesar **Cluster B (Ringan & Besar)** = 31.8% |

## Setup Environment

```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Aktivasi
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Menjalankan Dashboard

Dashboard di-deploy melalui **Streamlit Community Cloud** dengan langkah:
1. Push proyek ke repository GitHub
2. Login ke [share.streamlit.io](https://share.streamlit.io)
3. Klik **"New app"** → pilih repo, branch `main`, dan file `dashboard/dashboard.py`
4. Klik **"Deploy"**

🔗 **Akses Dashboard:** [https://firizki-ecommerce-analysis.streamlit.app/](https://firizki-ecommerce-analysis.streamlit.app/)

## Menjalankan Notebook

```bash
jupyter notebook Copy_of_Proyek_Analisis_Data.ipynb
```

## Author
**Shah Firizki Azmi** — Dicoding ID: shah-firizki-azmi
