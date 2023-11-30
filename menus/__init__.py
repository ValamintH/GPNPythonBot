from telebot import types
from models.users import User
from models.products import Product
from db import SessionLocal

menu = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton("О подразделении", callback_data="g info")
btn2 = types.InlineKeyboardButton("FAQ", callback_data="g faq")
btn3 = types.InlineKeyboardButton("Магазин барелек", callback_data="g to_shop")
menu.add(btn1, btn2, btn3)

shop = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton("Как получить барельки нефти?", callback_data="g how_to_get_barrels")
btn2 = types.InlineKeyboardButton("Каталог товаров", callback_data="g catalog")
btn3 = types.InlineKeyboardButton("Вернуться в меню", callback_data="g to_menu")
shop.add(btn2, btn3, btn1, row_width=2)

admenu = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton("Список пользователей", callback_data="ad users")
btn2 = types.InlineKeyboardButton("Список товаров", callback_data="ad products")
btn3 = types.InlineKeyboardButton("Список заказов", callback_data="ad orders")
admenu.add(btn1, btn2, btn3)


def get_user_list_markup():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("В меню", callback_data="ad menu")
    markup.add(button1, row_width=1)
    with SessionLocal() as session:
        res = session.query(User).order_by(User.is_admin, User.first_name).all()
        for usr in res:
            button = types.InlineKeyboardButton(usr.__repr__(), callback_data="ad_user data " + str(usr.id))
            markup.add(button, row_width=1)

    return markup


def get_product_list_markup():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("В меню", callback_data="ad menu")
    button2 = types.InlineKeyboardButton("Создать товар", callback_data="ad_create_prod")
    markup.add(button1, button2, row_width=2)
    with SessionLocal() as session:
        res = session.query(Product).order_by(Product.name).all()
        for prod in res:
            button = types.InlineKeyboardButton(prod.__repr__(), callback_data="ad_prod data " + str(prod.id))
            markup.add(button, row_width=1)

    return markup


def get_user_editor_markup(user: User):
    markup = types.InlineKeyboardMarkup()
    user_return = types.InlineKeyboardButton("В меню", callback_data="ad menu")
    user_id = str(user.id)
    if user.is_admin:
        button1 = types.InlineKeyboardButton("Понизить пользователя", callback_data="ad_user down " + user_id)
    else:
        button1 = types.InlineKeyboardButton("Повысить пользователя", callback_data="ad_user up " + user_id)
    button2 = types.InlineKeyboardButton("Удалить пользователя", callback_data="ad_user delete " + user_id)
    markup.add(user_return, button1, button2, row_width=1)

    return markup


def get_prod_editor_markup(prod_id: str):
    markup = types.InlineKeyboardMarkup()
    prod_return = types.InlineKeyboardButton("В меню", callback_data="ad menu")
    button1 = types.InlineKeyboardButton("Редактировать имя", callback_data="ad_prod name " + prod_id)
    button2 = types.InlineKeyboardButton("Редактировать цену", callback_data="ad_prod price " + prod_id)
    button3 = types.InlineKeyboardButton("Редактировать описание", callback_data="ad_prod desc " + prod_id)
    button4 = types.InlineKeyboardButton("Удалить товар", callback_data="ad_prod delete " + prod_id)
    markup.add(prod_return, button1, button2, button3, button4, row_width=1)

    return markup


def get_catalog_markup():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("В магазин", callback_data="g to_shop")
    markup.add(button1, row_width=1)
    with SessionLocal() as session:
        res = session.query(Product).order_by(Product.name).all()
        for prod in res:
            desc = prod.name + ", Цена: " + str(prod.price)
            if prod.description:
                desc += ", Описание: " + prod.description
            button = types.InlineKeyboardButton(desc, callback_data="g_prod data " + str(prod.id))
            markup.add(button, row_width=1)

    return markup


def get_prod_menu_markup(prod_id: str):
    markup = types.InlineKeyboardMarkup()
    prod_return = types.InlineKeyboardButton("В каталог", callback_data="g catalog")
    button1 = types.InlineKeyboardButton("Купить товар", callback_data="g_prod buy " + prod_id)
    markup.add(prod_return, button1, row_width=1)

    return markup
