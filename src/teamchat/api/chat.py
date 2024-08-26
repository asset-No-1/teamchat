from kafka import KafkaProducer, KafkaConsumer
from json import loads, dumps, dump
import threading
import json
import os


#THREAD_RUNNING = True

def create_data(username, message, end):
    return {'sender': username, 'message': message, 'end': end}

# SENDER
def pchat(chatroom, username):
    sender = KafkaProducer(
        bootstrap_servers = ['172.17.0.1:9092'],
        value_serializer = lambda x: dumps(x).encode('utf-8'),
    )

    try:
        initial_msg = f"User [{username}] has entered the chat!"
        end = False

        data = create_data(username, initial_msg, end)
        sender.send(chatroom, data)
        sender.flush()        

        while True:
            message = ""
            while message == "":
                #print(f"{username}: ", end="")
                message = input()
        
            if message == 'exit':
                message = f"User [{username}] has exited the chatroom."
                end = True

            data = {'sender': username, 'message': message, 'end': end}       
            sender.send(chatroom, value=data)
            sender.flush()

            if end == True:
                print("Exiting chat...")
                return    

    except KeyboardInterrupt:
        print("Encountered keyboard interrupt. Finishing chat...")
        return
    return

    
# RECEIVER
def cchat(chatroom, username):
    receiver = KafkaConsumer(
        chatroom,
        bootstrap_servers = ['172.17.0.1:9092'],
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
        for message in receiver:
            data = message.value
            messages.append(data)
            if data['end'] == True:
                # someone not me has exited
                if data['sender'] != username:
                    print()
                    print(f"User {data['sender']} has exited the chat.")
                    print("Type in 'exit' to also finish the chat.")
                    #print(f"{username}: ", end="")

                #else:
                    #break
                    #return
                else:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(messages, f, ensure_ascii=True, indent=4)
                    return

            elif data['sender'] != username:
                #print()
                print(f"{data['sender']}: {data['message']}")
                #print(f"{username}: ", end="")



        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=True, indent=4)
        print(f"All received messages are saved in {chatroom}_messages.json")

    except KeyboardInterrupt:
        print("Exiting chat...")
        return


# Threading
chatroom = input("Input chatroom name: ")
username = input("Input Username: ")

print()
print(f"[INFO] Initializing chatroom [{chatroom}] for user [{username}]...")

#json file create
with open(f"{chatroom}_messages.json", "r", encoding="utf-8") as f:
    chats = json.load(f)

print(f"[INFO] Initialize complete! Enjoy chatting!")
print()

thread_1 = threading.Thread(target = pchat, args = (chatroom, username))
thread_2 = threading.Thread(target = cchat, args = (chatroom, username))

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()
