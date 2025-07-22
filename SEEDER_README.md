# Data Seeder - Absensi Face Recognition

## Deskripsi
Data seeder ini digunakan untuk membuat data admin default pada sistem absensi face recognition. Program ini akan membuat satu user admin dengan kredensial default yang dapat digunakan untuk login pertama kali.

## Fitur
- ✅ Membuat user admin default
- ✅ Password hashing dengan bcrypt
- ✅ Pengecekan duplikasi data
- ✅ Pesan output yang informatif
- ✅ Error handling yang baik

## Cara Penggunaan

### 1. Pastikan Environment Siap
```bash
# Aktifkan virtual environment
cd absensi_app
venv\Scripts\activate  # Windows
# atau
source venv/bin/activate  # Linux/Mac

# Pastikan semua dependencies terinstall
pip install -r requirements.txt
```

### 2. Jalankan Data Seeder
```bash
# Dari direktori absensi_app
python data_seeder.py
```

### 3. Output yang Diharapkan
```
🚀 Memulai Data Seeder untuk Absensi Face Recognition
==================================================
✅ Admin user berhasil dibuat!
📋 Detail Admin:
   - Username: admin
   - Password: admin123
   - Nama: Administrator
   - Role: admin
   - ID: [firebase_document_id]

⚠️  Jangan lupa untuk mengubah password default setelah login pertama!

✅ Seeding selesai!
```

## Data Admin Default

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |
| Nama | `Administrator` |
| Kode Karyawan | `ADM001` |
| Area | `Jakarta` |
| Latitude | `-6.2088` |
| Longitude | `106.8456` |
| Role | `admin` |

## Keamanan
- Password akan di-hash menggunakan bcrypt sebelum disimpan ke database
- Program akan mengecek apakah admin sudah ada sebelum membuat yang baru
- **PENTING**: Ubah password default setelah login pertama kali!

## Troubleshooting

### Error: "Admin user sudah ada dalam database!"
- Admin sudah dibuat sebelumnya
- Tidak perlu menjalankan seeder lagi

### Error: "Error saat membuat admin user"
- Periksa koneksi Firebase
- Pastikan file konfigurasi Firebase ada dan benar
- Periksa permission Firebase

### Error: "Module not found"
- Pastikan virtual environment aktif
- Pastikan semua dependencies terinstall
- Periksa path Python

## Catatan
- Program ini hanya membuat satu user admin
- Data disimpan di Firebase Firestore collection "users"
- Password default adalah `admin123` - **HARUS DIUBAH** setelah login pertama 