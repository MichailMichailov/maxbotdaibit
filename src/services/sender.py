from maxapi.exceptions import MaxApiError
from core.bot import bot

async def safe_send(chat_id: int, text: str, attachments=None):
    try:
        return await bot.send_message(
            chat_id=chat_id,
            text=text,
            attachments=attachments
        )
    except MaxApiError as e:
        if getattr(e, "code", None) == 404:
            return None
        raise

async def broadcast(chat_ids: list[int], text: str):
    for chat_id in chat_ids:
        await safe_send(chat_id, text)