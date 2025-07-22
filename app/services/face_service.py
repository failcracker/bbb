import base64
import numpy as np
from typing import List, Tuple
from app.config.firebase import firestore_client
import torch
import cv2
from PIL import Image
import io
import os

# get static this dir
current_dir = os.path.dirname(os.path.abspath(__file__))
MOBILENET_PATH = os.path.join(current_dir, "mobilefacenet_scripted.pt")

class MobileFaceNetModel:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None  # Lazy loading

    def _load_model(self):
        if self.model is None:
            self.model = torch.jit.load(MOBILENET_PATH, map_location=self.device)
            self.model.eval()

    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        # Baca gambar dari bytes, konversi ke RGB, resize ke 112x112
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize((112, 112))
        img = np.array(img).astype(np.float32) / 255.0
        img = (img - 0.5) / 0.5  # Normalisasi [-1, 1]
        img = np.transpose(img, (2, 0, 1))  # HWC ke CHW
        return img

    def extract_embedding(self, image_bytes: bytes) -> List[float]:
        self._load_model()  # Load model jika belum
        img = self.preprocess(image_bytes)
        tensor = torch.from_numpy(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model(tensor)
        return embedding.cpu().numpy().flatten().tolist()

# Lazy loading - model hanya dibuat saat dibutuhkan
_model_instance = None

def get_model():
    global _model_instance
    if _model_instance is None:
        _model_instance = MobileFaceNetModel()
    return _model_instance

def base64_to_bytes(base64_str: str) -> bytes:
    return base64.b64decode(base64_str.split(",")[-1])

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def recognize_face(base64_image: str) -> Tuple[str, float]:
    model = get_model()
    embedding = model.extract_embedding(base64_to_bytes(base64_image))
    # Cari embedding paling mirip di Firestore
    users = firestore_client.collection("users").stream()
    best_id = None
    best_score = -1
    for doc in users:
        user = doc.to_dict()
        if "face_embedding" in user:
            score = cosine_similarity(embedding, user["face_embedding"])
            if score > best_score:
                best_score = score
                best_id = doc.id
    return best_id, best_score

def save_face_embedding(user_id: str, image_input):
    model = get_model()
    # image_input bisa berupa base64 string atau bytes
    if isinstance(image_input, str):
        embedding = model.extract_embedding(base64_to_bytes(image_input))
    else:
        embedding = model.extract_embedding(image_input)
    firestore_client.collection("users").document(user_id).update({"face_embedding": embedding})
    return embedding
