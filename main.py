import telebot

from handlers.admin_handlers import admin_menu_init, admin_menu, user_editor, order_editor
from handlers.admin_handlers import product_editor, create_product, add_barrels
from handlers.user_handlers import start_message, general_menus_handler, product_menu

TOKEN = "6765589159:AAF240vsNvP-I-AR-EEGcVlXzm2HaRxbb_M"

bot = telebot.TeleBot(TOKEN)
bot.register_message_handler(start_message, commands=["start"], pass_bot=True)
bot.register_message_handler(admin_menu_init, commands=["admenu"], pass_bot=True)
bot.register_message_handler(add_barrels, commands=["add"], pass_bot=True)


@bot.message_handler(content_types=["text"])
def default_handler(message):
    bot.send_message(message.from_user.id, "Неизвестная команда. Чтобы начать, напиши \\start")


def filter_call(call, filter_str):
    return call.data.partition(' ')[0] == filter_str


bot.register_callback_query_handler(general_menus_handler, func=lambda call: filter_call(call, "g"), pass_bot=True)
bot.register_callback_query_handler(product_menu, func=lambda call: filter_call(call, "g_prod"), pass_bot=True)

bot.register_callback_query_handler(admin_menu, func=lambda call: filter_call(call, "ad"), pass_bot=True)
bot.register_callback_query_handler(user_editor, func=lambda call: filter_call(call, "ad_user"), pass_bot=True)
bot.register_callback_query_handler(product_editor, func=lambda call: filter_call(call, "ad_prod"), pass_bot=True)
bot.register_callback_query_handler(order_editor, func=lambda call: filter_call(call, "ad_order"), pass_bot=True)
bot.register_callback_query_handler(
    create_product,
    func=lambda call: filter_call(call, "ad_create_prod"),
    pass_bot=True
)


bot.polling(none_stop=True, interval=0)
