from kafka import KafkaProducer, KafkaConsumer
from json import loads, dumps
import threading
import json
import os
import curses

# 동기화용 락
lock = threading.Lock()

def create_data(username, message, end):
    return {'sender': username, 'message': message, 'end': end}

# SENDER: 사용자 입력을 Kafka로 전송
def pchat(stdscr, chatroom, username):
    producer = KafkaProducer(
        #bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        bootstrap_servers=['172.17.0.1:9092'],
        value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'),
    )

    stdscr.clear()
    stdscr.refresh()

    input_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
    input_win.addstr(0, 0, f"{username}: ")
    input_win.refresh() 

    try:
        initial_msg = f"[{username}]님이 입장 했습니다."
        end = False

        data = create_data(username, initial_msg, end)
        producer.send(chatroom, value=data)
        producer.flush()

        while True:
            input_win.clear()
            input_win.addstr(0, 0, f"{username}: ")
            curses.echo()
            message = input_win.getstr().decode('utf-8', errors='ignore')
            #curses.noecho()

            if message == 'exit':
                message = f"[{username}]님이 방을 떠났습니다."
                end = True

            data = create_data(username, message, end)
            producer.send(chatroom, value=data)
            producer.flush()

            if end:
                stdscr.addstr(curses.LINES - 2, 0, "방을 나갑니다.")
                stdscr.refresh()
                return

    except KeyboardInterrupt:
        stdscr.addstr(curses.LINES - 2, 0, "Encountered keyboard interrupt. 방을 나갑니다...")
        stdscr.refresh()
        return

# RECEIVER: Kafka에서 메시지를 받아 출력
def cchat(stdscr, chatroom, username):
    consumer = KafkaConsumer(
        chatroom,
        #bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        bootstrap_servers=['172.17.0.1:9092'],
        enable_auto_commit=True,
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    #file_path = f"{chatroom}_messages.json"
    # 파일 경로 설정
    directory = os.path.expanduser('~/code/teamchat/logs/')
    filename = f"{chatroom}_messages.json"
    file_path = os.path.join(directory, filename)

    # 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
    else:
        messages = []

    stdscr.clear()
    stdscr.refresh()

    try:
        message_win = curses.newwin(curses.LINES - 2, curses.COLS, 0, 0)
        message_win.scrollok(True)

        for message in consumer:
            data = message.value
            with lock:
                messages.append(data)
                if data['end']:
                    if data['sender'] != username:
                        message_win.addstr(f"{data['sender']}님이 방을 나갔습니다.\n")
                        message_win.refresh()
                    else:
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(messages, f, ensure_ascii=True, indent=4)
                        return
                    message_win.refresh()
                else:
                    if data['sender'] == username:
                        # 현재 사용자의 메시지
                        message_win.addstr(f"나: {data['message']}\n")
                    else:
                        # 다른 사용자의 메시지
                        message_win.addstr(f"{data['sender']}: {data['message']}\n")
                    message_win.refresh()

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=True, indent=4)

        message_win.addstr(f"All received messages are saved in {chatroom}_messages.json\n")
        message_win.refresh()

    except KeyboardInterrupt:
        message_win.addstr("방을 나갑니다.\n")
        #message_win.refresh()
        return

username = input("사용자 이름: ")
chatroom = input("채팅방 이름: ")


def main(stdscr):
    # 스레딩

    stdscr.clear()
    stdscr.addstr(0, 0, f"[{username}]님이 [{chatroom}]에 입장했습니다.")
    stdscr.addstr(1, 0, f"아무 키나 눌러 채팅을 시작해주세요.")
    stdscr.refresh()
    stdscr.getch()  # 사용자가 아무 키나 눌러야 시작

    thread_1 = threading.Thread(target=pchat, args=(stdscr, chatroom, username))
    thread_2 = threading.Thread(target=cchat, args=(stdscr, chatroom, username))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

curses.wrapper(main)
