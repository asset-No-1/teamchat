# 영화 정보 검색 기능을 갖춘 Kafka 실시간 채팅 애플리케이션
<img src="https://img.shields.io/badge/Python-3.8-3776AB?style=flat&logo=Python&logoColor=F5F7F8"/>  <img src="https://img.shields.io/badge/Spark-3.5.1-E25A1C?style=flat&logo=apachespark&logoColor=F5F7F8"/>  <img src="https://img.shields.io/badge/ZeppelinSuperset-0.11.1-20A6C9?style=flat&logo=apachesuperset&logoColor=F5F7F8"/>  <img src="https://img.shields.io/badge/Airflow-2.7.0-017CEE?style=flat&logo=apacheairflow&logoColor=F5F7F8"/>  <img src="https://img.shields.io/badge/Kafka-3.8.0-231F20?style=flat&logo=apachekafka&logoColor=F5F7F8"/>

## 목차
- [프로젝트 개요](#프로젝트-개요)
- [기술 스택](#기술-스택)
- [기능](#기능)
- [설치 및 실행방법](#설치-및-실행방법)
- [사용 예시](#사용-예시)
- [Contributors](#Contributors)
- [Contribution](#Contribution)
- [License](#License)
- [문의](#문의)



## 프로젝트 개요
이 프로젝트는 사내 커뮤니케이션을 효율적으로 관리하고 촉진하기 위한 **사내 채팅 애플리케이션**입니다.
이 애플리케이션은 TUI기반으로 구현되었으며 실시간 메시징, 영화검색 챗봇 기능을 제공하여 팀 간의 협업을 강화하고, 조직 내 정보 전달을 용이하게 합니다.

주요 사용 사례는 다음과 같습니다.
- 팀 간 실시간 협업
- 부서 간 소통
- 긴급 공지사항 전달
- 원격 근무 환경에서의 커뮤니케이션
- 지식 공유 및 학습
- 영화검색 챗봇을 이용한 영화정보 탐색

사내 채팅 애플리케이션은 다양한 사용 사례에서 조직 내 커뮤니케이션을 개선하고, 협업의 효율성을 높이는 데 중요한 역할을 합니다. 실시간 소통을 통해 업무의 신속한 진행과 문제 해결, 정보 공유를 지원하며, 이를 통해 전체 조직의 생산성을 극대화할 수 있습니다.


## 기술 스택
- **기능구현**: Python, Apache Kafka
- **데이터 파이프라인**: Apache Airflow
- **데이터 분석**: Apache Spark
- **데이터 시각화**: Apache Zeppelin


## 기능

### 채팅 및 챗봇 기능
이 사내 채팅 애플리케이션은 Kafka를 사용한 실시간 메시징 기능과 curses 기반의 터미널 인터페이스를 제공합니다.
아래는 주요 기능에 대한 설명입니다:

1. 실시간 메시징
- **Kafka Producer & Consumer**


이 애플리케이션은 Kafka를 사용하여 메시지를 주고받습니다. KafkaProducer가 사용자 입력을 전송하고, KafkaConsumer가 이를 수신하여 실시간으로 메시지를 표시합니다.
Topic 기반 메시지 전송: 메시지는 특정 Kafka 토픽(Product)을 통해 전달되며, 같은 토픽에 연결된 모든 소비자가 해당 메시지를 받을 수 있습니다.

2. 터미널 기반 채팅 인터페이스
- **curses 기반 인터페이스**


터미널에서 동작하는 curses 라이브러리를 활용하여 채팅 UI를 제공합니다. 채팅창과 입력창을 별도로 구성하여 사용자의 메시지 입력과 출력을 명확히 구분합니다.
또한, curses는 스크롤 지원으로 채팅 창은 스크롤을 지원하여 이전 메시지를 쉽게 확인할 수 있습니다.

3. 영화 정보 검색 기능
- **JSON 파일 기반 영화 데이터 로드**


애플리케이션 시작 시, 특정 경로에 저장된 JSON 파일들 `*_data.json`을 로드하여 영화 정보를 `movie_dic` 딕셔너리에 저장합니다.
영화 제목 검색: 사용자가 @로 시작하는 메시지를 입력하면, 영화 제목을 추출하고 사전에 저장된 영화 데이터에서 해당 정보를 검색합니다.
유연한 검색: 공백이 포함된 제목을 처리할 수 있으며, 입력된 제목과 사전에 저장된 제목 간의 공백을 제거하여 비교합니다.
이를 통해 사용자는 영화 제목을 다양한 방식으로 입력할 수 있습니다.
결과 출력: 일치하는 영화 정보가 있을 경우 해당 정보를 출력하며, 없을 경우 "영화 정보를 찾을 수 없습니다."라는 메시지를 표시합니다.

4. 메시지 타임스탬프
- **로컬 시간 표시**


모든 메시지는 전송 시점의 로컬 시간을 함께 표시하여, 메시지의 시간 정보를 제공합니다. 이를 통해 사용자는 각 메시지가 언제 전송되었는지 쉽게 확인할 수 있습니다.

5. 종료 관리
- **exit 명령어**


사용자가 exit을 입력하면 채팅이 종료되며, 이 메시지는 컨슈머에게 종료 신호로 전송됩니다. 이후 애플리케이션이 안전하게 종료됩니다.


### 영화 데이터 로드
이 DAG(DAG: Directed Acyclic Graph)는 영화 데이터를 JSON 파일로 저장하고, 해당 데이터의 처리 결과에 따라 성공 또는 실패 알림을 전송하는 일련의 작업을 자동화합니다.


#### 데이터 파이프라인
<img width="1086" alt="스크린샷 2024-08-28 16 30 37" src="https://github.com/user-attachments/assets/42db2ac6-1ade-4ff3-9017-e9e111798c43">


**1. 영화 데이터 수집 및 저장**


외부 API로부터 주어진 연도의 영화 데이터를 수집하여 JSON 파일로 저장합니다. 가상 환경에서 안전하게 Python 코드를 실행하기 위해 PythonVirtualenvOperator를 사용합니다.

**2. 데이터 존재 여부 확인 및 분기**


해당 연도의 데이터 파일이 이미 존재하는지 확인합니다. 파일이 존재하면 삭제 작업을 수행하고, 없으면 새로운 데이터를 저장합니다. 이 작업은 BranchPythonOperator를 통해 분기됩니다.

**3. 파일 삭제**


이미 존재하는 데이터 파일이 있을 경우 이를 삭제하여 중복을 방지하고 최신 데이터를 유지합니다.

**4. 성공 및 실패 알림**


작업 완료 후, 성공 또는 실패 상태에 따라 LINE Notify API를 통해 알림을 전송합니다.

**5. 재시도 및 실행 관리**


작업 실패 시 3초 간격으로 한 번 재시도하며, 지정된 기간 동안 매년 실행되도록 스케줄링되어 있습니다.


### 채팅 로그 데이터 저장
이 DAG는 주기적으로 채팅 로그 데이터를 수집하고, 해당 데이터를 처리한 후, 성공 여부에 따라 알림을 전송하는 자동화된 워크플로우를 제공합니다. 각 작업은 데이터의 존재 여부, 처리 결과에 따라 분기되어 실행됩니다.


**1. 채팅 로그 데이터 수집 및 관리**
데이터 수집: `Spark`를 사용하여 지정된 경로에서 채팅 로그 데이터를 수집하고 JSON 파일로 저장합니다. 수집된 JSON 파일은 Airflow 홈 디렉토리에 저장됩니다.


파일 존재 여부 확인: DAG 실행 시, 먼저 JSON 데이터 파일이 이미 존재하는지 확인합니다. 파일이 존재하면 삭제 작업을 수행하고, 존재하지 않는 경우 데이터 수집 작업을 진행합니다.
데이터 파일 삭제: 기존에 저장된 채팅 로그 JSON 파일이 있을 경우 이를 삭제하여 새로운 데이터를 수집할 수 있도록 준비합니다.


**2. 데이터 처리 및 통계 분석**
채팅 로그 처리: 수집된 채팅 로그 JSON 파일을 읽어들여 통계 분석을 수행하고, 그 결과를 저장합니다. 이 과정은 제플린(Zeppelin)과 같은 데이터 분석 도구를 사용하여 수행됩니다.


프로세스 존재 여부 확인: 통계 처리 결과 파일이 존재하는지 확인하여, 성공 여부에 따라 후속 작업이 결정됩니다.


**3. 조건 분기 및 작업 흐름 제어**
BranchPythonOperator 사용: BranchPythonOperator를 사용하여 조건에 따라 DAG의 실행 흐름을 분기합니다. 데이터 파일의 존재 여부와 처리 결과에 따라 서로 다른 작업이 실행됩니다.


성공 및 실패 알림: 작업의 성공 또는 실패 여부에 따라 알림을 전송합니다. 이 알림은 시스템 챗봇 기능을 사용하여 실시간으로 담당자에게 전송됩니다.


**4. 알림 시스템**
작업 성공 및 실패 알림: 각 주요 작업(데이터 수집, 처리 등)의 성공 또는 실패 여부에 따라 시스템 챗봇을 통해 알림을 전송합니다. 예를 들어, 제플린 통계 보고서가 성공적으로 저장되었는지 여부를 알립니다.


PythonOperator로 알림 전송: PythonOperator를 사용하여 Python 함수(producer_alarm)를 호출하고, 알림 메시지를 `채팅 애플리케이션`에 지정된 형식으로 전송합니다.


## 설치 및 실행방법

### 사전 요구사항
- `python 3.8` 이상이 설치되어 있어야 합니다.
- `java`가 설치되어 있어야 합니다.
- `kafka-python`이 설치되어 있어야 합니다.
```python
pip install kafka-python
```
- [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html)가 설치되어 있어야 합니다.
- [Apache Kafka](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.8.0/kafka_2.13-3.8.0.tgz)가 설치되어 있어야 합니다.
- movie data가 사전에 있어야 합니다.
1. 리포지토리를 클론합니다:
```bash
git clone https://github.com/asset-No-1/airflow_chat.git
```

2. 에어플로우에 접속한 후, "movie_chat" dags를 실행시킵니다.
3. 경로에 파일이 제대로 저장되었는지 확인합니다.

### 채팅 애플리케이션 실행
- 리포지토리를 클론합니다:
```bash
https://github.com/asset-No-1/teamchat.git
```

- Kafka가 설치된 경로로 이동하여 Zookeeper와 Kafka를 실행합니다:
1. Zookeeper 실행
```bash
bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
```

2. Kafka 실행
```bash
bin/kafka-server-start.sh -daemon config/server.properties
```

- 실행파일에서 서버주소를 수정합니다:
```bash
vi src/teamchat/api/chat3.py
```

```python
bootstrap_servers=['서버주소 입력:9092']
```

- 애플리케이션을 시작합니다:
```bash
python src/teamchat/api/chat3.py
```


## 사용 예시
1. 사용자는 [사용자 이름]을 입력 후 채팅방을 참여합니다.
2. 채팅방에서 메시지를 입력하고 실시간으로 팀원들과 소통할 수 있습니다.
3. 채팅방에서 '@'를 입력 후 영화제목을 입력하면 영화 상세정보를 확인할 수 있습니다.
4. `chat3.py`에서 `topic` 을 다르게 하면 새로운 채팅방에서 대화를 할 수 있습니다. (default topic = Product)


## Contributors
- 실시간 채팅 기능 개발: Nicou11, DONGUK777
- 영화 챗봇 기능 개발: rlaehgus97, hamsunwoo
- 채팅 및 영화 챗봇 기능 디버깅: Nicou11, hamsunwoo
- 채팅 데이터 저장 및 저장 알림: rlaehgus97
- 데이터 분석 시각화: DONGUK777


## Contribution
asset-No-1은 Contributor를 언제나 환영합니다. Contribution을 원하시면 다음 단계를 따라주세요:

1. 저장소를 포크합니다.
2. 새로운 브랜치를 생성합니다 (git checkout -b new-feature).
3. 변경 사항을 커밋합니다 (git commit -am 'Add some feature').
4. 브랜치에 푸시합니다 (git push origin new-feature).
5. 새로운 풀 리퀘스트를 생성합니다.
6. 변경 사항에 따라 테스트 업데이트는 필수입니다.


## License
이 애플리케이션은 asset-No-1 라이선스에 따라 라이선스가 부과됩니다.


## 문의
질문이나 제안사항이 있으면 언제든지 연락주세요:

- 이메일: asset-no-1@asset-no-1.com
- GitHub: Nicou11, DONGUK777, rlaehgus97, hamsunwoo
