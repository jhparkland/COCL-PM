import firebase_admin
from firebase_admin import credentials, db, firestore
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

        self.db = firestore.client()

        print("firebase init success")

        self.cpuid = cpuid.CPUID()
        print("cpuid init success")
        self.encryptor = encryptor.NumberEncryptor()
        self.encrypted_result = self.encryptor.encrypt_number(self.cpuid(0))
        print("encryptor init success")
        # firebase app에 대한 참조 가져오기
        self.dbs = db.reference(f'/{self.encrypted_result}') # database 서비스에 대한 참조 가져오기


    """
    firebase에 데이터 업데이트
    """
    def update(self, data):
        self.dbs.update(data)
        print("firebase update success")

    def post(self, path, data):
        dbs = db.reference(f'/{self.encrypted_result}/{path}')
        dbs.update(data)
        print("firebase push success")

    def getdata(self, local=False):
        if local:
            dbs = db.reference(f'/{self.encrypted_result}/')
        else:
            dbs = db.reference(f'/')
        data = dbs.get()

        if data:
            print("Firebase get success")
            return data
        else:
            print("Firebase get failed")
            return None

if __name__ == "__main__":
    # FirebaseDataLoader 인스턴스 생성
    loader = FirebaseManager()

    data = loader.getdata()

    if data:
        print("Data retrieved:", data)
    else:
        print("Failed to retrieve data from Firebase.")
    # 데이터 변경 이벤트를 수신할 Firestore 컬렉션 경로
    
