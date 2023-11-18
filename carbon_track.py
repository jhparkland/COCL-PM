"""
Real_time database와 연동
"""

from carbon_api import carbon_intensity
from firebase import FirebaseManager
from firebase_admin import db
import json
import hashlib

def encrypt_number(number):
    # 숫자를 문자열로 변환하여 바이트로 인코딩
    number_str = str(number)
    number_bytes = number_str.encode('utf-8')

    # SHA-256 해시 계산
    sha256_hash = hashlib.sha256(number_bytes).hexdigest()

    return sha256_hash

class CarbonTrack:
    def __init__(self):
        fm = FirebaseManager() # firebase 연결 완료

        # carbon intensity data
        self.carbon_intensity = json.loads(json.dumps(carbon_intensity(zone='KR', data='intensity', format='history')))
        if self.carbon_intensity['carbon_intensity'] == None:
            raise Exception("carbon_intensity data is None")
        try:    
            fm.update(self.carbon_intensity)
            print("carbon_intensity data update success")
        except Exception as e:
            print("carbon_intensity data update failed")
            print(e)

ct = CarbonTrack()
