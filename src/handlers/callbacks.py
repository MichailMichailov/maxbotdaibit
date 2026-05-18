from core.bot import dp
from config import FILE_PATH_CHECKLIST, Write_Test, check_list
from services.users import add_user
from maxapi.types import InputMedia

attachment = None
async def preload_file(bot):
    global attachment
    media = InputMedia(path=FILE_PATH_CHECKLIST)
    attachment = await bot.upload_media(media)

def extract_phone_from_contact(payload):
    vcf_info = payload.vcf_info
    phone = None
    for line in vcf_info.splitlines():
        if line.startswith("TEL"):
            phone = line.split(":")[1]
            break
    return phone

@dp.message_created()
async def on_message(event):
    attachments = event.message.body.attachments or []

    for att in attachments:
        if att.type == "contact":
            payload = att.payload
            phone = extract_phone_from_contact(payload)
            added = await add_user(
                user_id=event.from_user.user_id,
                chat_id=event.chat.chat_id,
                first_name=event.from_user.first_name,
                last_name=event.from_user.last_name,
                username=event.from_user.username,
                phone=phone
            )

            await event.message.answer("Записали Вас на пробное" if added else "Вы уже записаны")
            if added:
                await event.message.answer(Write_Test)
                if attachment:
                    await event.bot.send_message( chat_id=event.chat.chat_id,
                        text=check_list, attachments=[attachment])
                else:
                    await event.message.answer("Чек-лист временно недоступен")
            return