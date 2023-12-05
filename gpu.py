import subprocess
import re
import platform

class GPUInfo:
    def __init__(self, gpu_id):
        self.gpu_id = gpu_id
        self.gpu_name = None
        self.default_gpu_usage = None  # Set this if needed
        if platform.machine() == "aarch64" or platform.machine() == "arm64":
            pass
        else:
            self.memory_total = self.get_gpu_info()
        
    def get_gpu_info(self):
        try:
            command = "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits"
            result = subprocess.check_output(command, shell=True, universal_newlines=True)

            lines = result.strip().split('\n')

            self.gpu_name, self.memory_total = lines[0].strip().split(',')
     
            return int(self.memory_total.strip())
            '''{
                "GPU Name": gpu_name.strip(),
                "Memory Total": memory_total.strip(),
            }'''
        except Exception as e:
            print("Error:", e)
            return None

    def get_gpu_memory_usage(self):
        # nvidia-smi command
        command = f"nvidia-smi --id {self.gpu_id} --query-gpu=memory.used --format=csv,noheader,nounits"
        result = subprocess.check_output(command, shell=True, universal_newlines=True)

        # result parsing
        memory_used = int(result.strip())  # in MiB

        return memory_used / int(self.memory_total)

    def get_gpu_power_usage(self):
        # nvidia-smi command
        command = f"nvidia-smi --id {self.gpu_id} --query-gpu=power.draw --format=csv,noheader,nounits"
        result = subprocess.check_output(command, shell=True, universal_newlines=True)

        # result parsing
        power_draw = float(result.strip()) / 100.0  # Convert to kW

        if self.default_gpu_usage is not None:
            power_draw -= self.default_gpu_usage

        if power_draw > 0:
            return power_draw
        else:
            return 0.0

    def get_gpu_m1(self):
        command = "sudo powermetrics --sample-count 1 gpu_power --show-process-energy"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        residency_pattern = re.compile(r"GPU idle residency:\s+([\d.]+)%")
        power_pattern = re.compile(r"GPU Power:\s+(\d+)\s+mW")

        residency_match = residency_pattern.search(output)
        power_match = power_pattern.search(output)

        idle_residency = float(residency_match.group(1)) if residency_match else None
        gpu_power = int(power_match.group(1)) if power_match else None
        gpu_usage = round(100 - idle_residency, 2) if idle_residency is not None else None

        return gpu_usage, gpu_power*0.1
