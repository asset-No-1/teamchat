from kafka import KafkaConsumer, TopicPartition
import os
from json import loads, dumps, load
import glob

# 경로 저장
home_path = os.path.expanduser("~")
FILE_PATH = os.path.join(home_path, 'data', 'mov_data', '*_data.json')
MOVIE_INFO = os.path.join(home_path, 'movie_info.json')

#검색한 영화 정보 저장
def save_movie_info(value):
    with open(MOVIE_INFO, 'a', encoding='utf-8') as f:
        f.write(dumps(value, ensure_ascii=False, indent=4))


# 저장된 영화데이터(JSON파일) 읽기
def read_json():
    all_data = []
    # 모든 *_data.json 파일 경로를 찾기
    file_paths = glob.glob(FILE_PATH)
    
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = load(f)  # 파일 객체를 사용하여 JSON을 로드
            all_data.extend(data)  # 모든 데이터를 리스트에 추가

    return all_data

#Consumer 설정
consumer = KafkaConsumer(
        "movies",
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        consumer_timeout_ms=10000,
        auto_offset_reset='latest',
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

