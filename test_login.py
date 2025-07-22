#!/usr/bin/env python3
"""
Test script untuk memverifikasi login admin
"""

import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.services.auth_service import AuthService
from app.models.user import UserLogin

def test_admin_login():
    """Test login dengan kredensial admin"""
    
    print("🧪 Testing Admin Login")
    print("=" * 30)
    
    # Test dengan kredensial admin
    admin_login = UserLogin(
        username="admin",
        password="admin123"
    )
    
    try:
        result = AuthService.login(admin_login)
        
        if result:
            print("✅ Login berhasil!")
            print(f"📋 Token: {result['access_token'][:50]}...")
            print(f"👤 User ID: {result['user']['id']}")
            print(f"👤 Username: {result['user']['username']}")
            print(f"👤 Role: {result['user']['role']}")
        else:
            print("❌ Login gagal - kredensial salah atau user tidak ditemukan")
            
    except Exception as e:
        print(f"❌ Error saat login: {str(e)}")

def test_wrong_password():
    """Test login dengan password salah"""
    
    print("\n🧪 Testing Wrong Password")
    print("=" * 30)
    
    wrong_login = UserLogin(
        username="admin",
        password="wrongpassword"
    )
    
    try:
        result = AuthService.login(wrong_login)
        
        if result:
            print("❌ Login berhasil (seharusnya gagal)")
        else:
            print("✅ Login gagal (sesuai ekspektasi)")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_nonexistent_user():
    """Test login dengan user yang tidak ada"""
    
    print("\n🧪 Testing Nonexistent User")
    print("=" * 30)
    
    nonexistent_login = UserLogin(
        username="nonexistent",
        password="anypassword"
    )
    
    try:
        result = AuthService.login(nonexistent_login)
        
        if result:
            print("❌ Login berhasil (seharusnya gagal)")
        else:
            print("✅ Login gagal (sesuai ekspektasi)")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main function untuk menjalankan semua test"""
    print("🚀 Memulai Test Login System")
    print("=" * 50)
    
    try:
        # Test admin login
        test_admin_login()
        
        # Test wrong password
        test_wrong_password()
        
        # Test nonexistent user
        test_nonexistent_user()
        
        print("\n✅ Semua test selesai!")
        
    except Exception as e:
        print(f"❌ Error fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 