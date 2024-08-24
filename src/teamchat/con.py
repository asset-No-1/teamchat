from kafka import KafkaConsumer, TopicPartition
import os
from json import loads, dumps, load


#경로저장
home_path = os.path.expanduser("~")
FILE_PATH=f'{home_path}/data/movies/year=2021/data.json'
MOVIE_INFO = os.path.join(home_path, 'movie_info.json')


#검색한 영화 정보 저장
def save_movie_info(value):
    with open(MOVIE_INFO, 'a', encoding='utf-8') as f:
        f.write(dumps(value, ensure_ascii=False, indent=4))


#저장된 영화데이터(JSON파일) 읽기
def read_json():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            data = load(f)  # 파일 객체를 사용하여 JSON을 로드
            return data

    return None


#Consumer 설정
consumer = KafkaConsumer(
        "movie",
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        consumer_timeout_ms=5000,
        group_id="movie_data",
        enable_auto_commit=False,
)


#키값을 영화제목을 주기위해 데이터를 담을 빈 딕셔너리 생성
movie_dic = {}
data = read_json()


for i in data:
    movie_dic[i["movieNm"]] = i


#Consumer 실행
try:
    for m in consumer:
        input_data = m.value
        movie_name = input_data.get("MovieName")

        if movie_name in movie_dic:
            value = movie_dic[movie_name]
            save_movie_info(value)
            
            print(f"영화 정보 저장 완료: {movie_name}")
            print(value)
            consumer.commit()

        else:
            print(f"'{movie_name}'에 대한 정보를 찾을 수 없습니다.")
        

except KeyboardInterrupt:
    print("챗봇 종료")


finally:
    consumer.close()

