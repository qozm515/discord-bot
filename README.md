```markdown
# my-first-bot

파이썬으로 만든 연습용 디스코드 봇입니다.  
현재 기능:
- `!ping` 명령어에 `pong` 으로 응답

처음 디스코드 봇을 만들면서 겪었던 전체 과정을 기록한 문서입니다.  
**“윈도우 + 파이썬 + VS Code + 디스코드 개발자 포털 + GitHub”** 를 한 번에 처음 겪는 사람을 기준으로 작성되었습니다.

---

## 0. 이 문서를 읽으면 알 수 있는 것

- 내 PC(Windows)에서 디스코드 봇을 처음부터 끝까지 만드는 순서
- 디스코드 개발자 포털에서
  - 애플리케이션 생성
  - Bot 탭 설정
  - MESSAGE CONTENT INTENT 토글 설정
  - OAuth2 URL Generator에서 **봇을 서버 멤버로 초대**하는 정확한 방법
- `PrivilegedIntentsRequired` 에러, PowerShell 실행 정책 문제 등  
  실제로 겪었던 대표적인 삽질과 해결법

---

## 1. 개발 환경

- OS: Windows 10/11
- Python: 3.14.2 (Windows Store에서 설치, `py --version` 으로 확인)
- 에디터: Visual Studio Code
- 가상환경: `.venv/`
- 주요 라이브러리:
  - `discord.py`
  - `python-dotenv`
- 버전 관리: Git + GitHub

프로젝트 폴더 예시:

```text
C:\Users\사용자이름\dev\discord-bot
```

---

## 2. 파이썬 프로젝트 초기 설정

### 2-1. 폴더 및 가상환경 생성

```bash
# (예시) 작업용 폴더로 이동
cd C:\Users\사용자이름\dev

# 프로젝트 폴더 생성
mkdir discord-bot
cd discord-bot

# 가상환경 생성
py -m venv .venv
```

### 2-2. 가상환경 활성화 (cmd 기준)

PowerShell에서 실행 정책 때문에 에러가 나는 경우가 있어,
**Windows 명령 프롬프트(cmd)** 를 기준으로 기록합니다.

```bash
# cmd 터미널에서
.\.venv\Scripts\activate
```

프롬프트 앞에 `(.venv)` 가 붙으면 활성화된 것입니다.

### 2-3. 라이브러리 설치

```bash
# 가상환경이 활성화된 상태에서
pip install -U discord.py python-dotenv
```

---

## 3. 디스코드 개발자 포털 설정

### 3-1. 애플리케이션 생성

1. 브라우저에서 `https://discord.com/developers/applications` 접속
2. 오른쪽 상단 **New Application** 클릭
3. 이름 예시: `my-first-bot`
4. 약관 동의 체크 후 **Create**

이 시점에서는 “애플리케이션”만 있을 뿐, 아직 디스코드 봇 유저는 만들어지지 않았습니다.

### 3-2. Bot 탭에서 봇 계정 만들기 + 인텐트 토글

1. 왼쪽 메뉴에서 **Bot** 탭 선택
2. 가운데의 **Add Bot** 또는 **Create Bot** 버튼 클릭 → 확인

   * 이제 실제 **봇 계정(로봇 아이콘)** 이 생성됩니다.
3. 같은 화면에서 아래로 내려가 **Privileged Gateway Intents** 섹션에서:

   * **Message Content Intent** 토글을 **ON** 으로 설정
   * 필요 시 나중에 `Server Members Intent` 등도 켤 수 있으나,
     기본 `!ping` 봇에는 `Message Content Intent` 만 있으면 충분
4. 화면 하단의 **Save Changes** 버튼을 꼭 눌러 변경사항 저장

> 이 토글을 켜지 않으면,
> 코드에서 `intents.message_content = True` 를 썼을 때
> `discord.errors.PrivilegedIntentsRequired` 에러가 발생합니다.

### 3-3. 봇 토큰 발급

