"""
Real_time database와 연동
"""

from carbon_api import carbon_intensity
from firebase import FirebaseManager
from firebase_admin import db
import json

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
