from core.bot import dp
from config import title_start_btn
from keyboards.start import start_keyboard
from services.sender import safe_send

@dp.bot_started()
async def on_bot_started(event):
    await safe_send(
        chat_id=event.chat_id,
        text=title_start_btn,
        attachments=[start_keyboard()]
    )