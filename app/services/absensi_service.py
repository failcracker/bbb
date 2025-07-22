from app.config.firebase import firestore_client
from app.models.absensi import AbsensiCreate, AbsensiOut
from typing import Optional, List
from datetime import date

class AbsensiService:
    @staticmethod
    def create_absensi(absensi: dict) -> str:
        doc_ref = firestore_client.collection("absensi").document()
        doc_ref.set(absensi)
        return doc_ref.id

    @staticmethod
    def get_absensi_by_id(absensi_id: str) -> Optional[AbsensiOut]:
        doc = firestore_client.collection("absensi").document(absensi_id).get()
        if doc.exists:
            return AbsensiOut(id=doc.id, **doc.to_dict())
        return None

    @staticmethod
    def get_absensi_by_karyawan_tanggal(karyawan_id: str, tanggal: date) -> Optional[AbsensiOut]:
        absens = firestore_client.collection("absensi") \
            .where("karyawan_id", "==", karyawan_id) \
            .where("tanggal", "==", tanggal.isoformat()) \
            .stream()
        for doc in absens:
            return AbsensiOut(id=doc.id, **doc.to_dict())
        return None

    @staticmethod
    def update_absensi(absensi_id: str, absensi: dict) -> bool:
        doc_ref = firestore_client.collection("absensi").document(absensi_id)
        if doc_ref.get().exists:
            doc_ref.update(absensi)
            return True
        return False

    @staticmethod
    def delete_absensi(absensi_id: str) -> bool:
        doc_ref = firestore_client.collection("absensi").document(absensi_id)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False

    @staticmethod
    def list_absensi(tanggal: Optional[date] = None) -> List[AbsensiOut]:
        query = firestore_client.collection("absensi")
        if tanggal:
            query = query.where("tanggal", "==", tanggal.isoformat())
        absens = query.stream()
        return [AbsensiOut(id=doc.id, **doc.to_dict()) for doc in absens]
