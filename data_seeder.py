#!/usr/bin/env python3
"""
Data Seeder untuk Absensi Face Recognition
Membuat data admin default untuk sistem
"""

import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.config.firebase import firestore_client
from app.models.user import UserCreate
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt"""
    return pwd_context.hash(password)

def create_admin_user():
    """Membuat user admin default"""
    
    # Data admin default
    admin_data = {
        "username": "admin",
        "nama": "Administrator",
        "kode_karyawan": "ADM001",
        "area": "Jakarta",
        "latitude": -6.2088,
        "longitude": 106.8456,
        "radius": 100.0,  # Tambahan radius default
        "role": "admin",
        "password": "admin123"  # Password default yang akan di-hash
    }
    
    try:
        # Cek apakah admin sudah ada
        existing_admin = firestore_client.collection("users").where("username", "==", "admin").stream()
        admin_exists = any(doc.exists for doc in existing_admin)
        
        if admin_exists:
            print("❌ Admin user sudah ada dalam database!")
            return False
        
        # Hash password
        hashed_password = hash_password(admin_data["password"])
        
        # Buat user admin
        user_create = UserCreate(
            username=admin_data["username"],
            nama=admin_data["nama"],
            kode_karyawan=admin_data["kode_karyawan"],
            area=admin_data["area"],
            latitude=admin_data["latitude"],
            longitude=admin_data["longitude"],
            radius=admin_data["radius"],
            role=admin_data["role"],
            password=hashed_password
        )
        
        # Simpan ke Firestore
        doc_ref = firestore_client.collection("users").document()
        doc_ref.set(user_create.dict())
        
        # Set juga radius di settings
        firestore_client.collection("settings").document("absensi").set({"radius_meter": admin_data["radius"]}, merge=True)
        
        print("✅ Admin user berhasil dibuat!")
        print(f"📋 Detail Admin:")
        print(f"   - Username: {admin_data['username']}")
        print(f"   - Password: {admin_data['password']}")
        print(f"   - Nama: {admin_data['nama']}")
        print(f"   - Role: {admin_data['role']}")
        print(f"   - ID: {doc_ref.id}")
        print("\n⚠️  Jangan lupa untuk mengubah password default setelah login pertama!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saat membuat admin user: {str(e)}")
        return False

def main():
    """Main function untuk menjalankan seeder"""
    print("🚀 Memulai Data Seeder untuk Absensi Face Recognition")
    print("=" * 50)
    
    try:
        # Buat admin user
        success = create_admin_user()
        
        if success:
            print("\n✅ Seeding selesai!")
        else:
            print("\n❌ Seeding gagal!")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 