"""
Real_time database와 연동


"""
from .firebase import FirebaseManager
from firebase_admin import db

class CarbonTrack:
    def __init__(self):
        fm = FirebaseManager() # firebase 연결 완료
        