1. 다시 Bot 탭 상단에서 **Token** 섹션을 찾습니다.
2. `Reset Token` / `View Token` / `Copy` 버튼으로 토큰을 확인하고 복사
3. 이 값은 **봇 비밀번호**이므로 절대 공개 저장소에 올리면 안 됩니다.

---

## 4. 환경 변수 파일(.env) 설정

프로젝트 루트(`discord-bot` 폴더)에 `.env` 파일을 만들고, 아래 내용을 작성합니다.

```env
DISCORD_TOKEN=여기에_디스코드_봇_토큰_붙여넣기
```

> ⚠ `.env` 파일은 절대 GitHub에 올리지 않습니다.
> `.gitignore` 에 `.env` 를 반드시 추가해야 합니다.

예시 `.gitignore`:

```gitignore
# Python 가상환경
.venv/

# 환경 변수 (비밀 토큰)
.env

# 파이썬 캐시 파일
__pycache__/
*.pyc
```

---

## 5. 봇 코드 (`bot.py`)

프로젝트 루트에 `bot.py` 파일을 만들고 다음 코드를 작성합니다.

```python
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 인텐트 설정: 메시지 내용 읽기 활성화
intents = discord.Intents.default()
intents.message_content = True

# 접두사: !로 시작하는 명령 사용
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user} (ID: {bot.user.id})")
    print("봇이 준비되었습니다.")


@bot.command()
async def ping(ctx):
    """!ping 이라고 치면 pong 으로 응답합니다."""
    await ctx.send("pong")


if __name__ == "__main__":
    if TOKEN is None:
        raise RuntimeError("DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
    bot.run(TOKEN)
```

---

## 6. 봇을 디스코드 서버에 초대하기

여기에서 실제로 많이 헷갈렸던 부분입니다.
**“앱을 서버에 설치하는 것”과 “봇 유저를 멤버로 초대하는 것”** 이 살짝 다르게 느껴집니다.

핵심은:

* **OAuth2 → URL Generator** 에서 **`bot` 스코프**를 포함한 URL을 만들어야
  → 봇이 서버 **멤버 목록**에 `BOT` 라벨을 달고 등장합니다.

### 6-1. OAuth2 URL Generator 설정

1. 개발자 포털에서 `my-first-bot` 애플리케이션 선택
2. 왼쪽 메뉴에서 **OAuth2 → URL Generator** 선택
3. **SCOPES** 섹션:

   * `bot` ✅ 체크
   * (선택) `/슬래시` 명령을 쓸 계획이라면 `applications.commands` 도 함께 체크
4. **BOT PERMISSIONS** 섹션 (아래로 스크롤):

   * **View Channels** (채널 보기)
   * **Send Messages** (메시지 보내기)
   * **Read Message History** (메시지 기록 읽기)
   * 이 세 가지면 기본 `!ping` 봇에 충분
5. 아래쪽 **Generated URL** 을 복사

### 6-2. URL로 서버에 봇 추가

1. 복사한 URL을 브라우저 주소창에 붙여넣고 접속
2. “Add to Server / 서버 선택” 드롭다운에서 **내 테스트 서버**를 선택
3. 권한 확인 화면에서 **Authorize** 클릭
4. CAPTCHA(로봇이 아닙니다) 체크

이제 디스코드 앱에서:

* 서버 설정 → **사람(멤버)** 메뉴로 들어가면

  * 사용자 계정 + `my-first-bot (BOT)` 이 함께 보이는지 확인합니다.

> 여기에서 가장 헷갈렸던 점:
> Installation 탭이나 다른 링크로 “앱 설치”만 하면
> **서버 멤버 목록에는 봇이 안 보입니다.**
> 반드시 **`bot` 스코프를 포함한 OAuth2 URL** 을 사용해야 합니다.

---

## 7. 봇 실행 및 테스트

### 7-1. 실행

