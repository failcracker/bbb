from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.dependencies import get_current_admin
from app.utils.export_handler import export_absensi_pdf, export_absensi_csv
from typing import Optional
from datetime import date

router = APIRouter()

# Simpan radius di Firestore (collection: settings, doc: absensi)
from app.config.firebase import firestore_client

@router.post("/radius")
def set_radius(radius_meter: int, admin=Depends(get_current_admin)):
    firestore_client.collection("settings").document("absensi").set({"radius_meter": radius_meter}, merge=True)
    return {"radius_meter": radius_meter}

@router.get("/radius")
def get_radius(admin=Depends(get_current_admin)):
    doc = firestore_client.collection("settings").document("absensi").get()
    if doc.exists:
        return doc.to_dict().get("radius_meter", 100)
    return 100

@router.get("/export/pdf")
def export_pdf(admin=Depends(get_current_admin), tanggal: Optional[date] = None):
    pdf_bytes = export_absensi_pdf(tanggal)
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.get("/export/csv")
def export_csv(admin=Depends(get_current_admin), tanggal: Optional[date] = None):
    csv_bytes = export_absensi_csv(tanggal)
    return Response(content=csv_bytes, media_type="text/csv")

@router.post("/face/training")
def train_face(admin=Depends(get_current_admin)):
    # Stub endpoint training wajah (implementasi opsional)
    return {"message": "Training face endpoint (not implemented)"}
