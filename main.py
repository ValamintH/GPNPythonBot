import telebot
from telebot import types
from db import SessionLocal
from users import User

bot = telebot.TeleBot('6765589159:AAF240vsNvP-I-AR-EEGcVlXzm2HaRxbb_M')

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_btn1 = types.KeyboardButton("О подразделении")
menu_btn2 = types.KeyboardButton("FAQ")
menu_btn3 = types.KeyboardButton("Магазин барелек")
menu_btn4 = types.KeyboardButton("Вернуться в меню")
menu.add(menu_btn1, menu_btn2, menu_btn3)

shop = types.ReplyKeyboardMarkup(resize_keyboard=True)
shop_btn1 = types.KeyboardButton("Как получить барельки нефти?")
shop_btn2 = types.KeyboardButton("Каталог товаров")
shop_btn3 = types.KeyboardButton("Вернуться в меню")
shop.add(shop_btn1, shop_btn2, shop_btn3)


@bot.message_handler(commands=["start"])
def start_message(message):
    user = message.from_user
    with SessionLocal() as session:
        res = session.query(User).filter(User.id == user.id).first()
        if not res:
            new_user = User(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
            )
            session.add(new_user)
            session.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать")
    markup.add(btn1)
    bot.send_message(user.id, "Привет! Я Газпром-бот. Начнем работу?", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    txt = message.text
    if txt == "Начать" or txt == "Меню" or txt == "Вернуться в меню":
        bot.send_message(message.from_user.id, "Выбери интересующую опцию из меню", reply_markup=menu)
    elif txt == "О подразделении":
        bot.send_message(message.from_user.id, "[информация о подразделении]", reply_markup=menu)
    elif txt == "FAQ":
        bot.send_message(message.from_user.id, "[FAQ]", reply_markup=menu)

    elif txt == "Магазин барелек":
        user = message.from_user
        with SessionLocal() as session:
            res = session.query(User).filter(User.id == user.id).first()
            bot.send_message(user.id,
                             "Добро пожаловать в магазин барелек нефти, здесь можно купить [что-то] за барельки нефти\n"
                             f"\nТекущий баланс: {res.barrels} барелек",
                             reply_markup=shop)
    elif txt == "Как получить барельки нефти?":
        bot.send_message(message.from_user.id, "Барельки нефти можно получить за [что-то]", reply_markup=shop)
    elif txt == "Каталог товаров":
        bot.send_message(message.from_user.id, "[каталог или ссылка на него]", reply_markup=shop)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню")
        markup.add(btn1)
        bot.send_message(message.from_user.id,
                         "Неизвестная команда. Чтобы вернуться в меню, напиши Меню",
                         reply_markup=markup)


bot.polling(none_stop=True, interval=0)
