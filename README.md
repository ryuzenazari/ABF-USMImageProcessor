# Aplikasi Peningkatan Kualitas Gambar

Aplikasi web untuk meningkatkan kualitas gambar menggunakan Filter Bilateral Adaptif (ABF) dan Unsharp Mask yang dikembangkan dengan Flask.

## Fitur Utama

- Implementasi dua jenis filter peningkatan kualitas gambar:
  - **Filter Bilateral Adaptif (ABF)** - untuk peningkatan detail dengan preservasi tepi
  - **Unsharp Mask** - untuk penajaman gambar dengan algoritma standar industri
- Deteksi otomatis parameter optimal berdasarkan karakteristik gambar (noise, tepi, tekstur)
- Pengurangan noise (denoising) dengan algoritma Non-Local Means
- Visualisasi histogram RGB untuk analisis distribusi warna
- Antarmuka pengguna yang intuitif dan responsif

## Cara Kerja Filter

### Filter Bilateral Adaptif (ABF)
Filter Bilateral Adaptif menggabungkan kemampuan filter bilateral konvensional dengan adaptasi parameter berdasarkan konten gambar. Filter ini:
1. Menganalisis karakteristik gambar (level noise, tepi, tekstur)
2. Menyesuaikan parameter filter secara otomatis untuk setiap gambar
3. Menerapkan denoising jika terdeteksi noise tinggi
4. Mempertahankan tepi sambil menghaluskan area homogen
5. Meningkatkan kontras lokal untuk hasil yang lebih tajam

### Unsharp Mask
Teknik Unsharp Mask berfungsi dengan:
1. Membuat versi blur dari gambar asli menggunakan Gaussian Blur
2. Menghitung "mask" dengan mengurangkan versi blur dari gambar asli
3. Menambahkan mask ke gambar asli dengan faktor penguat tertentu
4. Secara selektif meningkatkan detail pada kanal luminansi untuk meminimalkan artefak warna

## Instalasi

### Prasyarat
- Python 3.8 atau lebih baru
- pip (package manager Python)

### Langkah-langkah
1. Clone repositori ini:
   ```bash
   git clone https://github.com/yourusername/image-enhancement-app.git
   cd image-enhancement-app
   ```

2. Buat virtual environment Python (opsional tapi direkomendasikan):
   ```bash
   python -m venv venv
   ```

3. Aktifkan virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

5. Jalankan aplikasi:
   ```bash
   python run.py
   ```

6. Buka browser dan akses `http://localhost:5000`

## Penggunaan

1. Pada halaman utama, klik tombol "Pilih Gambar" untuk mengunggah gambar
2. Tunggu sistem memproses gambar dengan kedua filter
3. Pada halaman hasil, anda dapat:
   - Melihat perbandingan gambar asli dan hasil pemrosesan
   - Mengamati histogram RGB untuk analisis warna
   - Mengunduh gambar hasil

## Struktur Proyek

```
image-enhancement-app/
├── app/                  # Folder utama aplikasi Flask
│   ├── static/           # Aset statis (CSS, JS, gambar)
│   │   ├── uploads/      # Menyimpan gambar yang diunggah
│   │   ├── results/      # Menyimpan gambar hasil pemrosesan
│   │   ├── css/          # File stylesheet
│   │   ├── js/           # File JavaScript
│   ├── templates/        # Template HTML Flask
│   │   ├── index.html    # Halaman utama untuk unggah gambar
│   │   ├── result.html   # Halaman hasil dengan perbandingan gambar
│   ├── utils/            # Modul utilitas
│   │   ├── image_processor.py  # Implementasi filter gambar
│   ├── __init__.py       # Inisialisasi aplikasi Flask
│   ├── routes.py         # Definisi rute dan handlers permintaan HTTP
├── requirements.txt      # Dependensi proyek
├── run.py                # File entri untuk menjalankan aplikasi
├── README.md             # Dokumentasi proyek
```

## Teknologi yang Digunakan

- **Flask** - Web framework Python yang ringan
- **OpenCV** - Library computer vision dan pemrosesan gambar
- **NumPy** - Library komputasi numerik untuk Python
- **Pillow** - Library pemrosesan gambar Python yang mudah digunakan
- **Werkzeug** - Utilitas WSGI untuk Python web development
- **Bootstrap** - Framework CSS untuk antarmuka responsif

## Pengembangan Lebih Lanjut

Beberapa ide untuk pengembangan lebih lanjut:
- Menambahkan lebih banyak filter dan algoritma pemrosesan gambar
- Implementasi fitur editing gambar secara manual
- Implementasi API untuk pemrosesan batch
- Penyimpanan dan manajemen histori gambar
- Optimasi kinerja untuk gambar resolusi tinggi

## Lisensi

MIT License 