# 사내채팅 애플리케이션
<img src="https://img.shields.io/badge/Python-3.8-3776AB?style=flat&logo=Python&logoColor=F5F7F8"/>


## 목차
- [프로젝트 개요](#프로젝트-개요)
- [기능](#기능)
- [기술 스택](#기술-스택)
- [설치 및 실행방법](#설치-및-실행방법)
- [사용 예시](#사용-예시)
- [Contributors](#Contributors)
- [Contribution](#Contribution)
- [License](#License)
- [문의](#문의)



## 프로젝트 개요
이 프로젝트는 사내 커뮤니케이션을 효율적으로 관리하고 촉진하기 위한 **사내 채팅 애플리케이션**입니다.
이 애플리케이션은 실시간 메시징, 영화검색 챗봇 기능을 제공하여 팀 간의 협업을 강화하고, 조직 내 정보 전달을 용이하게 합니다.

주요 사용 사례는 다음과 같습니다.
- 팀 간 실시간 협업
- 부서 간 소통
- 긴급 공지사항 전달
- 원격 근무 환경에서의 커뮤니케이션
- 지식 공유 및 학습
- 영화검색 챗봇을 이용한 영화정보 탐색

사내 채팅 애플리케이션은 다양한 사용 사례에서 조직 내 커뮤니케이션을 개선하고, 협업의 효율성을 높이는 데 중요한 역할을 합니다. 실시간 소통을 통해 업무의 신속한 진행과 문제 해결, 정보 공유를 지원하며, 이를 통해 전체 조직의 생산성을 극대화할 수 있습니다.



## 기능
- **실시간 메시징**: 팀원 간의 즉각적인 커뮤니케이션을 지원합니다.
- **그룹 채팅**: 여러 사용자가 참여할 수 있는 채팅 그룹을 생성하여 협업을 강화합니다. (개발중)
- **영화검색 기능**: 영화챗봇을 이용하여 영화정보를 검색할 수 있습니다.



## 기술 스택
- **기능구현**: Python, Apache Kafka
- **데이터 파이프라인**: Apache Airflow
- **데이터 분석**: Apache Spark
- **데이터 시각화**: Apache Zeppelin



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
