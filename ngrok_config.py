#!/usr/bin/env python3
"""
Konfigurasi Ngrok untuk Port Forwarding
Membuat tunnel untuk akses aplikasi dari internet
"""

import subprocess
import time
import requests
import json
import os
from pathlib import Path

class NgrokManager:
    def __init__(self, local_port=8000, ngrok_auth_token=None):
        self.local_port = local_port
        self.ngrok_auth_token = ngrok_auth_token
        self.ngrok_process = None
        self.public_url = None
        
    def start_ngrok(self):
        """Mulai ngrok tunnel"""
        try:
            # Cek apakah ngrok sudah terinstall
            subprocess.run(["ngrok", "version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Ngrok tidak ditemukan!")
            print("📥 Silakan download dan install ngrok dari: https://ngrok.com/download")
            return False
            
        # Set auth token jika ada
        if self.ngrok_auth_token:
            subprocess.run(["ngrok", "config", "add-authtoken", self.ngrok_auth_token], 
                         check=True, capture_output=True)
        
        # Mulai ngrok tunnel
        print(f"🚀 Memulai ngrok tunnel untuk port {self.local_port}...")
        
        try:
            self.ngrok_process = subprocess.Popen(
                ["ngrok", "http", str(self.local_port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Tunggu sebentar agar ngrok siap
            time.sleep(3)
            
            # Ambil public URL
            self.public_url = self.get_public_url()
            
            if self.public_url:
                print(f"✅ Ngrok tunnel berhasil dibuat!")
                print(f"🌐 Public URL: {self.public_url}")
                print(f"🔗 Local URL: http://localhost:{self.local_port}")
                print("\n📋 Informasi:")
                print(f"   - API Base URL: {self.public_url}")
                print(f"   - Web Interface: http://localhost:4040")
                print(f"   - Status: Aktif")
                return True
            else:
                print("❌ Gagal mendapatkan public URL")
                return False
                
        except Exception as e:
            print(f"❌ Error saat menjalankan ngrok: {str(e)}")
            return False
    
    def get_public_url(self):
        """Ambil public URL dari ngrok API"""
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            if response.status_code == 200:
                tunnels = response.json()["tunnels"]
                for tunnel in tunnels:
                    if tunnel["proto"] == "https":
                        return tunnel["public_url"]
            return None
        except Exception:
            return None
    
    def stop_ngrok(self):
        """Hentikan ngrok tunnel"""
        if self.ngrok_process:
            self.ngrok_process.terminate()
            self.ngrok_process.wait()
            print("🛑 Ngrok tunnel dihentikan")
    
    def get_status(self):
        """Cek status ngrok tunnel"""
        if self.ngrok_process and self.ngrok_process.poll() is None:
            return "running"
        return "stopped"

def main():
    """Main function untuk menjalankan ngrok"""
    print("🌐 Ngrok Port Forwarding Manager")
    print("=" * 40)
    
    # Konfigurasi
    LOCAL_PORT = 8000  # Port aplikasi FastAPI
    
    # Auth token (opsional, untuk fitur premium)
    # NGROK_AUTH_TOKEN = "your_ngrok_auth_token_here"
    NGROK_AUTH_TOKEN = None
    
    # Buat instance ngrok manager
    ngrok = NgrokManager(LOCAL_PORT, NGROK_AUTH_TOKEN)
    
    try:
        # Mulai ngrok
        if ngrok.start_ngrok():
            print("\n🎯 Aplikasi siap diakses dari internet!")
            print("💡 Tips:")
            print("   - Gunakan public URL untuk testing dari device lain")
            print("   - Update Postman collection dengan base URL baru")
            print("   - Ngrok akan berhenti jika terminal ditutup")
            print("\n⏹️  Tekan Ctrl+C untuk menghentikan...")
            
            # Tunggu sampai user tekan Ctrl+C
            while True:
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n\n🛑 Menghentikan ngrok...")
        ngrok.stop_ngrok()
        print("✅ Selesai!")

if __name__ == "__main__":
    main() 