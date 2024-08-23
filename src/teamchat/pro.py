from kafka import KafkaProducer
import time
import json


p = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
        

)

print("환영합니다!")
print("영화제목을 입력해주세요!")


while True:
    msg = input("MovieName: ")
    if msg == 'exit':
        break

    data = {'MovieName': msg}
    p.send('movie', value=data)

    p.flush()

print("챗봇 종료")


