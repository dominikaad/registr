from aiogram.types import Message
from loader import router
from aiogram import F

@router.message(F.text == 'Информация')
async def fun_text(message: Message):
    file = open('data/info.txt', 'r',encoding='utf-8')
    text = file.read()
    await message.answer(text=f'{text}')