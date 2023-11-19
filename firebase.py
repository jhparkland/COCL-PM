import firebase_admin
from firebase_admin import credentials, db
import cpuid
import encryptor

# .env 파일에서 환경변수 로드
import os
from dotenv import load_dotenv
load_dotenv()


class FirebaseManager:
    """
    firebase 연결 매니저
    """

    def __init__(self):
        # Firebase database init
        self.config = credentials.Certificate('cocl-pm-firebase.json')
        self.app = firebase_admin.initialize_app (self.config, {
            'databaseURL' : 'https://cocl-pm-default-rtdb.firebaseio.com'
        })
        print("firebase init success")

        self.cpuid = cpuid.CPUID()
        print("cpuid init success")
        self.encryptor = encryptor.NumberEncryptor()
        self.encrypted_result = self.encryptor.encrypt_number(self.cpuid(0))
        print("encryptor init success")
        # firebase app에 대한 참조 가져오기
        self.dbs = db.reference (f'/{self.encrypted_result}') # database 서비스에 대한 참조 가져오기


    """
    firebase에 데이터 업데이트
    """
    def update(self, data):
        self.dbs.update(data)
        print("firebase update success")
