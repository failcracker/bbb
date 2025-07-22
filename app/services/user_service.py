from app.config.firebase import firestore_client
from app.models.user import UserCreate, UserOut
from typing import Optional, List

class UserService:
    @staticmethod
    def create_user(user: UserCreate) -> str:
        doc_ref = firestore_client.collection("users").document()
        data = user.dict()
        # Pastikan radius selalu ada (default 100 jika None)
        if data.get("radius") is None:
            data["radius"] = 100.0
        doc_ref.set(data)
        return doc_ref.id

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[UserOut]:
        doc = firestore_client.collection("users").document(user_id).get()
        if doc.exists:
            user_dict = doc.to_dict()
            return UserOut(id=doc.id, **user_dict)
        return None

    @staticmethod
    def get_user_by_username(username: str) -> Optional[UserOut]:
        users = firestore_client.collection("users").where("username", "==", username).stream()
        for doc in users:
            user_dict = doc.to_dict()
            return UserOut(id=doc.id, **user_dict)
        return None

    @staticmethod
    def update_user(user_id: str, user: dict) -> bool:
        doc_ref = firestore_client.collection("users").document(user_id)
        if doc_ref.get().exists:
            doc_ref.update(user)
            return True
        return False

    @staticmethod
    def delete_user(user_id: str) -> bool:
        doc_ref = firestore_client.collection("users").document(user_id)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False

    @staticmethod
    def list_users() -> List[UserOut]:
        users = firestore_client.collection("users").stream()
        result = []
        for doc in users:
            user_dict = doc.to_dict()
            result.append(UserOut(id=doc.id, **user_dict))
        return result
