import pyrebase

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
        self.config = {
                        'apiKey': os.getenv("APIKEY"),
                        'authDomain': os.getenv("AUTHDOMAIN"),
                        'databaseURL': os.getenv("DATABASEURL"),
                        'serverAccount' : os.getenv("SERVERACCOUNT"),
                        'projectId': os.getenv("PROJECTID"),
                        'storageBucket': os.getenv("STORAGEBUCKET"),
                        'messagingSenderId': os.getenv("MESSAGINGSENDERID"),
                        'appId': os.getenv("APPID"),
                    }
        self.app = pyrebase.initialize_app(self.config) # firebase app에 대한 참조 가져오기
        self.db = self.app.database() # database 서비스에 대한 참조 가져오기
