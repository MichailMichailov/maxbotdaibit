from maxapi.types import ButtonsPayload, RequestContactButton
from config import text_start_btn

def start_keyboard():
    return ButtonsPayload(
        buttons=[
            [RequestContactButton(text=text_start_btn)]
        ]
    ).pack()