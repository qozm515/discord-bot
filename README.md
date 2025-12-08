# my-first-bot

파이썬으로 만든 연습용 디스코드 봇입니다.

현재 기능:
- `!ping` 명령어에 `pong` 으로 응답

이 문서는 **완전 초보가 윈도우에서 디스코드 봇을 처음부터 끝까지 만드는 과정**을 정리한 기록입니다.

---

## 0. 전체 흐름 한눈에 보기

1. 파이썬 설치 (Windows)
2. VS Code 설치 및 기본 설정
3. Git 설치 (선택) + GitHub 계정 준비
4. 디스코드 계정 및 테스트용 서버 준비
5. 파이썬 프로젝트 폴더/가상환경/라이브러리 설치
6. 디스코드 개발자 포털에서 봇 애플리케이션/봇 계정 생성
7. 토큰 발급 + `.env` 파일로 관리
8. 인텐트(Message Content Intent) 토글 설정
9. OAuth2 URL Generator로 봇을 디스코드 서버에 초대
10. `bot.py` 작성 후 `py bot.py` 로 실행, `!ping` 테스트
11. `.gitignore` / `README.md` / Git 커밋 / GitHub 업로드
12. 자주 겪었던 문제 정리 (PowerShell, 인텐트 에러, 봇 안 보일 때 등)

---

## 1. 준비물

### 1-1. 파이썬 설치 (Windows)

1. Microsoft Store 또는 공식 사이트에서 Python 3.10+ 버전을 설치합니다.
2. 설치 후 터미널이나 cmd 에서 아래 명령으로 버전을 확인합니다.

```bash
py --version
````

예시:

```text
Python 3.14.2
```

### 1-2. VS Code 설치

1. [https://code.visualstudio.com](https://code.visualstudio.com) 에서 VS Code 설치
2. 설치 후 실행
3. VS Code에서 **Extensions(확장)** 아이콘 클릭 → `Python` 검색 → Microsoft의 Python 확장 설치

### 1-3. Git 설치 (선택이지만 추천)

1. [https://git-scm.com](https://git-scm.com) 에서 Windows용 Git 설치
2. 설치 후 터미널에서 확인:

```bash
git --version
```

### 1-4. 디스코드 계정 및 테스트용 서버

1. 디스코드 앱 또는 웹에서 계정 생성/로그인
2. 좌측 서버 목록에서 `+` 클릭 → **서버 만들기** → 테스트용 서버 하나 생성
   (예: “엄지왕 봇 테스트 서버”)

---

## 2. 파이썬 프로젝트 초기 설정 (로컬)

### 2-1. 프로젝트 폴더 구조

예시 기준:

```text
C:\Users\사용자이름\dev\discord-bot
```

1. 탐색기 또는 cmd에서 작업용 폴더를 만듭니다.

```bash
cd C:\Users\사용자이름
mkdir dev
cd dev
mkdir discord-bot
cd discord-bot
```

### 2-2. VS Code에서 폴더 열기

1. VS Code 실행
2. 메뉴: **File → Open Folder…**
3. `C:\Users\사용자이름\dev\discord-bot` 선택
4. “이 폴더를 신뢰하겠냐”는 창이 뜨면
   → **Yes, I trust the authors** 선택

### 2-3. 가상환경 생성

VS Code에서 터미널 열기:

* 단축키: `Ctrl + ` (숫자 1 왼쪽의 백틱 키)
* 또는 상단 메뉴: **Terminal → New Terminal**

터미널에서:

```bash
cd C:\Users\사용자이름\dev\discord-bot

