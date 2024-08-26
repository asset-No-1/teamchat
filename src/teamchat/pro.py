from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
        

)

while True:
    movie_title = input("MovieName: ")
    if movie_title == 'exit':
        break

    data = {'MovieName': movie_title}
    producer.send('movies', value=data)

    producer.flush()

print("챗봇 종료")


