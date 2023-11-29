import subprocess
import re

def get_gpu_power_metrics():
    command = "sudo powermetrics --sample-count 1 gpu_power --show-process-energy"
    
    # try:
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout
    # except subprocess.CalledProcessError as e:
    #     output = f"Error: {e}\n{e.stderr}"

    return output

def extract_gpu_metrics(output):
    # 정규 표현식 패턴
    residency_pattern = re.compile(r"GPU idle residency:\s+([\d.]+)%")
    power_pattern = re.compile(r"GPU Power:\s+(\d+)\s+mW")

    # 매칭 수행
    residency_match = residency_pattern.search(output)
    power_match = power_pattern.search(output)

    # 결과 추출
    gpu_idle_residency = float(residency_match.group(1)) if residency_match else None
    gpu_power = int(power_match.group(1)) if power_match else None
    gpu_usage = round(100 - idle_residency, 2) if idle_residency is not None else None

    return gpu_usage, gpu_power

# GPU 전력 소모 관련 데이터 출력
gpu_metrics = get_gpu_power_metrics()

# 메모리 사용량 및 전력 사용량 추출
gpu_usage, power_usage = extract_gpu_metrics(gpu_metrics)
# 결과 출력
print("-" * 50)
print(f"GPU Idle Residency: {gpu_usage}%")
print(f"GPU Power Usage: {power_usage} mW")