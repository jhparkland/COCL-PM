"""
Integration with Real_time database
"""

from carbon_api import CarbonIntensityAPI
from firebase import FirebaseManager
from firebase_admin import db
import json
from gpu import GPUInfo
import platform

class CarbonTrack:
    def __init__(self, json_file_path, database_url, carbon_api_key):
        self.fm = FirebaseManager(json_file_path, database_url)
        self.gpu_info = GPUInfo(gpu_id=0)
        if platform.machine() == "aarch64" or platform.machine() == "arm64":
            self.gpu_info.gpu_name = "macOS M1 GPU"
            self.memory_usage, self.power_usage = self.gpu_info.get_gpu_m1()

        else:
            self.memory_usage = self.gpu_info.get_gpu_memory_usage()
            self.power_usage = self.gpu_info.get_gpu_power_usage()

        self.carbon_api_key = carbon_api_key
        self.carbon_intensity = json.loads(json.dumps(CarbonIntensityAPI(carbon_api_key).get_carbon_intensity(zone='KR', data='intensity', format='history')))
        print("run __init__ part")
        print(f"GPU Name: {self.gpu_info.gpu_name}")
        print(f"Memory usage of GPU {self.gpu_info.gpu_id}: {self.memory_usage} %")
        print(f"Power usage of GPU {self.gpu_info.gpu_id}: {self.power_usage} kWh")
        data = {'carbon_intensity': self.carbon_intensity['carbon_intensity'], 'gpu_info': self.gpu_info.gpu_name, 'memory_usage': self.memory_usage, 'power_usage': self.power_usage}
        self.gpu = json.loads(json.dumps(data))
        self.fm.update(self.gpu)

    def collect(self):
        if platform.machine() == "aarch64" or platform.machine() == "arm64":
            self.memory_usage, self.power_usage = self.gpu_info.get_gpu_m1()

        else:
            self.memory_usage = self.gpu_info.get_gpu_memory_usage()
            self.power_usage = self.gpu_info.get_gpu_power_usage()

        self.carbon_intensity = json.loads(json.dumps(CarbonIntensityAPI(self.carbon_api_key).get_carbon_intensity(zone='KR', data='intensity', format='history')))
        data = {'carbon_intensity': self.carbon_intensity['carbon_intensity'], 'gpu_info': self.gpu_info.gpu_name, 'memory_usage': self.memory_usage, 'power_usage': self.power_usage}
        self.gpu = json.loads(json.dumps(data))
        self.fm.update(self.gpu)
