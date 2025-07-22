#!/usr/bin/env python3
"""
Script untuk menjalankan aplikasi FastAPI dengan ngrok tunnel
"""

import subprocess
import time
import threading
import signal
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from ngrok_config import NgrokManager

class FastAPINgrokRunner:
    def __init__(self, port=8000):
        self.port = port
        self.fastapi_process = None
        self.ngrok_manager = NgrokManager(port)
        self.running = True
        
    def start_fastapi(self):
        """Jalankan aplikasi FastAPI"""
        print("🚀 Menjalankan aplikasi FastAPI...")
        
        try:
            self.fastapi_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "main:app", 
                "--host", "0.0.0.0", 
                "--port", str(self.port),
                "--reload"
            ])
            
            # Tunggu sebentar agar FastAPI siap
            time.sleep(5)
            
            if self.fastapi_process.poll() is None:
                print(f"✅ FastAPI berjalan di http://localhost:{self.port}")
                return True
            else:
                print("❌ FastAPI gagal dijalankan")
                return False
                
        except Exception as e:
            print(f"❌ Error menjalankan FastAPI: {str(e)}")
            return False
    
    def start_ngrok(self):
        """Jalankan ngrok tunnel"""
        print("🌐 Menjalankan ngrok tunnel...")
        return self.ngrok_manager.start_ngrok()
    
    def run(self):
        """Jalankan FastAPI dan ngrok bersamaan"""
        print("🎯 FastAPI + Ngrok Runner")
        print("=" * 40)
        
        # Jalankan FastAPI
        if not self.start_fastapi():
            return
        
        # Jalankan ngrok
        if not self.start_ngrok():
            print("⚠️  Ngrok gagal, aplikasi tetap berjalan di localhost")
        
        print("\n🎉 Sistem siap!")
        print("📋 Endpoint yang tersedia:")
        print(f"   - Local: http://localhost:{self.port}")
        if self.ngrok_manager.public_url:
            print(f"   - Public: {self.ngrok_manager.public_url}")
        print("\n📚 Dokumentasi API:")
        print(f"   - Swagger UI: http://localhost:{self.port}/docs")
        print(f"   - ReDoc: http://localhost:{self.port}/redoc")
        
        print("\n⏹️  Tekan Ctrl+C untuk menghentikan...")
        
        # Setup signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Tunggu sampai dihentikan
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C"""
        print("\n\n🛑 Menghentikan aplikasi...")
        self.running = False
        
        # Hentikan ngrok
        self.ngrok_manager.stop_ngrok()
        
        # Hentikan FastAPI
        if self.fastapi_process:
            self.fastapi_process.terminate()
            self.fastapi_process.wait()
        
        print("✅ Semua proses dihentikan!")
        sys.exit(0)

def main():
    """Main function"""
    runner = FastAPINgrokRunner(port=8000)
    runner.run()

if __name__ == "__main__":
    main() 