# 가상환경 생성
py -m venv .venv
```

### 2-4. 가상환경 활성화 (cmd 기준)

PowerShell에서 실행 정책 에러가 날 수 있으므로, **cmd 터미널**을 사용하는 것을 기준으로 합니다.

1. VS Code 터미널에서 프로필을 `Command Prompt` 로 선택
2. 아래 명령 실행:

```bash
.\.venv\Scripts\activate
```

프롬프트가 다음처럼 바뀌면 성공입니다.

```text
(.venv) C:\Users\사용자이름\dev\discord-bot>
```

### 2-5. 라이브러리 설치

```bash
pip install -U discord.py python-dotenv
```

---

## 3. 디스코드 개발자 포털: 애플리케이션/봇 설정

### 3-1. 애플리케이션 생성

1. 브라우저에서: [https://discord.com/developers/applications](https://discord.com/developers/applications) 접속
2. 우측 상단 **New Application** 클릭
3. 이름 입력 (예: `my-first-bot`)
4. 약관 동의 체크 박스 선택 → **Create**

이 시점에는 “애플리케이션”만 있고, 실제 디스코드 봇 유저는 아직 없습니다.

### 3-2. Bot 탭에서 봇 계정 생성

1. 왼쪽 메뉴에서 **Bot** 탭 클릭 (로봇 아이콘)
2. **Add Bot** 또는 **Create Bot** 버튼 클릭 → 확인
3. Username: `my-first-bot` 등으로 표시됨
   → 이제 실제 “봇 유저”가 만들어진 것입니다.

### 3-3. Message Content Intent 토글 설정 (중요)

1. 같은 Bot 페이지에서 아래로 스크롤

2. **Privileged Gateway Intents** 섹션 찾기

3. 이 중에서:

   * Presence Intent: 필요 시
   * Server Members Intent: 필요 시
   * **Message Content Intent: 반드시 ON**

4. 하단의 **Save Changes** 버튼 클릭

> 이 토글을 켜지 않으면,
> 코드에서 `intents.message_content = True` 를 사용했을 때
> `discord.errors.PrivilegedIntentsRequired` 에러가 발생합니다.

### 3-4. 토큰 발급

1. Bot 페이지 상단에서 **Token** 섹션 찾기
2. `Reset Token` / `View Token` / `Copy` 버튼으로 토큰 복사
3. 이 값은 **봇의 비밀번호**이므로 절대 공개 저장소에 올리면 안 됩니다.

---

## 4. 환경 변수 파일(.env) + .gitignore 설정

### 4-1. `.env` 파일

프로젝트 루트(`discord-bot` 폴더)에 `.env` 파일을 만들고 아래 내용 입력:

```env
DISCORD_TOKEN=여기에_디스코드_봇_토큰_붙여넣기
```

저장 (`Ctrl + S`).

### 4-2. `.gitignore` 파일

Git을 사용할 경우, 비밀 파일과 가상환경을 제외하기 위해 `.gitignore` 생성:

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

## 5. 봇 코드 작성 (`bot.py`)

프로젝트 루트에 `bot.py` 파일을 만들고 다음 내용을 작성합니다.

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

# 접두사: ! 로 시작하는 명령 사용
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

## 6. 디스코드 서버에 봇 초대 (OAuth2 URL Generator)

### 6-1. Scopes 설정

1. 개발자 포털에서 `my-first-bot` 애플리케이션 선택
2. 왼쪽 메뉴에서 **OAuth2 → URL Generator** 선택
3. **SCOPES** 섹션에서:

   * `bot` ✅ (필수)
   * (선택) `applications.commands` ✅ (슬래시 명령을 쓸 계획일 때)

다른 항목은 건드리지 않아도 됩니다.

### 6-2. Bot Permissions 설정 (View/Send/History)

같은 페이지에서 아래로 스크롤하면 **BOT PERMISSIONS** 섹션이 있습니다.

* General Permissions:

  * ✅ View Channels
* Text Permissions:

  * ✅ Send Messages
  * ✅ Read Message History

기본 `!ping` 봇에는 이 세 가지면 충분합니다.

### 6-3. 초대 URL 생성 및 사용

1. 페이지 하단의 **Generated URL** 을 복사
2. 브라우저 주소창에 붙여넣고 접속
3. “Add to Server / 서버 선택” 드롭다운에서
   → 테스트 서버(예: “엄지왕 봇 테스트 서버”) 선택
4. 권한 확인 후 **Authorize** 클릭
5. “로봇이 아닙니다” 체크

### 6-4. 서버에서 봇이 들어왔는지 확인

디스코드 앱에서:

1. 해당 서버 열기
2. **서버 설정 → 사용자 관리 → 멤버(또는 사람)** 메뉴로 이동
3. 멤버 목록에 `my-first-bot (BOT)` 이 있는지 확인

> 여기에서 실제로 많이 헷갈렸던 부분:
> Installation 탭에서 “설치”만 하면 멤버 목록에 봇이 안 보일 수 있습니다.
> **반드시 OAuth2 URL Generator에서 `bot` 스코프를 체크한 URL** 로 초대해야
> 서버 멤버로 등록됩니다.

---

## 7. 봇 실행 및 테스트

### 7-1. 봇 실행

VS Code 터미널 (cmd, 가상환경 활성화된 상태)에서:

```bash
cd C:\Users\사용자이름\dev\discord-bot

# 가상환경 활성화 (이미 활성화된 상태라면 생략 가능)
.\.venv\Scripts\activate

