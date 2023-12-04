import firebase_admin
from firebase_admin import credentials, db, firestore
import cpuid
import encryptor

# Loading environment variables from an .env file
import os
from dotenv import load_dotenv
load_dotenv()


class FirebaseManager:
    """
    firebase connection manager
    """

    def __init__(self, json_file_path, database_url):
        # Firebase database init
        self.config = credentials.Certificate(json_file_path)
        self.app = firebase_admin.initialize_app (self.config, {
            'databaseURL' : database_url
        })

        self.db = firestore.client()

        print("firebase init success")

        self.cpuid = cpuid.CPUID()
        print("cpuid init success")
        self.encryptor = encryptor.NumberEncryptor()
        self.encrypted_result = self.encryptor.encrypt_number(self.cpuid(0))
        print("encryptor init success")
        # Get a reference to a firebase app
        self.dbs = db.reference(f'/{self.encrypted_result}') # Get a reference to the database service


    """
    Updating data to firebase
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
