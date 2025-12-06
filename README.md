# my-first-bot

파이썬으로 만든 연습용 디스코드 봇입니다.  
현재 기능:
- `!ping` 명령어에 `pong` 으로 응답

## 1. 개발 환경

- Python 3.14.2 (Windows)
- 가상환경: `.venv`
- 주요 라이브러리:
  - `discord.py`
  - `python-dotenv`

## 2. 초기 설정

```bash
# 프로젝트 폴더 생성
mkdir discord-bot
cd discord-bot

# 가상환경 생성
py -m venv .venv

# 가상환경 활성화 (Windows CMD)
.\.venv\Scripts\activate

# 라이브러리 설치
pip install -U discord.py python-dotenv
```

## 3. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 만들고, 디스코드 개발자 포털에서 발급받은 봇 토큰을 넣습니다.

DISCORD_TOKEN=여기에_봇_토큰_붙여넣기

> ⚠ `.env` 파일은 절대 GitHub에 올리지 않습니다.
> (이미 `.gitignore` 에 추가되어 있습니다.)

## 4. 봇 실행

```bash
# 가상환경 활성화
.\.venv\Scripts\activate

# 봇 실행
py bot.py
```

디스코드 서버에서 `!ping` 을 입력하면 `pong` 으로 응답합니다.

## 5. 인텐트 설정

디스코드 개발자 포털의 **Bot** 탭에서 다음을 설정했습니다.

* **MESSAGE CONTENT INTENT**: ON
* 변경 후 반드시 `Save Changes` 클릭