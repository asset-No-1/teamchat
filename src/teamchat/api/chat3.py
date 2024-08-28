from kafka import KafkaProducer, KafkaConsumer
from json import loads, dumps, load, JSONDecodeError
import threading
import os
import curses
import glob
import time

# 경로 저장
home_path = os.path.expanduser("~")
FILE_PATH = os.path.join(home_path, 'data', 'mov_data', '*_data.json')

# 시간 함수
def local_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#PRODUCER 설정
def pro_chat(username, stdscr):
    producer = KafkaProducer(
        bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'),
    )
    
    input_win = curses.newwin(1, curses.COLS - 1, curses.LINES - 1, 0)
    # 새 창 생성 (height = 창 높이 1줄 , width = 오른쪽에 한칸 여백, starty = 가장 아래쪽, startx = 왼쪽 가장자리)
    input_win.refresh()

    while True:
        input_win.clear()
        # 창의 내용을 지움
        input_win.addstr(0, 0, f"{username}: ")
        # (y, x) 위치에 username 추가
        input_win.refresh()
        # 창의 내용 화면에 즉시 반영
        curses.echo()  # 입력된 내용을 실시간으로 표시
        data = input_win.getstr().decode('utf-8', errors='ignore')
        

        if data == 'exit':
            # exit 메시지를 전송하여 컨슈머에게 종료 신호를 보냄
            message = {'user': username, 'message': 'exit', 'time': local_time()}
            producer.send('Product', value=message)
            producer.flush()
            break

        else:
            # 메시지를 JSON으로 보내면서 사용자 이름을 포함하고, local time을 표시.
            message = {'user': username, 'message': data, 'time': local_time()}
            producer.send('Product', value=message)
            producer.flush()
    
    # 채팅 종료 메시지를 화면에 출력
    # stdscr = 가상 디폴트 윈도우(표준화면)
    stdscr.addstr(curses.LINES - 1, 0, "채팅 종료, 아무 키나 눌러주세요")
    stdscr.refresh()
    stdscr.getch()  # 아무 키 입력 후 종료됨


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

#키값을 영화제목을 주기위해 데이터를 담을 빈 딕셔너리 생성
movie_dic = {}
data = read_json()

for i in data:
    movie_dic[i["movieNm"]] = i


#CONSUMER 설정
def con_chat(username, stdscr):
    consumer = KafkaConsumer(
        "Product",
        bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        enable_auto_commit=True,
        #group_id=f"group_{username}",
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        #auto_offset_reset='latest',
    )


    message_win = curses.newwin(curses.LINES - 2, curses.COLS, 0, 0)
    message_win.scrollok(True)

    try:
        for m in consumer:
            message = m.value
            if message['message'] == 'exit' and message['user'] == username:
                break
            # 시간 출력
            timestamp = message.get('time', '')
            message_time = f"{message['user']}: {message['message']}  {timestamp}\n"

            # 상대방이 보낸 메시지에서 '@'로 시작하지 않는 경우만 출력
            if message['user'] != username:
                if not message['message'].startswith('@'):
                    message_win.addstr(message_time)
                    #message_win.addstr(f"{message['user']}: {message['message']} {[timestamp]}\n")
            
            else:
                # 자신이 보낸 메시지가 '@'로 시작하는 경우
                if message['message'].startswith('@'):

                    # '@' 뒤에 있는 영화 제목을 추출
                    #movie_title = message['message'][1:].strip()
                    movie_title = message['message'][1:].strip().replace(" ","")
                    matched_title = None
                    for title in movie_dic:
                        if title.replace(" ", "") == movie_title:
                            matched_title = title
                            break
                    if matched_title:
                        value = movie_dic[matched_title]
                    #if movie_title in movie_dic:
                        #value = movie_dic[movie_title]
                        message_win.addstr(f"사용자: {message['message']} - {value}\n {timestamp}\n")
                    elif not matched_title:
                        message_win.addstr(f"사용자: 영화 정보를 찾을 수 없습니다. {timestamp}\n")
                    else:
                        message_win.addstr(f"사용자: {message['message']}  {timestamp}\n")
                else:
                    # 일반 메시지 출력
                    message_win.addstr(f"사용자: {message['message']}  {timestamp}\n")

            message_win.refresh()
        
    
    except KeyboardInterrupt:
        stdscr.addstr(curses.LINES - 1, 0, "Consumer 종료")
        stdscr.refresh()
        stdscr.getch()  # 사용자 입력을 대기하여 화면이 유지되도록 함

    #except JSONDecodeError as e:
     #   print(f"JSON Decode Error: {e}")
      #  print(f"Raw message: {message}")

    #except TypeError as e:
     #   print(f"TypeError: {e}")
      #  print(f"Raw message: {message}")


username = input("이름: ")
#topic = input("방 이름: ")

def main(stdscr):

    stdscr.clear()
    stdscr.addstr(1, 0, f"아무 키나 눌러 채팅을 시작해주세요.")
    stdscr.refresh()
    stdscr.getch()  # 사용자가 아무 키나 눌러야 시작
    stdscr.clear()
    stdscr.refresh()

    pro_thread = threading.Thread(target = pro_chat, args = (username, stdscr))
    con_thread = threading.Thread(target = con_chat, args = (username, stdscr))

    pro_thread.start()
    con_thread.start()

    pro_thread.join()
    con_thread.join()
#if __name__ == "__main__": # 

curses.wrapper(main) # curses 환경을 설정하고 'main' 함수 호출
