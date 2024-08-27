from kafka import KafkaProducer, KafkaConsumer
from json import loads, dumps, load, JSONDecodeError
import threading
import os


#PRODUCER 설정
def pro_chat(username):
    producer = KafkaProducer(
        bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'),
    )
    

    while True:
        data = input(f'{username}: ')
        
        if data == 'exit':
            # exit 메시지를 전송하여 컨슈머에게 종료 신호를 보냄
            message = {'user': username, 'message': 'exit'}
            producer.send('chat', value=message)
            producer.flush()
            break

        else:
            # 메시지를 JSON으로 보내면서 사용자 이름을 포함시킵니다.
            message = {'user': username, 'message': data}
            producer.send('chat', value=message)
            producer.flush()
    
    print("채팅 종료")


#CONSUMER 설정
def con_chat(username):
    consumer = KafkaConsumer(
        "chat",
        bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        enable_auto_commit=True,
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    try:
        for m in consumer:
            message = m.value

            if message['message'] == 'exit':
                break

            # 수신한 메시지에서 사용자 이름과 메시지를 출력합니다.
            if message['user'] != username:
                print(f"{message['user']}: {message['message']}")

            #if message['user'] != username:
            #  print(f"{message['user']}: {message['message']}")
             #   print(f"나: {message['message']}\n")
            
            
    except KeyboardInterrupt:
        print("Consumer 종료")

    except JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Raw message: {message}")

    except TypeError as e:
        print(f"TypeError: {e}")
        print(f"Raw message: {message}")

    finally:
        consumer.close()

# 각 사용자 이름을 입력받아 PRODUCER와 CONSUMER 실행
username = input("이름: ")

thread_1 = threading.Thread(target = pro_chat, args = (username,))
thread_2 = threading.Thread(target = con_chat, args = (username,))

thread_1.start()
thread_2.start()


thread_1.join()
thread_2.join()
