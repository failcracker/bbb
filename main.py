from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, absensi, admin
import uvicorn

# List origins (domain) yang diizinkan
origins = [
    "https://frontend-mobilefacenet.vercel.app",
    "http://localhost",  # Tambahkan ini untuk development lokal
    "http://localhost:3000", # Contoh jika FE Anda berjalan di port 3000
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode (GET, POST, PUT, dll.)
    allow_headers=["*"],  # Mengizinkan semua header
)

app = FastAPI(title="Absensi Face Recognition API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(absensi.router, prefix="/absensi", tags=["Absensi"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
