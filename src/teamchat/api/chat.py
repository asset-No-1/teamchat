from kafka import KafkaProducer, KafkaConsumer
from json import loads, dumps
import threading
import json
import os
import queue

# 동기화용 락
lock = threading.Lock()

def create_data(username, message, end):
    return {'sender': username, 'message': message, 'end': end}

# SENDER: 사용자 입력을 Kafka로 전송
def pchat(chatroom, username):
    producer = KafkaProducer(
        #bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        bootstrap_servers=['172.17.0.1:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8'),
    sender = KafkaProducer(
        bootstrap_servers = ['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        value_serializer = lambda x: dumps(x).encode('utf-8'),
    )

    try:
        initial_msg = f"User [{username}] has entered the chat!"
        end = False

        data = create_data(username, initial_msg, end)
        producer.send(chatroom, value=data)
        producer.flush()

        while True:
            message = "" 
            while message == "":
                message = input()

            if message == 'exit':
                message = f"User [{username}] has exited the chatroom."
                end = True

            data = create_data(username, message, end)
            producer.send(chatroom, value=data)
            producer.flush()

            if end:
                print("Exiting chat...")
                return

    except KeyboardInterrupt:
        print("Encountered keyboard interrupt. Finishing chat...")
        return

# RECEIVER: Kafka에서 메시지를 받아 출력
def cchat(chatroom, username):
    consumer = KafkaConsumer(
        chatroom,
        #bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        bootstrap_servers=['172.17.0.1:9092'],
        enable_auto_commit=True,
        value_deserializer=lambda x: loads(x.decode('utf-8'))
        bootstrap_servers = ['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        enable_auto_commit = True,
        value_deserializer = lambda x: loads(x.decode('utf-8'))
    )

    file_path = f"{chatroom}_messages.json"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
    else:
        messages = []

    try:
        for message in consumer:
            data = message.value
            with lock:
                messages.append(data)
                if data['end']:
                    if data['sender'] != username:
                        print()
                        print(f"User {data['sender']} has exited the chat.")
                        print("Type in 'exit' to also finish the chat.")
                    else:
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(messages, f, ensure_ascii=True, indent=4)
                        return
                elif data['sender'] != username:
                    print()
                    print(f"{data['sender']}: {data['message']}")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=True, indent=4)
        print(f"All received messages are saved in {chatroom}_messages.json")

    except KeyboardInterrupt:
        print("Exiting chat...")
        return


# 스레딩
chatroom = input("Input chatroom name: ")
username = input("Input Username: ")

print()
print(f"[INFO] Initializing chatroom [{chatroom}] for user [{username}]...")

>>>>>>> 0746433 (dummy)
print(f"[INFO] Initialize complete! Enjoy chatting!")
print()

thread_1 = threading.Thread(target=pchat, args=(chatroom, username))
thread_2 = threading.Thread(target=cchat, args=(chatroom, username))

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()
