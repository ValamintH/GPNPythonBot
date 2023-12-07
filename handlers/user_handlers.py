from db import SessionLocal
from models.users import User
from models.products import Product
from models.orders import Order
from menus import menu, shop, get_catalog_markup, get_prod_menu_markup
from telebot import types, TeleBot


def start_message(message: types.Message, bot: TeleBot):
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
        else:
            res.first_name = user.first_name
            res.last_name = user.last_name
            res.username = user.username

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Начать", callback_data="g to_menu")
    markup.add(btn1)
    bot.send_message(user.id, "Привет! Я Газпром-бот. Начнем работу?", reply_markup=markup)


def general_menus_handler(call: types.CallbackQuery, bot: TeleBot):
    """
    callback data format: g [data]
    """
    data = call.data.partition(' ')[2]
    user = call.from_user

    if data == "to_menu":
        bot.send_message(user.id, "Выбери интересующую опцию из меню", reply_markup=menu)
    elif data == "info":
        bot.send_message(user.id, "[информация о подразделении]", reply_markup=menu)
    elif data == "faq":
        bot.send_message(user.id, "[FAQ]", reply_markup=menu)

    elif data == "to_shop":
        resp_str = "Добро пожаловать в магазин баррелек нефти, здесь можно купить [что-то] за баррельки нефти\n"
        with SessionLocal() as session:
            res = session.query(User).filter(User.id == user.id).first()
            if res:
                resp_str += f"\nТекущий баланс: {res.barrels} баррелек"
        bot.send_message(user.id, resp_str, reply_markup=shop)
    elif data == "how_to_get_barrels":
        bot.send_message(user.id, "Баррельки нефти можно получить за [что-то]", reply_markup=shop)
    elif data == "catalog":
        markup = get_catalog_markup()
        bot.send_message(user.id, "Список доступных для покупки товаров", reply_markup=markup)

    bot.answer_callback_query(call.id)


def product_menu(call: types.CallbackQuery, bot: TeleBot):
    """
    callback data format: g_prod [command] [prod_id]
    """
    command = call.data.split()[1]
    user = call.from_user
    prod_id = call.data.split()[2]

    with SessionLocal() as session:
        db_prod = session.query(Product).filter(Product.id == prod_id).first()
        out_str = db_prod.name + "\nЦена: " + str(db_prod.price)
        if db_prod.description:
            out_str += "\nОписание: " + db_prod.description
        if command == "buy":
            db_user = session.query(User).filter(User.id == user.id).first()
            if db_user.barrels >= db_prod.price:
                new_order = Order(
                    username=db_user.username,
                    product_name=db_prod.name,
                )
                session.add(new_order)
                db_user.barrels -= db_prod.price
                session.commit()
                out_str += "\n\nТовар куплен! Администратор свяжется с вами для его отправки"
            else:
                out_str += f"\n\nНедостаточно баррелек для покупки товара. Баланс: {db_user.barrels}"

        markup = get_prod_menu_markup(prod_id)
        if db_prod.image:
            bot.send_photo(user.id, db_prod.image)
        bot.send_message(user.id, out_str, reply_markup=markup)

    bot.answer_callback_query(call.id)

