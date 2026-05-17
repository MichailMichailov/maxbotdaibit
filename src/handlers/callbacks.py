from core.bot import dp
from config import FILE_PATH_CHECKLIST, check_list
from services.users import add_user
from maxapi.types import InputMedia

attachment = None
async def preload_file(bot):
    global attachment
    media = InputMedia(path=FILE_PATH_CHECKLIST)
    attachment = await bot.upload_media(media)

@dp.message_callback()
async def on_callback(event):
    payload = event.callback.payload

    if payload == "start_click":
        added = await add_user(
            user_id=event.from_user.user_id,
            chat_id=event.chat.chat_id,
            first_name=event.from_user.first_name,
            last_name=event.from_user.last_name,
            username=event.from_user.username,
            payload=event.callback.payload
        )
        await event.answer(notification="Готово")
        if added:
            await event.message.answer("Записали Вас на пробное")
            if attachment:
                await event.bot.send_message( chat_id=event.chat.chat_id,
                    text=check_list, attachments=[attachment] )
            else:
                await event.message.answer("Чек-лист временно недоступен")
        else:
            await event.message.answer("Вы уже записаны")