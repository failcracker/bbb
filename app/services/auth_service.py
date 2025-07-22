from app.models.user import UserLogin
from app.utils.jwt_handler import create_access_token
from app.config.firebase import firestore_client
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str):
        # Query Firestore untuk mencari user berdasarkan username
        users = firestore_client.collection("users").where("username", "==", username).stream()
        
        for doc in users:
            user_data = doc.to_dict()
            # Verifikasi password
            if pwd_context.verify(password, user_data["password"]):
                return {"id": doc.id, **user_data}
        return None

    @staticmethod
    def login(user_login: UserLogin):
        user = AuthService.authenticate_user(user_login.username, user_login.password)
        if not user:
            return None
        token = create_access_token({"sub": user["id"], "role": user["role"]})
        return {"access_token": token, "token_type": "bearer", "user": user}
