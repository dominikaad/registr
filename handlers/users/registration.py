from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loader import router, cursor, con
from aiogram import F
from aiogram import types
import sqlite3
from aiogram import Bot, Dispatcher, Router

class Form_reg(StatesGroup):
    fio = State()
    numbers = State()
    email = State()
    age = State()

@router.message(Command('cancel'))
async def cancel_reg (message: Message):
    cursor.execute(
        "DELETE FROM users")
    con.commit()
    await message.answer('Регистрация удалена')

@router.message(Command('return'))
async def cancel_reg (message: Message, state: FSMContext):
    a = await state.get_state()
    b = a.split(':')[1]
    if b == 'age':
        await state.set_state(Form_reg.fio)
        await message.answer('Для начала введите ФИО полностью', reply_markup=types.ReplyKeyboardRemove())
    if b == 'numbers':
        await state.set_state(Form_reg.age)
        await message.answer('А теперь введите свой возраст')
    if b == 'email':
        await state.set_state(Form_reg.numbers)
        await message.answer('А теперь введите свой номер телефона (начиная с +)')

@router.message(F.text == 'Регистрация')
async def reg_start(message: Message, state: FSMContext):
    id_user = message.chat.id
    cursor.execute("SELECT id FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    if len(a)>0:
        await message.answer(text='Вы уже зарегистрированы')
    else:
        cursor.execute("SELECT status FROM start_reg ")
        b = cursor.fetchall()
        if b == 'False':
            await message.answer(text='Регистрация завершена')
        else:
            await state.set_state(Form_reg.fio)
            await message.answer('Для начала введите ФИО полностью', reply_markup=types.ReplyKeyboardRemove())

@router.message(Form_reg.fio)
async def get_fio(message: Message, state: FSMContext):
    a = await state.get_state()
    print(a.split(':')[1])
    await state.update_data(fio=message.text)
    if message.text.count(' ') + 1 < 2:
        await message.answer('Неверный ввод')
        return
    await state.set_state(Form_reg.age)
    await message.answer('А теперь введите свой возраст')

@router.message(Form_reg.age)
async def get_fio(message: Message, state: FSMContext):
    a = await state.get_state()
    await state.update_data(age=message.text)
    if int(message.text) < 14:
        await message.answer('Неверный ввод')
        return
    await state.set_state(Form_reg.numbers)
    await message.answer('А теперь введите свой номер телефона (начиная с +)')

@router.message(Form_reg.numbers)
async def get_fio(message: Message, state: FSMContext):
    a = await state.get_state()
    await state.update_data(numbers=message.text)
    print(message.text)
    if len(message.text) < 13 or message.text.count('+375') < 1:
        await message.answer('Неверный ввод')
        return
    await state.set_state(Form_reg.email)
    await message.answer('А теперь введите свою почту')

@router.message(Form_reg.email)
async def get_fio(message: Message, state: FSMContext):
    a = await state.get_state()
    await state.update_data(email=message.text)
    if message.text.count('@') != 1:
        await message.answer('Неверный ввод')
        return
    data = await state.get_data()
    fio = data['fio']
    age = data['age']
    numbers = data['numbers']
    email = data['email']
    id_user = message.chat.id
    await state.clear()
    cursor.execute(
        "INSERT INTO users (id, fio, age, numbers, email) VALUES (?, ?, ?, ?, ?)",
        [id_user, fio, age, numbers, email])
    con.commit()
    await message.answer('Регистрация успешно завершена')

@router.message(Command('cancel'))
async def fun_start (message: Message):
    cursor.execute(
        "DELETE FROM users")
    con.commit()