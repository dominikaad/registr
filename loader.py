from Scripts.bottle import route
from aiogram import Bot, Dispatcher, Router
from config.token import TOKEN
import sqlite3

con = sqlite3.connect("data/data.db")
cursor = con.cursor()

admin_id = [1375619533]

router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)