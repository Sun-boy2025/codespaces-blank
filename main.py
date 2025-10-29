import os
import logging
from telebot import types
from dotenv import load_dotenv

# Импорт Lite-версии модели (название класса зависит от вашей фактической установки)
from langchain_gigachat import GigaChat

load_dotenv()

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
GIGACHAT_KEY = os.getenv("GIGACHAT_KEY")

# Для pyTelegramBotAPI (telebot)
import telebot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_kids_article(topic):
    """Генерирует адаптированную статью через GigaChat Lite"""
    try:
        llm = GigaChat(
            credentials=GIGACHAT_KEY,
            verify_ssl_certs=False,  # Обычно SSL нужен, меняйте если реально требуется
            scope="GIGACHAT_API_PERS"
        )
        prompt = (
            f"Напиши статью на тему '{topic}' для детей 12 лет. "
            "Используй простой и живой язык, яркие примеры, поясни сложные слова, добавь интересные факты."
        )
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        logging.error(f"Ошибка генерации статьи: {e}")
        return "Извините, не удалось сгенерировать статью."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
        "Привет! Отправь мне тему, и я сгенерирую статью для детей 12 лет.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    topic = message.text.strip()
    bot.send_message(message.chat.id, "Генерирую статью...")
    article = generate_kids_article(topic)
    bot.send_message(message.chat.id, article)

if __name__ == '__main__':
    bot.polling(none_stop=True)
