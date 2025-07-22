# Ngrok Port Forwarding Setup

## 📋 Deskripsi
Konfigurasi ngrok untuk membuat tunnel agar aplikasi FastAPI dapat diakses dari internet melalui public URL.

## 🚀 Cara Penggunaan

### 1. Install Ngrok
```bash
# Download dari https://ngrok.com/download
# Atau gunakan package manager
# Windows: choco install ngrok
# macOS: brew install ngrok
# Linux: snap install ngrok
```

### 2. Setup Ngrok (Opsional)
```bash
# Daftar akun gratis di https://ngrok.com
# Dapatkan auth token dari dashboard
# Set auth token (untuk fitur premium)
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### 3. Jalankan Aplikasi dengan Ngrok

#### Opsi A: Otomatis (Direkomendasikan)
```bash
cd absensi_app
python start_with_ngrok.py
```

#### Opsi B: Manual
```bash
# Terminal 1: Jalankan FastAPI
cd absensi_app
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Jalankan ngrok
ngrok http 8000
```

#### Opsi C: Ngrok saja
```bash
cd absensi_app
python ngrok_config.py
```

## 🌐 URL yang Tersedia

### Setelah ngrok berjalan:
- **Local URL:** `http://localhost:8000`
- **Public URL:** `https://xxxx-xx-xx-xxx-xx.ngrok.io`
- **Ngrok Web UI:** `http://localhost:4040`

### Dokumentasi API:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 📱 Testing dari Device Lain

### 1. Update Postman Collection
```json
{
  "variable": [
    {
      "key": "base_url",
      "value": "https://xxxx-xx-xx-xxx-xx.ngrok.io"
    }
  ]
}
```

### 2. Test dari Mobile App
- Gunakan public URL ngrok sebagai base URL
- Pastikan endpoint `/auth/login` berfungsi
- Test upload gambar untuk create user

### 3. Test dari Browser
- Akses `https://xxxx-xx-xx-xxx-xx.ngrok.io/docs`
- Test API langsung dari Swagger UI

## ⚙️ Konfigurasi

### File: `ngrok_config.py`
```python
LOCAL_PORT = 8000  # Port aplikasi FastAPI
NGROK_AUTH_TOKEN = None  # Token untuk fitur premium
```

### File: `start_with_ngrok.py`
```python
port = 8000  # Port yang digunakan
```

## 🔧 Troubleshooting

### Error: "ngrok command not found"
```bash
# Pastikan ngrok sudah diinstall dan ada di PATH
# Windows: Restart terminal setelah install
# Linux/macOS: export PATH=$PATH:/path/to/ngrok
```

### Error: "tunnel not found"
```bash
# Cek apakah port 8000 sudah digunakan
# Ganti port di konfigurasi
# Restart ngrok
```

### Error: "connection refused"
```bash
# Pastikan FastAPI sudah berjalan
# Cek firewall settings
# Pastikan host = "0.0.0.0" bukan "127.0.0.1"
```

### Ngrok tidak muncul public URL
```bash
# Tunggu 5-10 detik setelah start
# Cek ngrok web UI di http://localhost:4040
# Restart ngrok jika perlu
```

## 📊 Monitoring

### Ngrok Web Interface
- URL: `http://localhost:4040`
- Fitur: Monitor traffic, inspect requests, view logs

### Logs
```bash
# Ngrok logs muncul di terminal
# FastAPI logs terpisah
# Gunakan Ctrl+C untuk stop
```

## 🔒 Keamanan

### Perhatian:
- **Public URL ngrok dapat diakses siapa saja**
- **Jangan gunakan untuk production**
- **Sesuai untuk development dan testing saja**

### Tips Keamanan:
- Gunakan auth token ngrok untuk fitur premium
- Monitor traffic di ngrok web UI
- Hentikan tunnel saat tidak digunakan

## 🎯 Fitur Ngrok

### Free Plan:
- ✅ 1 tunnel per session
- ✅ Random subdomain
- ✅ HTTP/HTTPS support
- ❌ Custom domain
- ❌ Reserved domain

### Paid Plan:
- ✅ Multiple tunnels
- ✅ Custom domain
- ✅ Reserved domain
- ✅ More bandwidth

## 📝 Contoh Penggunaan

### 1. Development Team
```bash
# Developer A menjalankan ngrok
python start_with_ngrok.py

# Developer B test dari device lain
# Gunakan public URL untuk testing
```

### 2. Mobile App Testing
```bash
# Backend developer
python start_with_ngrok.py

# Mobile developer
# Update base URL di app ke public URL ngrok
```

### 3. Demo/Presentasi
```bash
# Presenter
python start_with_ngrok.py

# Audience
# Akses public URL untuk demo live
```

## 🚨 Important Notes

1. **Ngrok URL berubah setiap restart** (free plan)
2. **Tunnel berhenti jika terminal ditutup**
3. **Gunakan untuk development/testing saja**
4. **Monitor traffic untuk keamanan**
5. **Backup konfigurasi jika menggunakan auth token** 