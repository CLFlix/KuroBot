import asyncio
from bot.bot import KuroBot
from bot.utils.utils import write_log
from bot.bot import LOG_FILE

async def main():
    bot = KuroBot()

    try:
        await bot.run_forever()
    except Exception as e:
        write_log(LOG_FILE, f"[FATAL] - Bot crashed: {e}")

if __name__ == "__main__":
    asyncio.run(main())