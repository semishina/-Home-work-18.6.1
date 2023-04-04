import telebot
from Config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f'Приветствую, {message.chat.username}! \n \
\nЧтобы начать работу, введите команду боту в следующем \n\
формате (через пробел, с маленькой буквы, без кавычек): \n \
\n<имя валюты>  <в какую валюту перевести>  <количество переводимой валюты> \n\
\nЧтобы получить список доступных валют\nвведите команду /values '
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Количество введеных параметров не соответствует условию!\nПопробуйте еще раз!')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:\
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        total_price = total_base * int(amount)
        text = f'Стоимость {amount} {quote} в {base} составляет: {total_price}'
        bot.send_message(message.chat.id, text)

bot.polling()
