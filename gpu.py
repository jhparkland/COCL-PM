import subprocess

class GPUInfo:
    def __init__(self, gpu_id):
        self.gpu_id = gpu_id
        self.default_gpu_usage = None  # Set this if needed

    def get_gpu_memory_usage(self):
        # nvidia-smi command
        command = f"nvidia-smi --id {self.gpu_id} --query-gpu=memory.used --format=csv,noheader,nounits"
        result = subprocess.check_output(command, shell=True, universal_newlines=True)

        # result parsing
        memory_used = int(result.strip())  # in MiB

        return memory_used

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

# 예를 들어 GPU 0번에 대한 정보 가져오기
gpu_info = GPUInfo(gpu_id=0)
memory_usage = gpu_info.get_gpu_memory_usage()
power_usage = gpu_info.get_gpu_power_usage()

print(f"GPU {gpu_info.gpu_id}의 메모리 사용량: {memory_usage} MiB")
print(f"GPU {gpu_info.gpu_id}의 전력 사용량: {power_usage} kW")
