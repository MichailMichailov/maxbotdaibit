import asyncio
import os

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(PARENT_DIR, 'data', 'users.json')
FILE_PATH_CHECKLIST = os.path.join(PARENT_DIR, 'data', 'checklist.pdf')

file_lock = asyncio.Lock()

BOT_NAME = "ДАЙБИТ_БОТ"
id_bot = "@id645485463201_bot"

title_start_btn="""
Для подтверждения записи на пробное занятие по битбоксу нажмите «Я пойду» 👇🏻 

После чего мы пришлем бесплатный чек-лист:
«Переводчик детского «не хочу»: 3 скрытых смысла, о которых молчат психологи.» 🎁 
"""
text_start_btn="Я пойду"
check_list = """
Переводчик детского «не хочу»: 3 скрытых смысла, о которых молчат психологи.
"""
REMINDER_TEXT = """
напоминаем, что сегодня вечером у вас пробное занятие по битбоксу. Не забудьте добавить ребенка в группу, чтобы он успел познакомиться и группой и учителем. 

Хорошего урока 💥
"""