```bash
# 프로젝트 폴더로 이동
cd C:\Users\사용자이름\dev\discord-bot

# 가상환경 활성화
.\.venv\Scripts\activate

# 봇 실행
py bot.py
```

터미널에서 예를 들어 다음과 같은 로그가 나오면 성공입니다.

```text
INFO     discord.client logging in using static token
로그인 완료: my-first-bot#1234 (ID: 123456789012345678)
봇이 준비되었습니다.
```

### 7-2. 디스코드에서 테스트

1. 디스코드에서 봇이 추가된 서버의 `#일반` 채널을 엽니다.
2. 메시지로 아래를 입력합니다.

```text
!ping
```

3. 봇이 다음과 같이 응답하면 정상 동작입니다.

```text
pong
```

---

## 8. 자주 겪는 문제와 해결

### 8-1. PowerShell에서 가상환경 활성화가 안 될 때

에러 예시:

> 이 시스템에서 스크립트를 실행할 수 없으므로 … Activate.ps1 파일을 로드할 수 없습니다.

해결 방법:

* 방법 1: **cmd 터미널에서 실행**
  VS Code 터미널에서 프로필을 `Command Prompt` 로 바꾸고 다음 실행

  ```bash
  .\.venv\Scripts\activate
  ```

* 방법 2: PowerShell에서 `.bat` 사용

  ```bash
  .\.venv\Scripts\activate.bat
  ```

둘 중 하나로 `(.venv)` 표시만 뜨면 충분합니다.

---

### 8-2. `discord.errors.PrivilegedIntentsRequired` 에러

에러 메시지 예시:

> PrivilegedIntentsRequired: Shard ID None is requesting privileged intents that have not been explicitly enabled…

원인:

* 코드에서

  ```python
  intents = discord.Intents.default()
  intents.message_content = True
  ```

  로 **MESSAGE CONTENT 인텐트**를 켰는데,
* 개발자 포털 Bot 탭에서 **Message Content Intent** 토글을 켜지 않았거나
  켠 뒤에 **Save Changes** 를 누르지 않은 경우

해결:

1. 개발자 포털 → 해당 애플리케이션 → **Bot** 탭
2. **Privileged Gateway Intents** 섹션 확인
3. **Message Content Intent** 를 ON
4. 하단 **Save Changes** 클릭
5. `py bot.py` 를 다시 실행

---

### 8-3. 서버 멤버 목록에 봇이 안 보일 때

상황:

* 초대 URL을 통해 무언가 설치된 것 같지만,
* 서버 설정 → 사람(멤버) 목록에는 봇이 나타나지 않는 경우

체크할 것:

1. OAuth2 URL Generator에서 **Scopes에 `bot` 이 체크되어 있는지** 확인
2. 해당 URL로 다시 접속해서 **내 서버**를 선택하고 **Authorize** 했는지 확인
3. 디스코드 서버 설정 → **멤버** 메뉴에서
   `my-first-bot (BOT)` 이 보이는지 확인

서버 멤버 목록에 봇이 보이기만 하면,
이후에는 코드 실행 여부에 따라 온라인/오프라인 상태만 바뀝니다.

---

## 9. Git / GitHub 메모 (요약)

이 프로젝트를 Git으로 관리할 때 최소한의 명령만 정리합니다.

### 9-1. 첫 커밋

```bash
git init
git add .
git commit -m "첫 디스코드 봇 초기 버전"
```

### 9-2. GitHub에 올리기 (이미 저장소를 만든 뒤)

```bash
git remote add origin https://github.com/내-계정이름/discord-bot.git
git branch -M main
git push -u origin main
```

이후에는 수정할 때마다:

```bash
git add bot.py README.md
git commit -m "명령어 추가"  # 메시지는 자유롭게
git push
```

이런 식으로 기록을 쌓아가면,
나중에 “어디서 꼬였는지”를 되돌아보거나, 다른 서버로 옮길 때도 훨씬 수월해집니다.

```