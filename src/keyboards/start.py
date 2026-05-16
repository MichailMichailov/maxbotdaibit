from config import text_start_btn
from maxapi.types import ButtonsPayload, CallbackButton

def start_keyboard():
    return ButtonsPayload(
        buttons=[[CallbackButton(text=text_start_btn, payload="start_click")]]
    ).pack()