# 봇 실행
py bot.py
```

정상이라면 터미널에 대략 다음과 같은 로그가 표시됩니다.

```text
INFO     discord.client logging in using static token
로그인 완료: my-first-bot#1234 (ID: 123456789012345678)
봇이 준비되었습니다.
```

### 7-2. 디스코드에서 `!ping` 테스트

1. 디스코드에서 봇이 추가된 서버의 텍스트 채널 (예: `#일반`) 열기
2. 메시지로 다음 입력:

```text
!ping
```

3. 봇이 다음과 같이 응답하면 성공입니다.

```text
pong
```

---

## 8. 자주 겪었던 문제와 해결법

### 8-1. PowerShell에서 venv 활성화가 안 될 때

에러 예시:

> 이 시스템에서 스크립트를 실행할 수 없으므로 … Activate.ps1 파일을 로드할 수 없습니다.

해결 방법 둘 중 하나:

1. **cmd 프로필 사용 (추천)**

   * VS Code 터미널 프로필을 `Command Prompt` 로 설정
   * 다음 명령 사용:

   ```bash
   .\.venv\Scripts\activate
   ```

2. PowerShell에서 `.bat` 파일로 활성화:

   ```bash
   .\.venv\Scripts\activate.bat
   ```

둘 중 하나로 `(.venv)` 표시만 뜨면 됩니다.

---

### 8-2. `discord.errors.PrivilegedIntentsRequired` 에러

에러 메시지 요약:

> PrivilegedIntentsRequired: … privileged intents that have not been explicitly enabled…

원인:

* 코드에서 `intents.message_content = True` 를 켰는데,
* 개발자 포털 Bot 탭에서 **Message Content Intent** 토글이 OFF 상태거나,
* 켠 뒤에 `Save Changes` 를 누르지 않은 경우

해결 순서:

1. 개발자 포털 → 애플리케이션 → **Bot** 탭
2. **Privileged Gateway Intents** 섹션에서

   * **Message Content Intent** 를 ON
3. 하단 **Save Changes** 클릭
4. `py bot.py` 재실행

---

### 8-3. 서버 멤버 목록에 봇이 안 나타날 때

상황:

* OAuth2/Installation 등을 눌러 “뭔가 설치”는 한 것 같은데,
* 서버 설정 → 멤버 목록에 봇이 없다.

체크할 것:

1. OAuth2 URL Generator에서 **SCOPES에 `bot` 이 체크**되어 있는지
2. 해당 URL로 실제로 접속해, 테스트 서버를 선택하고 **Authorize** 까지 눌렀는지
3. 디스코드 서버 설정 → 멤버 메뉴에서
   `my-first-bot (BOT)` 이 보이는지

---

## 9. Git / GitHub 으로 버전 관리 (선택)

### 9-1. 첫 초기화 및 커밋

프로젝트 루트에서:

```bash
git init
git add .
git commit -m "첫 디스코드 봇 초기 버전"
```

※ 이때 `.env`, `.venv/` 는 `.gitignore` 에 포함되어 있어야 합니다.

### 9-2. GitHub에 올리기

1. GitHub 웹에서 새 저장소 생성 (예: `discord-bot`)

   * README / .gitignore / License 는 생성하지 않아도 됨
2. 생성 직후 안내 문구 예시:

```bash
git remote add origin https://github.com/내-계정이름/discord-bot.git
git branch -M main
git push -u origin main
```

3. 이후에는 수정할 때마다:

```bash
git add README.md bot.py
git commit -m "기능 추가 및 문서 업데이트"
git push
```

### 9-3. 커밋 로그 보는 법

* 로컬:

```bash
git log --oneline
```

* GitHub 웹:

  * 저장소 페이지 상단의 `N commits` 버튼 클릭
  * 또는 파일 화면에서 `History` 버튼 클릭

---

## 10. 앞으로의 확장 아이디어

* `!help`, `!ping` 외에 명령어 추가
* 슬래시 명령(`/ping`) 지원
* 특정 채널에 자동으로 공지 보내기
* 로그 파일/데이터베이스와 연동
* 최종적으로는 24시간 돌아가는 VPS/서버에 올려 상시 서비스화

이 문서는 **“처음 디스코드 봇을 만들 때 어떤 화면에서 어떤 체크박스를 켜야 하는지, 어떤 오류를 어떻게 해결했는지”** 를 그대로 기록한 것입니다.
필요에 따라 스크린샷이나 개인적인 메모를 더 추가해 가면,
나중에 다른 봇을 만들 때도 좋은 템플릿이 될 수 있습니다.
