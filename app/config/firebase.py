import firebase_admin
from firebase_admin import credentials, firestore
import os

# get static this dir
current_dir = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(current_dir, "absen-mobilefacenet-firebase-adminsdk-fbsvc-fbc9804711.json"))
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()
