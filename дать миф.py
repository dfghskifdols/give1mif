from hikka import loader
from hikka.modules import Module
import asyncio
import aiohttp

API_TOKEN = '7705193251:AAFrnXeNBgiFo3ZQsGNvEOa2lNzQPKo3XHM'
CHAT_ID = '-1002268486160'

async def send_message(text, reply_to_message_id=None):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
        data = {
            'chat_id': CHAT_ID,
            'text': text,
        }
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        try:
            async with session.post(url, data=data) as response:
                return await response.json()
        except Exception as e:
            print(f"❌ Помилка при надсиланні повідомлення: {e}")
            return None

async def get_latest_updates():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://api.telegram.org/bot{API_TOKEN}/getUpdates", timeout=5) as response:
                return await response.json()
        except Exception as e:
            print(f"❌ Помилка при отриманні оновлень: {e}")
            return {}

class RewardAutoReply(Module):
    strings = {"name": "RewardAutoReply"}

    async def on_ready(self):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.monitor_bot_messages())

    async def monitor_bot_messages(self):
        last_checked_id = 0
        while True:
            updates = await get_latest_updates()
            for update in updates.get("result", []):
                msg = update.get("message", {})
                text = msg.get("text")
                message_id = msg.get("message_id")
                reply_to = msg.get("reply_to_message", {})

                if not message_id or message_id <= last_checked_id:
                    continue

                if text == "🎁 Выдаю!" and reply_to:
                    reply_id = reply_to.get("message_id")
                    if reply_id:
                        await send_message("дать миф 1", reply_to_message_id=reply_id)
                        print(f"✅ Надіслано 'дать миф 1' у відповідь на повідомлення {reply_id}")
                        last_checked_id = message_id

            await asyncio.sleep(5)

def register(cb):
    return RewardAutoReply(cb)
