from core.bot import dp
from config import check_list

@dp.message_callback()
async def on_callback(event):
    payload = event.callback.payload

    if payload == "start_click":
        await event.answer(notification="Готово")
        await event.message.answer("Записали Вас на пробное")
        await event.message.answer(check_list)