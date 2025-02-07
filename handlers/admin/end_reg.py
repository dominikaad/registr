from aiogram.types import Message
from loader import router, cursor, con, admin_id
from aiogram.filters import Command

@router.message(Command('end_reg'))
async def reg_end(message: Message):
    id_user = message.chat.id
    if not id_user in admin_id:
        await message.answer(text='Вы не являетесь админом')
    else:
        cursor.execute(
                "UPDATE start_reg SET status=('False') ")
        con.commit()
        await message.answer(text='Регистрация закрыта')