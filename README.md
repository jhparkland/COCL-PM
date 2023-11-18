# COCL-PM
Deep Learning Performance Monitor Development

- [x] 실시간 탄소 집약도 api 키 발급
- [x] 가장 최근 탄소 집약도 불러와 firebase와 연동
- [x] GPU에서 { GPU 정보, RAM 사용률, 전력 소비량, 탄소 배출량 } 추출
- [ ] 기존 gpu_utils의 class에 추가
- [ ] PC별 고유 number를 추적하여 firebase DB에 저장
- [ ] Mac 지원?

## 프로젝트 목표
1. 딥러닝의 모델의 학습이나 연산 수준에서의 전력 소비량을 추적하고 모니터링합니다.    
2. 측정의 단위는 연산자별, 시간별, epoch 혹은 모델의 단계(생성/학습/최적화) 등으로 나누어 질 수 있습니다.
3. 실시간 탄소 집약도(Carbon-Intensity) 데이터를 바탕으로 측정한 전력 소비량을 탄소배출량으로 변환합니다.

## 추가 설명
1. **행렬의 곱셉(matmul)과 나눗셈(division)의 전력 소비량은 높을 수 있음.**   
- 행렬의 곱셈은 많은 계산을 필요로 함. 큰 행렬을 곱하려면 많은 곱셈과 덧셈 연산이 필요함. 이는 프로세서에 높은 부하를 주게 되어 전력 소비가 증가할 수 있음. 큰 행렬을 곱할 시, 캐시 메모리에 모든 데이터를 저장하기 어려울 수 있으며 이로 인해 메모리를 주기적으로 불러오고 저장해햐 하기 때문에 많은 전력을 사용할 수 있음.      
- 행렬의 나눗셈은 역행렬을 계산해야 하기 때문에 행렬의 곱셈보다 더 많은 계산을 필요로 하며 이는 더 큰 전력 소비량을 발생시킴.   
  
2. **합성곱 연산, 풀링, 활성화 함수, Dropout, softmax간의 연산의 전력 소비량을 비교할 수 있음.**   
- 연산들은 딥러닝 신경망의 구성 요소로 각각의 기능과 특성을 가지고 있으며 이들 간의 전력 소비량은 각각 다름. 연산 간의 전력 소비량을 바탕으로 효율적이고 환경적으로 지속 가능한 모델을 개발할 수 있음.   

3. **모델의 크기와 효율성, 하드웨어 가속기에 따라 전력 소비량에 차이가 발생할 수 있음.**
- 모델의 크기와 효율성은 매개변수(parameter)와 관련되어 있음. 큰 모델은 더 많은 매개변수를 가지며 이는 많은 메모리와 계산이 필요하는 의미임. 따라서 모델의 크기가 클수록 더 많은 전력을 소비하게 됨. 또한 매개변수의 사용 및 연산의 효율성은 동일한 작업을 수행하면서도 더 적은 연산과 메모리를 사용한다는 것을 의미함. 따라서 효율적인 모델은 더 적은 전력을 소비함.
- 모델은 CPU, GPU, TPU 등 다양한 하드웨어 가속기에서 실행될 수 있음. 각 가속기에 따라서 모델을 처리하는 방식과 속도가 다름. 예를 들어 GPU는 병렬 처리가 가능하므로 대규모 연산을 빠르게 처리할 수 있으나 더 많은 전력을 소비함.

4. **실시간 탄소 집약도 데이터는 Electricity Maps API를 통해 수집가능함.**
- Electricity Maps 플랫폼에서 (Free tier)무료 제품을 신청하여, API key(auth-token)를 받아야 함.
- 탄소 집약도(Carbon-intensity)는 재생에너지, 화력, 원자력 발전량에 따라 실시간으로 변동되는 값을 가지며, 데이터의 측정 주기는 다양하게 선택하여 수집 가능함.
- 실시간 탄소 집약도(gCO2eq/kWh)와 실시간 전력 소비량(kWh)을 곱하여 실시간 탄소 배출량을 도출 가능함.
  
![Electricity](https://github.com/jhparkland/COCL-PM/assets/80153046/1dad5ad0-6a42-4e53-aa35-3d5caa34f5cf)
- API Doucument : [https://static.electricitymaps.com/api/docs/index.html](https://static.electricitymaps.com/api/docs/index.html)
- Github : [https://github.com/electricitymaps/electricitymaps-contrib](https://github.com/electricitymaps/electricitymaps-contrib)

## 참여 신청 방법

1. issues 탭 클릭
2. new issues 클릭 후 가입신청 템플릿 선택
3. 양식에 맞춰 작성
