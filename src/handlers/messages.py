from maxapi.types import MessageCreated
from core.bot import dp
from config import text_start_btn, check_list


@dp.message_created()
async def on_message(event: MessageCreated):
    text = (event.message.body.text or "").strip()

    if text == text_start_btn:
        await event.message.answer(check_list)