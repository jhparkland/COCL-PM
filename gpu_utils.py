import time
import subprocess
import pandas as pd


class Check_GPU:
    def __init__(self) -> None:
        # !!!!!!!!!!! Need to Change !!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # undervolting clock rate
        self.under_volting_rate = 1.0

        # DL model name
        self.dl_model = 'VGGNet'

        # GPU device ID 
        self.gpu_id = 0
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        # idle gpu power
        self.default_gpu_usage = None
        self.default_gpu_usage = self.get_gpu_usage()

        # total consumtion, total execute time
        self.total_excution_time = 0.0
        self.total_energy_usage = 0.0

        # gpu min, max frequency (core, memory)
        self.freq_minmax_info = self.get_min_max_freq_info()

        self.cfreq_min = self.freq_minmax_info['MinCoreClock']
        self.cfreq_max = self.freq_minmax_info['MaxCoreClock']

        # setable frequency list
        self.cfreq_list = self.freq_minmax_info['AvailCoreClock']

        # to change frequency
        self.cur_cfreq = self.cfreq_max * self.under_volting_rate

        self.epoch = 0
        self.iter = 0
        self.batch_size = 0
        self.iter_execution_time = 0.0
        self.iter_energy_usage = 0.0
        self.core_freq = 0
        # self.opt_core_freq = 0

        # GPU info 
        self.device_info = self.get_gpu_info()
        print(self.device_info)
        if self.freq_minmax_info:
            print(self.freq_minmax_info)
        print('Default gpu freq :', self.get_gpu_freq_info())
        # setting frequency (not use optimization algorithm(L-BFGS))
        self.cur_cfreq = self.set_gpu_core_clock(int(self.cur_cfreq))

        self.cur_df = pd.DataFrame(columns=['DeviceID', 'DLmodel', 'TimeStamp', 'EpcohIdx', 'IterIdx', 'ExecutionTime', 'Energy', 'ExecutionTimePerData', 'EnergyPerData', 'CoreFreq', 'OtimalCoreFreq'])


        

    # GPU 전력 사용량 측정 함수
    def get_gpu_usage(self):
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


    # GPU 이름 가져오기
    def get_gpu_info(self):
        try:
            # nvidia-smi 명령 실행
            command = "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits"
            result = subprocess.check_output(command, shell=True, universal_newlines=True)

            # 결과 파싱
            lines = result.strip().split('\n')

            gpu_name, memory_total = lines[0].strip().split(',')
            
            return {
                "GPU Name": gpu_name.strip(),
                "Memory Total": memory_total.strip(),
            }
        except Exception as e:
            print("Error:", e)
            return None



    # GPU 최소, 최대 주파수 정보 가져오기
    def get_min_max_freq_info(self):
        try:
            # "nvidia-smi -q -d SUPPORTED_CLOCKS" 명령 실행
            command = "nvidia-smi -q -d SUPPORTED_CLOCKS"
            result = subprocess.check_output(command, shell=True, universal_newlines=True)

            # 결과 문자열에서 "Graphics" 주파수 정보 추출
            graphics_frequencies = []

            # 결과 문자열을 줄 단위로 분할
            lines = result.strip().split('\n')
            in_graphics_section = False
            cnt = 0

            for line in lines:
                # "Supported Clocks" 섹션 진입 여부 확인
                if "Supported Clocks" in line:
                    in_graphics_section = True
                elif in_graphics_section:
                    # "Memory" 주파수 정보가 나오면 루프 종료
                    if "Memory" in line:
                        cnt += 1
                        if cnt > 1:
                            break
                    # "Graphics" 주파수 정보 추출
                    elif "Graphics" in line:
                        # 주파수 값에서 'MHz' 문자를 제거하고 숫자로 변환하여 저장
                        frequency_str = line.split(":")[1].strip().replace('MHz', '')
                        frequency = float(frequency_str)
                        graphics_frequencies.append(frequency)

            # # 추출된 "Graphics" 주파수 리스트 출력
            # print("Graphics Frequencies:", graphics_frequencies)
            return {'MinCoreClock': min(graphics_frequencies), 
                    'MaxCoreClock': max(graphics_frequencies),
                    'AvailCoreClock': graphics_frequencies,
                    }

        except Exception as e:
            print("#Error#:", e)
            return None

    # set {gpu_index} gpu's core clock to {core_clock_freq}
    def set_gpu_core_clock(self, core_clock_freq):
        try:
            # setting command for change gpu core clock
            command = f"nvidia-smi -i {self.gpu_id} --lock-gpu-clocks={core_clock_freq},{core_clock_freq}"

            # nvidia-smi 명령 실행
            subprocess.run(command, shell=True, check=True)
            cur_clock = self.get_gpu_freq_info()

            return cur_clock['CoreClock']

        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return None



    def reset_gpu_core_clock(self):
        try:
            # reset command of gpu core clock
            command = f"nvidia-smi -i {self.gpu_id} --reset-gpu-clocks"

            # nvidia-smi command execute
            subprocess.run(command, shell=True, check=True)

            time.sleep(1000)
            cur_clock = self.get_gpu_freq_info()

            print(f"Core Clock reset to {cur_clock['CoreClock']} MHz ")
            
            return cur_clock['CoreClock']

        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return None



    # 현재 gpu 주파수 측정
    def get_gpu_freq_info(self):
        try:
            # Getting GPU info by nvidia-smi query
            command = "nvidia-smi --query-gpu=clocks.current.memory,clocks.current.graphics --format=csv,noheader,nounits"
            result = subprocess.check_output(command, shell=True, universal_newlines=True)

            # 결과 파싱
            lines = result.strip().split('\n')
            memory_clock, core_clock = map(int, lines[0].strip().split(','))

            return {
                "MemoryClock": memory_clock,
                "CoreClock": core_clock,
            }
        except Exception as e:
            print("Error:", e)
            return None


    # 매 iter 시작마다 호출
    def iter_start(self, e, i, b_size, is_eval=False):
        # epoch, iter info allocate
        self.epoch = e
        self.iter = i
        self.batch_size = b_size
            
        # variable value initailization for current iteration
        self.iter_execution_time = time.time()
        self.iter_energy_usage = 0.0
        self.core_freq = 0
        # self.opt_core_freq = 0
        self.stop = False
        
        prev_time = time.time()
        # 1 while := 0.015s
        while not self.stop:
            cur_time = time.time()
            exec_time = cur_time - prev_time
            # kW * (second / 3600) -> kWh
            self.iter_energy_usage += self.get_gpu_usage() * (exec_time / 3600.0)
            
            prev_time = cur_time
            
            

        
        

    ### append dictionary data of iteration measurement to dataframe
    def iter_end(self):
        # timestamp
        self.stop = True
        timestamp = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(time.time()))
        self.iter_execution_time = time.time() - self.iter_execution_time
        self.total_excution_time += self.iter_execution_time
        self.total_energy_usage += self.iter_energy_usage
        freq_info = self.get_gpu_freq_info()
        self.core_freq = max(self.core_freq, freq_info['CoreClock'])

        row = {'DeviceID': self.device_info['GPU Name'],
            'DLmodel': self.dl_model,
            'TimeStamp': timestamp,
            'EpcohIdx': self.epoch,
            'IterIdx': self.iter,
            'ExecutionTime': self.iter_execution_time,
            'Energy': self.iter_energy_usage,
            'ExecutionTimePerData': self.iter_execution_time / self.batch_size,
            'EnergyPerData': self.iter_energy_usage / self.batch_size,
            'CoreFreq': self.core_freq,
            'TotalExecutionTime': self.total_excution_time,
            'TotalEnergy': self.total_energy_usage,
            # 아직 최적화 알고리즘 구현 X
            'OtimalCoreFreq':None}
        
        # print dictionary data of iteration
        print(f"iter measurement:{row}")

        self.cur_df.loc[len(self.cur_df) + 1] = row

    def save_csv(self):
        # append measurement to total csv
        try:
            total_df = pd.read_csv(f'{int(self.under_volting_rate * 100)}_measurement.csv')
        except Exception:
            total_df = pd.DataFrame(columns=['DeviceID', 'DLmodel', 'TimeStamp', 'EpcohIdx', 'IterIdx', 'ExecutionTime', 'Energy', 'ExecutionTimePerData', 'EnergyPerData', 'CoreFreq', 'OtimalCoreFreq'])
        total_df = pd.concat([total_df, self.cur_df])

        # save csv
        total_df.to_csv(f'{int(self.under_volting_rate * 100)}_measurement.csv', index=False)
        print(total_df.tail(5))
        print(f'measurement saved into {int(self.under_volting_rate * 100)}_measurement.csv ...')

        # for next save
        total_df = None
        self.cur_df = pd.DataFrame(columns=['DeviceID', 'DLmodel', 'TimeStamp', 'EpcohIdx', 'IterIdx', 'ExecutionTime', 'Energy', 'ExecutionTimePerData', 'EnergyPerData', 'CoreFreq', 'OtimalCoreFreq'])

