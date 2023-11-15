import firebase_admin
from firebase_admin import credentials, db

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
     # firebase app에 대한 참조 가져오기
        self.dbs = db.reference ('/') # database 서비스에 대한 참조 가져오기


    """
    firebase에 데이터 업데이트
    """
    def update(self, data):
        self.dbs.update(data)
