# bot.py

import os
import logging
import csv
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# --- Базовая настройка ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Не найден TELEGRAM_BOT_TOKEN в файле .env. Пожалуйста, установите его.")

# --- Состояния для диалога ---
GET_NAME, GET_EMAIL, GET_MESSAGE = range(3)
CONTACT_FILE = "contacts.csv"

# --- Тексты для бота (на русском языке) ---
ПРИВЕТСТВЕННОЕ_СООБЩЕНИЕ = (
    "👋 Добро пожаловать в Montech IT Бот!\n\n"
    "Мы ваши партнеры в создании потрясающих цифровых решений. "
    "Используйте команды ниже, чтобы узнать о нас больше.\n\n"
    "/services - Посмотреть, что мы предлагаем\n"
    "/portfolio - Ознакомиться с нашими работами\n"
    "/contact - Связаться с нами\n\n"
    "Для полного списка команд используйте /help."
)

О_НАС_ТЕКСТ = (
    "Montech — это прогрессивный стартап, посвященный предоставлению передовых решений "
    "в области ИИ и веб-разработки. Наша миссия — расширять возможности бизнеса, "
    "создавая интеллектуальные, эффективные и удобные приложения."
)

УСЛУГИ_ТЕКСТ = (
    "Мы предлагаем широкий спектр услуг для воплощения ваших идей в жизнь:\n\n"
    "🤖 **ИИ и чат-боты:** Пользовательские ИИ-ассистенты и интеллектуальные чат-боты.\n"
    "🌐 **Веб-разработка:** Высокопроизводительные веб-сайты и целевые страницы.\n"
    "📈 **Автоматизация:** Оптимизация бизнес-процессов с помощью технологий.\n\n"
    "Готовы начать проект? Используйте команду /contact!"
)

ПОРТФОЛИО_ТЕКСТ = (
    "Здесь вы можете увидеть примеры наших лучших работ:\n\n"
    "🔗 **Проект 1:** [Ссылка на ваш проект]\n"
    "🔗 **Проект 2:** [Ссылка на ваш проект]\n"
    "🔗 **Проект 3:** [Ссылка на ваш проект]\n\n"
    "Мы гордимся каждым созданным нами решением!"
)

ПОМОЩЬ_ТЕКСТ = (
    "Вот список всех доступных команд:\n\n"
    "/start - Начальное приветствие\n"
    "/about - Узнать больше о нашей компании\n"
    "/services - Список наших услуг\n"
    "/portfolio - Посмотреть наши работы\n"
    "/contact - Отправить нам сообщение\n"
    "/cancel - Отменить текущую операцию (например, отправку сообщения)"
)

# --- Обработчики команд ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(ПРИВЕТСТВЕННОЕ_СООБЩЕНИЕ)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(О_НАС_ТЕКСТ)

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(УСЛУГИ_ТЕКСТ, parse_mode='Markdown')

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(ПОРТФОЛИО_ТЕКСТ, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(ПОМОЩЬ_ТЕКСТ)

# --- Обработчик для любых других текстовых сообщений ---
async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветствует пользователя по имени, если команда не распознана."""
    first_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"Здравствуйте, {first_name}! 👋\n"
        f"Я не совсем понял ваш запрос. Пожалуйста, используйте /help, чтобы увидеть список доступных команд."
    )

# --- Диалог для /contact ---

async def contact_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['contact_info'] = {}
    await update.message.reply_text(
        "Отлично! Давайте свяжемся. Сначала, как ваше полное имя?"
    )
    return GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_name = update.message.text
    context.user_data['contact_info']['name'] = user_name
    await update.message.reply_text(
        f"Спасибо, {user_name}. Теперь, какой ваш адрес электронной почты?"
    )
    return GET_EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_email = update.message.text
    context.user_data['contact_info']['email'] = user_email
    await update.message.reply_text(
        "Отлично. Наконец, пожалуйста, введите сообщение, которое вы хотите нам отправить."
    )
    return GET_MESSAGE

def save_contact_to_csv(data: dict):
    file_exists = os.path.isfile(CONTACT_FILE)
    with open(CONTACT_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'email', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
    logger.info(f"Контактная информация сохранена в {CONTACT_FILE}")

async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_message = update.message.text
    context.user_data['contact_info']['message'] = user_message
    save_contact_to_csv(context.user_data['contact_info'])
    await update.message.reply_text(
        "✅ Спасибо! Мы получили ваше сообщение и скоро с вами свяжемся."
    )
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Операция отменена. Вы можете начать заново с /contact в любое время."
    )
    context.user_data.clear()
    return ConversationHandler.END

# --- Основная функция запуска бота ---
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("contact", contact_start)],
        states={
            GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GET_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            GET_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("services", services))
    application.add_handler(CommandHandler("portfolio", portfolio))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)
    
    # Этот обработчик должен быть добавлен одним из последних
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greet_user))

    logger.info("Бот запускается...")
    application.run_polling()

if __name__ == "__main__":
    main()