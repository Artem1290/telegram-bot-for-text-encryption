import telebot
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


user_keys = {}

key_mason = {
    'A': '@', 'B': '#', 'C': '$', 'D': '%', 'E': '&', 'F': '*', 'G': '(',
    'H': ')', 'I': '!', 'J': '^', 'K': '_', 'L': '+', 'M': '~', 'N': '`',
    'O': '-', 'P': '=', 'Q': '{', 'R': '}', 'S': '[', 'T': ']', 'U': ';',
    'V': ':', 'W': '"', 'X': "'", 'Y': '<', 'Z': '>', ' ': ' '
}

key_mason_rev = {v: k for k, v in key_mason.items()}

def mason_encrypt(text):
    return "".join(key_mason.get(char.upper(), char) for char in text)

def mason_decrypt(text):
    return "".join(key_mason_rev.get(char, char) for char in text)


def caesar_encrypt(txt, shift=3):
    result = ""
    for char in txt:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(txt, shift=3):
    result = ""
    for char in txt:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result


TOKEN = 'YOUR TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я твій новий бот 😃")

    #logs
    logging.info(f"User {message.from_user.username} (id={message.from_user.id}) used /start command")



@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,
                 "Команди:\n"
                 "/start — початок роботи\n"
                 "/help — допомога\n"
                 "/cesar_encrypt <текст> — шифрування Цезарем\n"
                 "/cesar_decrypt <текст> — розшифрування Цезарем\n"
                 "/set_key — встановити ключ Цезаря\n"
                 "/mason_encrypt <текст> — шифрування масонським шрифтом\n"
                 "/mason_decrypt <текст> — розшифрування масонським шрифтом")

    #logs
    logging.info(f"User {message.from_user.username} (id={message.from_user.id}) used /help command")

# Масонський шифр
@bot.message_handler(commands=['mason_encrypt'])
def mason_encrypt_text(message):
    text = message.text[14:]
    if not text:
        bot.reply_to(message, "Введи текст для шифрування масонським шрифтом. Наприклад: /mason_encrypt hello")
        return

    encrypted = mason_encrypt(text)

    #logs
    logging.info(f"User {message.from_user.username} (id={message.from_user.id}) used /mason_encrypt with text: {text}")
    logging.info(f"Result for user {message.from_user.id}: {encrypted}")
    bot.reply_to(message, f"Зашифровано: {encrypted}")

@bot.message_handler(commands=['mason_decrypt'])
def mason_decrypt_text(message):
    text = message.text[14:]
    if not text:
        bot.reply_to(message, "Введи текст для розшифрування масонським шрифтом. Наприклад: /mason_decrypt @#%-")
        return

    #logs
    decrypted = mason_decrypt(text)
    logging.info(f"User {message.from_user.username} (id={message.from_user.id}) used /mason_decrypt with text: {text}")
    logging.info(f"Result for user {message.from_user.id}: {decrypted}")
    bot.reply_to(message, f"Розшифровано: {decrypted}")


# Цезар
@bot.message_handler(commands=['cesar_encrypt'])
def encrypt_text(message):
    text = message.text[15:]
    if not text:
        bot.reply_to(message, "Будь ласка, введи текст для шифрування.")
        return

    shift = user_keys.get(message.from_user.id, 3)
    encrypted = caesar_encrypt(text, shift)

    #logs
    logging.info(f"User {message.from_user.username} (id={message.from_user.id}) used /cesar_encrypt with text: {text}")
    logging.info(f"Result for user {message.from_user.id}: {encrypted}")

    bot.reply_to(message, f"Зашифровано: {encrypted}")

@bot.message_handler(commands=['cesar_decrypt'])
def decrypt_text(message):
    text = message.text[15:]
    if not text:
        bot.reply_to(message, "Будь ласка, введи текст для розшифрування.")
        return

    shift = user_keys.get(message.from_user.id, 3)
    decrypted = caesar_decrypt(text, shift)

    #logs
    logging.info(f"User {message.from_user.username} (id={message.from_user.id}) used /cesar_decrypt with text: {text}")
    logging.info(f"Result for user {message.from_user.id}: {decrypted}")

    bot.reply_to(message, f"Розшифровано: {decrypted}")


@bot.message_handler(commands=['set_key'])
def set_key(message):
    bot.reply_to(message, "Введи число для ключа шифрування:")
    bot.register_next_step_handler(message, save_key)


def save_key(message):
    try:
        key = int(message.text)
        user_keys[message.from_user.id] = key
        bot.reply_to(message, f"Ключ успішно встановлено: {key}")

        # logs
        logging.info(f"User {message.from_user.username} (id={message.from_user.id}) set Caesar key: {key}")

    except ValueError:
        bot.reply_to(message, "Введи число!")
        logging.warning(f"User {message.from_user.username} (id={message.from_user.id}) tried to set invalid key: {message.text}")


bot.polling()
