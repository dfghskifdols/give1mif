# meta developer: @Bl_Nexus
# meta name: RewardResponderMod
# meta description: Выдает 1 миф, если у пользователя >=15 тикетов
# requires: asyncpg

import asyncio
import asyncpg
from telethon import events
from .. import loader

# Параметри підключення до БД через URL
DATABASE_URL = "postgresql://neondb_owner:npg_PXgGyF7Z5MUJ@ep-shy-feather-a2zlgfcw-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"

# Функція перевірки квитків
async def has_enough_tickets(user_id):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        result = await conn.fetchrow("SELECT tickets FROM user_tickets WHERE user_id = $1", user_id)
        await conn.close()
        return result and result["tickets"] >= 15
    except Exception as e:
        print(f"[RewardResponderMod] ❌ DB error: {e}")
        return False

@loader.tds
class RewardResponderMod(loader.Module):
    """Авто-реагування на /get_reward, якщо у користувача 15+ квитків"""

    strings = {"name": "RewardResponderMod"}

    async def client_ready(self, client, db):
        self.client = client

    async def watcher(self, event):
        if not isinstance(event, events.NewMessage.Event):
            return

        msg = event.message

        if msg.raw_text.strip() != "/get_reward":
            return

        user_id = msg.sender_id
        if await has_enough_tickets(user_id):
            try:
                reply = await msg.reply("дать миф 1")
                await asyncio.sleep(3)
                await reply.delete()
            except Exception as e:
                print(f"[RewardResponderMod] ❌ Error sending or deleting message: {e}")
