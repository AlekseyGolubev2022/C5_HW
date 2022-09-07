import telebot
from extensions import APIException, Currencies
import settings

bot = telebot.TeleBot(settings.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = (
        'Бот вычисляет цену заданного количества одной валюты в ' +
        '\nдругой (округление до сотых).' +
        '\nФормат запроса (текстовое сообщение, через пробел): ' +
        '\nполучаемая валюта, конвертируемая валюта, ' +
        '\nколичество получаемой валюты.' +
        '\n\nДоступные команды: ' +
        '\n/start или /help - справка по программе,' +
        '\n/values - список доступных валют'
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def handle_start_help(message):
    names = '\n'.join(v for v in Currencies.names.values())
    text = f'Cписок доступных валют: \n{names}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):

    # Преобразование формата и валидация введенных данных
    try:
        params = message.text.split()
        if len(params) != 3:
            raise APIException('Неверный ввод. Пример: евро рубль 100')
        names = Currencies.names.values()
        if not ({params[0], params[1]} <= set(names)):
            text = f'Неверный ввод валют, доступны: {" ".join(names)}'
            raise APIException(text)
        try:
            params[2] = round(float(params[2].replace(',', '.')), 2)
        except Exception:
            raise APIException('Неверный ввод суммы.')

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        text = f'Ошибка на стороне сервиса - {type(e)} {e}'
        bot.reply_to(message, text)
    else:
        base, quote, amount = params
        price = amount if base == quote else 0
        if amount != 0:
            price = Currencies.get_price(base, quote, abs(amount))
        if amount < 0:
            price = - price
        text = f'Цена за {amount} ({base}) = {price} ({quote})'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
