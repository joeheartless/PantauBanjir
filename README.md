# Real-time Pemantauan Debit Air (infopintuair.py)
---

## Fitur Utama

### Scraping Data Debit Air
- Mengambil data dari [Posko Banjir DSDADKI](https://poskobanjir.dsdadki.web.id)
- Mengambil laporan tinggi muka air dari [BPBD Kota Bekasi](https://bpbd.bekasikota.go.id)
- Parsing HTML table & teks otomatis

### Notifikasi Telegram Otomatis
- Kirim laporan ke grup/akun Telegram jika:
  - Ketinggian air Katulampa ≥ 80 cm
  - Status sungai tidak "normal"
- Laporan mencakup waktu, lokasi, tinggi air, dan status siaga

### Logging ke CSV (setiap 2 jam)
- Format CSV: `tanggal, waktu, pintu air, ketinggian air (cm), status`
- Otomatis membuat file `data_debit_air.csv`
- Cocok untuk analisis historis dan visualisasi data

### Fitur Pendukung
- Anti-spam: hanya kirim notifikasi saat tinggi air katulampa SIAGA 1 ( >= 80 cm )
- Cek status `SIAGA 1`, `SIAGA 2`, `SIAGA 3` berdasarkan tinggi air
- Friendly untuk cronjob atau dijalankan terus-menerus di server

---

## Instalasi & Penggunaan

### 1. Clone Repository
```bash
git clone https://github.com/username/infopintuair.git
cd infopintuair
```
### 2. Dependencies
```
pip install requests beautifulsoup4
```
