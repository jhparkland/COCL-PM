import subprocess

class GPUInfo:
    def __init__(self, gpu_id):
        self.gpu_id = gpu_id
        self.default_gpu_usage = None  # Set this if needed
        self.memory_total = self.get_gpu_info()
        print(self.memory_total)
        
    def get_gpu_info(self):
        try:
            # nvidia-smi 명령 실행
            command = "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits"
            result = subprocess.check_output(command, shell=True, universal_newlines=True)

            # 결과 파싱
            lines = result.strip().split('\n')

            gpu_name, self.memory_total = lines[0].strip().split(',')
     
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
        power_draw = float(result.strip()) / 1000.0  # Convert to kW

        if self.default_gpu_usage is not None:
            power_draw -= self.default_gpu_usage

        if power_draw > 0:
            return power_draw
        else:
            return 0.0
