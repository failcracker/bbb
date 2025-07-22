from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.models.absensi import AbsensiCreate, AbsensiOut
from app.services.absensi_service import AbsensiService
from app.dependencies import get_current_user, get_current_admin
from typing import List, Optional
from datetime import date, datetime, time
from app.services.face_service import recognize_face
from app.utils.location_validator import is_within_radius
from app.config.firebase import firestore_client
import base64

router = APIRouter()

@router.post("/", response_model=str)
def absen(absensi: AbsensiCreate, user=Depends(get_current_user)):
    absensi_data = absensi.dict()
    absensi_data["karyawan_id"] = user["id"]
    absensi_data["tanggal"] = date.today().isoformat()
    absensi_id = AbsensiService.create_absensi(absensi_data)
    return absensi_id

@router.get("/me", response_model=List[AbsensiOut])
def list_my_absensi(user=Depends(get_current_user)):
    return AbsensiService.list_absensi()

@router.get("/", response_model=List[AbsensiOut])
def list_all_absensi(admin=Depends(get_current_admin), tanggal: Optional[date] = None):
    return AbsensiService.list_absensi(tanggal)

@router.get("/{absensi_id}", response_model=AbsensiOut)
def get_absensi(absensi_id: str, user=Depends(get_current_user)):
    absensi = AbsensiService.get_absensi_by_id(absensi_id)
    if not absensi:
        raise HTTPException(status_code=404, detail="Absensi not found")
    return absensi

def is_late(jam_datang: str) -> bool:
    return jam_datang > "08:59:59"

def is_valid_pulang(jam_pulang: str) -> bool:
    return "17:00:00" <= jam_pulang <= "22:00:00"

@router.post("/face", response_model=dict)
def absen_face(
    image_base64: str = Body(..., embed=True),
    latitude: float = Body(...),
    longitude: float = Body(...),
    tipe: str = Body(..., embed=True),  # "datang" atau "pulang"
):
    user_id, score = recognize_face(image_base64)
    if not user_id or score < 0.5:
        raise HTTPException(status_code=401, detail="Face not recognized")
    user_doc = firestore_client.collection("users").document(user_id).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_doc.to_dict()
    radius_doc = firestore_client.collection("settings").document("absensi").get()
    radius = radius_doc.to_dict().get("radius_meter", 100) if radius_doc.exists else 100
    valid_lokasi, distance = is_within_radius(latitude, longitude, user["latitude"], user["longitude"], radius)
    if not valid_lokasi:
        raise HTTPException(status_code=403, detail="Lokasi di luar radius")
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M:%S")
    absensi_ref = firestore_client.collection("absensi")
    # Cek absensi hari ini
    absens_today = list(absensi_ref.where("karyawan_id", "==", user_id).where("tanggal", "==", today).stream())
    absensi_id = None
    absensi_data = None
    if absens_today:
        absensi_id = absens_today[0].id
        absensi_data = absens_today[0].to_dict()
    if tipe == "datang":
        if absensi_data and absensi_data.get("jam_datang"):
            raise HTTPException(status_code=400, detail="Sudah absen datang hari ini")
        terlambat = is_late(now)
        data = {
            "karyawan_id": user_id,
            "tanggal": today,
            "jam_datang": now,
            "status_kehadiran": "hadir",
            "status_lokasi": "valid",
            "terlambat": terlambat,
            "face_valid": True,
        }
        if absensi_id:
            absensi_ref.document(absensi_id).update(data)
        else:
            absensi_ref.add(data)
        return {"user_id": user_id, "score": score, "image": image_base64, "terlambat": terlambat}
    elif tipe == "pulang":
        if not absensi_data or not absensi_data.get("jam_datang"):
            raise HTTPException(status_code=400, detail="Belum absen datang, tidak boleh absen pulang")
        if absensi_data.get("jam_pulang"):
            raise HTTPException(status_code=400, detail="Sudah absen pulang hari ini")
        if not is_valid_pulang(now):
            raise HTTPException(status_code=400, detail="Jam pulang tidak valid")
        data = {"jam_pulang": now}
        absensi_ref.document(absensi_id).update(data)
        return {"user_id": user_id, "score": score, "image": image_base64, "jam_pulang": now}
    else:
        raise HTTPException(status_code=400, detail="Tipe absen tidak valid")
