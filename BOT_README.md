# 🤖 Portfolio Update Bot - Telegram Bot

Bot Telegram untuk memperbarui foto di website portfolio dengan mudah.

## 📋 Fitur

- ✅ Upload foto portfolio
- ✅ Upload dokumentasi magang
- ✅ Otomatis menyimpan dengan timestamp
- ✅ Interface menu interaktif
- ✅ Kontrol akses (opsional)
- ✅ Status monitoring folder

## 🚀 Cara Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Buat Bot di Telegram

1. Buka Telegram dan cari **@BotFather**
2. Kirim perintah `/newbot`
3. Ikuti instruksi untuk memberi nama bot
4. Salin **token** yang diberikan

### 3. Konfigurasi Bot

1. Salin file `.env.example` menjadi `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit file `.env` dan masukkan token bot Anda:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

3. (Opsional) Tambahkan User ID yang diizinkan:
   ```
   ALLOWED_USER_IDS=123456789,987654321
   ```
   
   **Cara mendapatkan User ID Anda:**
   - Buka bot **@userinfobot** di Telegram
   - Bot akan menampilkan User ID Anda

### 4. Jalankan Bot

```bash
python telegram_bot.py
```

Bot siap digunakan! 🎉

## 📱 Cara Menggunakan Bot

1. **Start Bot**
   - Buka bot di Telegram
   - Kirim perintah `/start`

2. **Upload Foto Portfolio**
   - Pilih menu "📸 Upload Foto Portfolio"
   - Kirim foto yang ingin diupload
   - Foto akan tersimpan di folder `foto/`

3. **Upload Dokumentasi Magang**
   - Pilih menu "📂 Upload Dokumentasi Magang"
   - Kirim foto dokumentasi
   - Foto akan tersimpan di folder `dokumentasimagang/`

4. **Cek Status**
   - Pilih menu "📊 Lihat Status"
   - Lihat jumlah foto di setiap folder

## 🎯 Perintah Bot

| Perintah | Deskripsi |
|----------|-----------|
| `/start` | Tampilkan menu utama |
| `/cancel` | Batalkan upload saat ini |
| `/status` | Lihat status folder |

## 📁 Struktur Folder

```
portoku/
├── telegram_bot.py          # File utama bot
├── .env                     # Konfigurasi (jangan diupload ke git)
├── .env.example            # Template konfigurasi
├── requirements.txt        # Dependencies Python
├── foto/                   # Folder foto portfolio (auto-created)
└── dokumentasimagang/      # Folder dokumentasi (auto-created)
```

## 🔒 Keamanan

- **Token Bot**: Jangan share token bot Anda ke siapa pun
- **File .env**: Pastikan `.env` ada di `.gitignore`
- **User ID**: Batasi akses hanya untuk user yang diizinkan

## 🛠️ Troubleshooting

### Bot tidak merespon
- Pastikan token bot benar
- Cek koneksi internet
- Pastikan bot sudah dijalankan dengan `python telegram_bot.py`

### Error "Module not found"
```bash
pip install -r requirements.txt
```

### Foto tidak tersimpan
- Pastikan folder `foto/` dan `dokumentasimagang/` ada
- Cek permission folder
- Bot akan membuat folder otomatis jika belum ada

## 📝 Update Website

Setelah foto diupload melalui bot:

1. **Foto Portfolio**: Foto tersimpan di folder `foto/`
2. **Dokumentasi**: Foto tersimpan di folder `dokumentasimagang/`
3. Update HTML jika perlu menambahkan foto baru ke galeri
4. Refresh website untuk melihat perubahan

## 🚀 Menjalankan Bot 24/7

Untuk menjalankan bot terus menerus:

### Windows (Background Process)
```bash
start /B python telegram_bot.py
```

### Atau gunakan hosting:
- **Heroku** (Free/Paid)
- **Railway** (Free tier available)
- **PythonAnywhere** (Free tier available)
- **VPS** (DigitalOcean, Vultr, dll)

## 📞 Support

Jika ada masalah atau pertanyaan, silakan buat issue atau hubungi developer.

---

Made with ❤️ for Portfolio Management
