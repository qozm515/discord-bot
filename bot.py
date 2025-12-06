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
