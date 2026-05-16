import asyncio
from core.bot import bot, dp

import handlers.start
import handlers.callbacks
import handlers.messages


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await dp.stop_polling()
        await bot.session.close()

if __name__ == "__main__":
    try:
        print("Bot started...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")



# from config import TOKEN, text_start_btn, title_start_btn, check_list

# import asyncio
# from maxapi import Bot, Dispatcher
# from maxapi.exceptions import MaxApiError
# from maxapi.types import (BotStarted, MessageCreated, ButtonsPayload, MessageButton, 
#                           CallbackButton, MessageCallback)

# bot = Bot(TOKEN)
# dp = Dispatcher()

# @dp.bot_started()
# async def on_bot_started(event: BotStarted):
#     keyboard = ButtonsPayload(
#         buttons=[
#             [CallbackButton(text=text_start_btn, payload="start_click")]
#         ]
#     ).pack()
#     await event.bot.send_message( chat_id=event.chat_id, text=title_start_btn, attachments=[keyboard] )
# @dp.message_callback()
# async def on_callback(event: MessageCallback):
#     payload = event.callback.payload 
    
#     if payload == "start_click":
#         await event.answer(notification="Готово")
#         await event.message.answer("Записали Вас на пробное")
#         await event.message.answer(check_list)
# @dp.message_created()
# async def on_message(event: MessageCreated):
#     try:
#         text = event.message.body.text or ""

#         if text == text_start_btn:
#             await event.message.answer(check_list)

#     except MaxApiError as e:
#         if e.code == 404:
#             return
#         raise

# async def main():
#     try:
#         await dp.start_polling(bot)
#     finally:
#         await dp.stop_polling()
#         await bot.session.close()

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("Bot stopped")