# teamchat

## API 추출 기능 개발 중...

** Apache Kafka를 이용한 채팅 프로그램 개발 **

## 사용 방법
```bash
$ pip install teamchat

$ teamchat-<method name>
```
[추가예정] pyproject.toml의 project.script에 반영해야함

## 개발자 일 때
```bash
$ git clone ... & cd ...

$ pdm venv create
$ source .venv/bin/activate
$ pdm install

$ pytest --cov
================ test session starts =================
platform linux -- Python 3.11.9, pytest-8.3.2, pluggy-1.5.0
configfile: pyproject.toml
plugins: cov-5.0.0

---------- coverage: platform linux, python 3.11.9-final-0 -----------
Name                      Stmts   Miss  Cover
---------------------------------------------
src/teamchat/api/__init__.py  0      0   100%
src/teamchat/api/chat.py      2      0   100%
tests/__init__.py             0      0   100%
tests/test_call.py            4      0   100%
---------------------------------------------
TOTAL                         6      0   100%


================= 1 passed in 0.05s ==================
```

