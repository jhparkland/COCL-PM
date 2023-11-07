import pyrebase

class FirebaseManager:
    """
    firebase 연결 매니저
    """

    def __init__(self):
        # Firebase database init
        self.config = {
                        'apiKey': "",
                        'authDomain': "",
                        'databaseURL': '',
                        'serverAccount' : '',
                        'projectId': "",
                        'storageBucket': "",
                        'messagingSenderId': "",
                        'appId': ""
                    }
        self.app = pyrebase.initialize_app(self.config) # firebase app에 대한 참조 가져오기
        self.db = self.app.database() # database 서비스에 대한 참조 가져오기
