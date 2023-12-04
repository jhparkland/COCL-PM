"""
Real_time database와 연동
"""

from carbon_api import carbon_intensity
from firebase import FirebaseManager
from firebase_admin import db
import json
from gpu import GPUInfo
import platform

class CarbonTrack:
    def __init__(self):
        self.fm = FirebaseManager()
        self.gpu_info = GPUInfo(gpu_id=0)
        if platform.machine() == "aarch64" or platform.machine() == "arm64":
            self.gpu_info.gpu_name = "macOS M1 GPU"
            self.memory_usage, self.power_usage = self.gpu_info.get_gpu_m1()

        else:
            self.memory_usage = self.gpu_info.get_gpu_memory_usage()
            self.power_usage = self.gpu_info.get_gpu_power_usage()

        
        self.carbon_intensity = json.loads(json.dumps(carbon_intensity(zone='KR', data='intensity', format='history')))
        print("run __init__ part")
        print(f"GPU Name: {self.gpu_info.gpu_name}")
        print(f"GPU {self.gpu_info.gpu_id}의 메모리 사용량: {self.memory_usage} %")
        print(f"GPU {self.gpu_info.gpu_id}의 전력 사용량: {self.power_usage} kWh")
        data = {'carbon_intensity': self.carbon_intensity['carbon_intensity'], 'gpu_info': self.gpu_info.gpu_name, 'memory_usage': self.memory_usage, 'power_usage': self.power_usage}
        self.gpu = json.loads(json.dumps(data))
        self.fm.update(self.gpu)

    def collect(self):
        if platform.machine() == "aarch64" or platform.machine() == "arm64":
            self.memory_usage, self.power_usage = self.gpu_info.get_gpu_m1()

        else:
            self.memory_usage = self.gpu_info.get_gpu_memory_usage()
            self.power_usage = self.gpu_info.get_gpu_power_usage()

        self.carbon_intensity = json.loads(json.dumps(carbon_intensity(zone='KR', data='intensity', format='history')))
        data = {'carbon_intensity': self.carbon_intensity['carbon_intensity'], 'gpu_info': self.gpu_info.gpu_name, 'memory_usage': self.memory_usage, 'power_usage': self.power_usage}
        self.gpu = json.loads(json.dumps(data))
        self.fm.update(self.gpu)
