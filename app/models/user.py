from pydantic import BaseModel, Field
from typing import Literal, Optional

class UserBase(BaseModel):
    username: str
    nama: str
    kode_karyawan: str
    area: str
    latitude: float
    longitude: float
    radius: Optional[float] = None
    role: Literal["admin", "karyawan"]

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
