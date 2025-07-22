from fastapi import FastAPI
from app.routers import auth, users, absensi, admin
import uvicorn

app = FastAPI(title="Absensi Face Recognition API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(absensi.router, prefix="/absensi", tags=["Absensi"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)