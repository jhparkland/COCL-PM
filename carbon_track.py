"""
Real_time database와 연동
"""

from carbon_api import carbon_intensity
from firebase import FirebaseManager
from firebase_admin import db
import json
from gpu import GPUInfo

class CarbonTrack:
    def __init__(self):
        fm = FirebaseManager() # firebase 연결 완료
        gpu_info = GPUInfo(gpu_id=0)
        self.memory_usage = gpu_info.get_gpu_memory_usage()
        self.power_usage = gpu_info.get_gpu_power_usage()

        

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
        
        print(f"GPU Name: {gpu_info.gpu_name}")
        print(f"GPU {gpu_info.gpu_id}의 메모리 사용량: {self.memory_usage} MiB")
        print(f"GPU {gpu_info.gpu_id}의 전력 사용량: {self.power_usage} kWh")
        self.gpu = json.loads(json.dumps({'gpu_info': gpu_info.gpu_name, 'memory_usage': self.memory_usage, 'power_usage': self.power_usage}))
        fm.update(self.gpu)
        

ct = CarbonTrack()
