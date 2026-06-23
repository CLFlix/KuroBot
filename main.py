import asyncio
from bot import KuroBot
from utils.utils import write_log
from bot import LOG_FILE

async def main():
    bot = KuroBot()

    try:
        await bot.run_forever()
    except Exception as e:
        write_log(LOG_FILE, e)

if __name__ == "__main__":
    asyncio.run(main())