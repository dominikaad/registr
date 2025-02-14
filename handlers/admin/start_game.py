from aiogram.types import Message
from loader import router, cursor, con, admin_id, Bot
from aiogram.filters import Command
import random

@router.message(Command('start_game'))
async def game_start(message: Message, bot: Bot):
    id_user = message.chat.id
    if not id_user in admin_id:
        await message.answer(text='Вы не являетесь админом')
    else:
        cursor.execute("SELECT * FROM users ")
        data = cursor.fetchall()
        random.shuffle(data)
        file = open('data/prize.txt', 'r', encoding='utf-8')
        prize = file.read()
        text = ('Розыгрыш завершен!\n'
                'Поздравляем победителей с пободой:\n'
                )
        for i in range(1):
            text += f'{data[i][1]} - {prize}\n'
        for user in data:
            try:
                await bot.send_message(text=text, chat_id=user[0])

            except:
                pass
        cursor.execute(
                    "update start_reg set status=(?) ", ('False',))
        cursor.execute(
            "DELETE FROM users")
        con.commit()
