import pyrebase

class FirebaseManager:
    """
    firebase 연결 매니저
    """

    def __init__(self):
        # Firebase database init
        self.config = {
                        'apiKey': "AIzaSyCIhOSHqDgjbe9LU2x45xByd8g4Y2P18HM",
                        'authDomain': "carbon-friendly-402901.firebaseapp.com",
                        'databaseURL': 'https://carbon-friendly-402901-default-rtdb.firebaseio.com/',
                        'serverAccount' : '../../firebase_SDK.json',
                        'projectId': "carbon-friendly-402901",
                        'storageBucket': "carbon-friendly-402901.appspot.com",
                        'messagingSenderId': "982587361472",
                        'appId': "1:982587361472:web:3c7e267e476bad79674525"
                    }
        self.app = pyrebase.initialize_app(self.config) # firebase app에 대한 참조 가져오기
        self.db = self.app.database() # database 서비스에 대한 참조 가져오기