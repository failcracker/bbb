from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from app.models.user import UserCreate, UserOut
from app.services.user_service import UserService
from app.services.face_service import save_face_embedding, get_model
from app.dependencies import get_current_admin
from typing import List

router = APIRouter()

@router.post("/", response_model=str)
def create_user(
    username: str = Form(...),
    nama: str = Form(...),
    kode_karyawan: str = Form(...),
    area: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    radius: float = Form(100.0),
    role: str = Form(...),
    password: str = Form(...),
    image: UploadFile = File(...),
    admin=Depends(get_current_admin)
):
    # Baca file gambar dan pastikan file ditutup
    try:
        image_bytes = image.file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Gagal membaca file gambar")
    finally:
        try:
            image.file.close()
        except Exception:
            pass
    # Deteksi wajah (jika tidak bisa extract embedding, berarti tidak ada wajah)
    try:
        face_model = get_model()
        embedding = face_model.extract_embedding(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Gambar tidak valid atau wajah tidak terdeteksi: {}".format(str(e)))
    if embedding is None or len(embedding) == 0:
        raise HTTPException(status_code=400, detail="Wajah tidak terdeteksi pada gambar")
    # Buat user
    user = UserCreate(
        username=username,
        nama=nama,
        kode_karyawan=kode_karyawan,
        area=area,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        role=role,
        password=password
    )
    user_id = UserService.create_user(user)
    # Simpan embedding wajah
    save_face_embedding(user_id, image_bytes)
    return user_id

@router.get("/", response_model=List[UserOut])
def list_users(admin=Depends(get_current_admin)):
    return UserService.list_users()

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, admin=Depends(get_current_admin)):
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=bool)
def update_user(user_id: str, user: dict, admin=Depends(get_current_admin)):
    return UserService.update_user(user_id, user)

@router.delete("/{user_id}", response_model=bool)
def delete_user(user_id: str, admin=Depends(get_current_admin)):
    return UserService.delete_user(user_id)
