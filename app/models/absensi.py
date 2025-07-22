from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class AbsensiBase(BaseModel):
    karyawan_id: str
    tanggal: date
    jam_datang: Optional[str] = None
    jam_pulang: Optional[str] = None
    status_kehadiran: str
    status_lokasi: str
    terlambat: bool = False
    face_valid: bool = False

class AbsensiCreate(BaseModel):
    latitude: float
    longitude: float
    face_embedding: Optional[list[float]] = None
    tipe: str  # "datang" atau "pulang"

class AbsensiOut(AbsensiBase):
    id: Optional[str] = None
