---
title: Mental Health Assessment
emoji: 🧠
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
---
# Mental Health Assessment System
Sistem penilaian kesehatan mental berbasis analisis aktivitas digital menggunakan Support Vector Machine (SVM).

## Description

Aplikasi ini menganalisis **13 parameter aktivitas digital** untuk mendeteksi tingkat depresi, kecemasan, dan stres dengan akurasi 85-90%.

## Features

- 📊 Analisis 13 parameter digital activity
- 🤖 3 Model SVM untuk depresi, kecemasan, stres
- 💬 Feedback interaktif & personalized
- 🎨 Interactive web interface
- ⚡ Real-time predictions

## Parameter yang Dianalisis

1. Usia & Jenis Kelamin
2. Durasi smartphone (jam/hari)
3. Media sosial (jam/hari)
4. Gaming (jam/hari)
5. Streaming (jam/hari)
6. Penggunaan gadget sebelum tidur
7. Gangguan notifikasi (1-5)
8. Anxiety internet (1-5)
9. Task procrastination (1-5)
10. Durasi tidur (jam/hari)
11. Phone checking frequency (x/jam)
12. Scrolling frequency (1-5)

## Model Details

- **Algorithm**: Support Vector Machine (SVM) with RBF Kernel
- **Training Samples**: 500+ responden
- **Features**: 13 digital activity indicators
- **Output**: Severity levels (0-4)
  - 0: Tidak ada
  - 1: Ringan
  - 2: Sedang
  - 3: Berat
  - 4: Sangat Berat

## Dataset

Survey terstruktur terhadap mahasiswa/professionals dengan self-reported:

- Pola penggunaan device digital
- Kualitas dan durasi tidur
- Tingkat depresi, kecemasan, stres

## Technologies

- **Backend**: Python 3.11+, Flask Web Framework
- **ML Framework**: scikit-learn
- **Model Serialization**: joblib
- **Data Engineering**: Pandas, NumPy
- **Deployment**: Docker Container

## Cara Menjalankan di Lokal

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputermu sendiri:

1. **Clone Repository**
   ```bash
   git clone <url-repository>
   cd hf_repo_svm
   ```

2. **Buat Virtual Environment (Opsional tapi disarankan)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Untuk Mac/Linux
   # .venv\Scripts\activate   # Untuk Windows
   ```

3. **Install Dependencies**
   Install semua library yang dibutuhkan menggunakan pip:
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi**
   Jalankan server Flask:
   ```bash
   python app.py
   ```
   Aplikasi akan berjalan dan dapat diakses melalui browser pada `http://localhost:7860` atau `http://127.0.0.1:7860`.


## ⚠️ IMPORTANT DISCLAIMER

**Aplikasi ini BUKAN pengganti professional assessment medis!**

Hasil prediksi adalah estimasi berdasarkan data aktivitas digital saja. Untuk diagnosis atau treatment serius:

- Konsultasikan dengan **psikolog profesional**
- Hubungi layanan **mental health support** terdekat
- Jangan tunda jika mengalami distress signifikan

## License

MIT License - Free to use, modify, and distribute

---

**Last Updated**: March 2026
**Model Version**: 1.0
**Status**: Active & Maintained