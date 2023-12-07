from telebot import types, TeleBot
from db import SessionLocal
from models.users import User
from models.products import Product
from models.orders import Order
from menus import admenu, get_prod_editor_markup, get_user_editor_markup, get_order_editor_markup
from menus import get_product_list_markup, get_user_list_markup, get_order_list_markup


def admin_menu_init(message: types.Message, bot: TeleBot):
    user = message.from_user
    with SessionLocal() as session:
        res = session.query(User).filter(User.id == user.id).first()
        if res and res.is_admin:
            bot.send_message(user.id, "Добро пожаловать в меню администратора", reply_markup=admenu)
        else:
            bot.send_message(user.id, "Недостаточно прав")


def add_barrels(message: types.Message, bot: TeleBot):
    user = message.from_user
    target_username = message.text.split()[1]
    barrels = message.text.split()[2]
    if not barrels.isdigit() or target_username[0] != '@':
        bot.send_message(user.id, "Неверный формат команды\nПиши /add [ник получателя] [число баррелек]")
        return

    with SessionLocal() as session:
        admin = session.query(User).filter(User.id == user.id).first()
        if admin and admin.is_admin:
            target_user = session.query(User).filter(User.username == target_username[1:]).first()
            if not target_user:
                bot.send_message(user.id, "Такого пользователя нет в базе")
            else:
                target_user.barrels += int(barrels)
                session.commit()
                bot.send_message(user.id, "Баррельки начислены")
        else:
            bot.send_message(user.id, "Недостаточно прав")


def admin_menu(call: types.CallbackQuery, bot: TeleBot):
    """
    callback data format: ad [data]
    """
    data = call.data.partition(' ')[2]
    user = call.from_user

    if data == "menu":
        bot.send_message(user.id, "Меню администратора", reply_markup=admenu)
    elif data == "users":
        markup = get_user_list_markup()
        bot.send_message(user.id, "Выбери пользователя для редактирования", reply_markup=markup)
    elif data == "products":
        markup = get_product_list_markup()
        bot.send_message(user.id, "Выбери товар для редактирования", reply_markup=markup)
    elif data == "orders":
        markup = get_order_list_markup()
        bot.send_message(user.id, "Выбери заказ для редактирования", reply_markup=markup)

    bot.answer_callback_query(call.id)


def user_editor(call: types.CallbackQuery, bot: TeleBot):
    """
    callback data format: ad_user [command] [db_user_id]
    """
    command = call.data.split()[1]
    user = call.from_user
    db_user_id = call.data.split()[2]
    out_str = "\nВыбери, что хочешь сделать"

    with SessionLocal() as session:
        res = session.query(User).filter(User.id == db_user_id).first()
        if command == "down":  # о т т е с т и т ь
            res.is_admin = False
            session.commit()
            out_str = "\nПользователь понижен до обычного"
        elif command == "up":
            res.is_admin = True
            session.commit()
            out_str = "\nПользователь повышен до администратора"
        elif command == "delete":
            session.delete(res)
            session.commit()
            markup = get_user_list_markup()
            bot.send_message(user.id, "Пользователь удален", reply_markup=markup)
            bot.answer_callback_query(call.id)
            return

        markup = get_user_editor_markup(res)
        bot.send_message(user.id, res.__repr__() + out_str, reply_markup=markup)

    bot.answer_callback_query(call.id)


def create_product(call: types.CallbackQuery, bot: TeleBot):
    """
    callback data format: ad_create_prod
    """
    user = call.from_user
    msg = "Введи данные для нового товара одним сообщением в формате:\n\n" \
          "имя товара\n" \
          "цена товара (в баррельках)\n" \
          "описание товара (опционально)\n" \
          "\nТакже можно приложить фотографию с изображением товара (сжимать при отправке)"
    bot.send_message(user.id, msg)
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, create_product_msg_handler, bot)

    bot.answer_callback_query(call.id)


def create_product_msg_handler(message: types.Message, bot: TeleBot):
    text = message.text.split('\n') if message.text else message.caption.split('\n')
    user = message.from_user
    if not (len(text) == 2 or len(text) == 3) or not text[1].isdigit():
        markup = get_product_list_markup()
        bot.send_message(user.id, "Неверный формат данных", reply_markup=markup)
        return

    with SessionLocal() as session:
        old_prod = session.query(Product).filter(Product.name == text[0]).first()
        if old_prod:
            markup = get_product_list_markup()
            bot.send_message(user.id, "Товар с таким именем уже существует", reply_markup=markup)
            return

        image = None
        if len(message.photo) > 2:
            image = message.photo[2].file_id

        new_prod = Product(
            name=text[0],
            description=text[2] if len(text) == 3 else None,
            price=int(text[1]),
            image=image,
        )
        session.add(new_prod)
        session.commit()
        markup = get_prod_editor_markup(str(new_prod.id))
        if image:
            bot.send_photo(user.id, image)
        bot.send_message(user.id, new_prod.__repr__() + "\nСоздан новый товар", reply_markup=markup)


def product_editor(call: types.CallbackQuery, bot: TeleBot):
    """
    callback data format: ad_prod [command] [prod_id]
    """
    command = call.data.split()[1]
    user = call.from_user
    prod_id = call.data.split()[2]
    out_str = "\nВыбери, что хочешь сделать"

    with SessionLocal() as session:
        res = session.query(Product).filter(Product.id == prod_id).first()
        if command == "name":
            out_str = "\nСделаем эту функцию потом"
        elif command == "price":
            out_str = "\nСделаем эту функцию потом"
        elif command == "desc":
            out_str = "\nСделаем эту функцию потом"
        elif command == "delete":
            session.delete(res)
            session.commit()
            markup = get_product_list_markup()
            bot.send_message(user.id, "Товар удален", reply_markup=markup)
            bot.answer_callback_query(call.id)
            return

        markup = get_prod_editor_markup(prod_id)
        if res.image:
            bot.send_photo(user.id, res.image)
        bot.send_message(user.id, res.__repr__() + out_str, reply_markup=markup)

    bot.answer_callback_query(call.id)


def order_editor(call: types.CallbackQuery, bot: TeleBot):
    """
    callback data format: ad_order [command] [order_id]
    """
    command = call.data.split()[1]
    user = call.from_user
    order_id = call.data.split()[2]
    out_str = "\nВыбери, что хочешь сделать"

    with SessionLocal() as session:
        res = session.query(Order).filter(Order.id == order_id).first()
        if command == "close":
            session.delete(res)
            session.commit()
            markup = get_order_list_markup()
            bot.send_message(user.id, "Заказ закрыт", reply_markup=markup)
        else:
            markup = get_order_editor_markup(order_id)
            bot.send_message(user.id, res.__repr__() + out_str, reply_markup=markup)

    bot.answer_callback_query(call.id)
