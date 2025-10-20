import os
import logging
from dotenv import load_dotenv
load_dotenv()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import httpx
from handlers import parse_uzbek_russian_message

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_URL = os.getenv('ENV_BACKEND_URL', 'http://localhost:8000')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'http://localhost:3000')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    
    # Check if user is authenticated
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{BACKEND_URL}/api/auth/status/{user_id}')
            is_authenticated = response.json().get('authenticated', False)
        except:
            is_authenticated = False
    
    if is_authenticated:
        await update.message.reply_text(
            "🎉 Salom! Men sizning shaxsiy yordamchingizman.\n"
            "👋 Привет! Я ваш персональный помощник.\n\n"
            "Menga xabar yozing va men:\n"
            "📅 Google Calendar'ga voqea qo'shaman\n"
            "📝 Google Keep'ga eslatma yarataman\n\n"
            "Напишите мне, и я:\n"
            "📅 Добавлю событие в Google Calendar\n"
            "📝 Создам заметку в Google Keep\n\n"
            "Misol/Пример:\n"
            "• 'Ertaga soat 3 da uchrashuv' → Calendar\n"
            "• 'Non va sut sotib olish' → Keep"
        )
    else:
        keyboard = [[InlineKeyboardButton("🔐 Google bilan kirish / Войти через Google", url=f"{WEBAPP_URL}?user_id={user_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "👋 Assalomu alaykum! Google hisobingizni ulash kerak.\n"
            "👋 Здравствуйте! Необходимо подключить ваш Google аккаунт.\n\n"
            "Tugmani bosing / Нажмите кнопку:",
            reply_markup=reply_markup
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "📖 Yordam / Помощь:\n\n"
        "Men tabiiy tilda yozilgan xabarlarni tushunaman:\n"
        "Я понимаю сообщения на естественном языке:\n\n"
        "📅 Calendar uchun / для Calendar:\n"
        "• 'Ertaga soat 14:00 da doktor'\n"
        "• 'Завтра в 14:00 к врачу'\n"
        "• 'Dushanba kuni soat 10 da yig'ilish'\n"
        "• 'В понедельник в 10 собрание'\n\n"
        "📝 Keep uchun / для Keep:\n"
        "• 'Eslatma: non va sut olish'\n"
        "• 'Заметка: купить хлеб и молоко'\n"
        "• 'Kitob o'qishni unutma'\n"
        "• 'Не забыть прочитать книгу'\n\n"
        "Buyruqlar / Команды:\n"
        "/start - Boshlash / Начать\n"
        "/help - Yordam / Помощь\n"
        "/auth - Qayta kirish / Переавторизация\n"
        "/status - Holat / Статус"
    )

async def auth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /auth command"""
    user_id = update.effective_user.id
    keyboard = [[InlineKeyboardButton("🔐 Google bilan kirish / Войти через Google", url=f"{WEBAPP_URL}?user_id={user_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Google hisobingizni ulash uchun tugmani bosing:\n"
        "Нажмите кнопку для подключения Google аккаунта:",
        reply_markup=reply_markup
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    user_id = update.effective_user.id
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{BACKEND_URL}/api/auth/status/{user_id}')
            data = response.json()
            
            if data.get('authenticated'):
                await update.message.reply_text(
                    f"✅ Ulangan / Подключено\n"
                    f"📧 Email: {data.get('email', 'N/A')}\n"
                    f"📅 Calendar: ✅\n"
                    f"📝 Keep: ✅"
                )
            else:
                await update.message.reply_text(
                    "❌ Ulanmagan / Не подключено\n"
                    "/auth buyrug'ini ishga tushiring\n"
                    "Используйте команду /auth"
                )
        except Exception as e:
            logger.error(f"Status check error: {e}")
            await update.message.reply_text("⚠️ Xatolik / Ошибка")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Check authentication
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{BACKEND_URL}/api/auth/status/{user_id}')
            if not response.json().get('authenticated'):
                keyboard = [[InlineKeyboardButton("🔐 Kirish / Войти", url=f"{WEBAPP_URL}?user_id={user_id}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    "⚠️ Avval Google hisobingizni ulang\n"
                    "⚠️ Сначала подключите Google аккаунт",
                    reply_markup=reply_markup
                )
                return
        except Exception as e:
            logger.error(f"Backend error: {e}")
            await update.message.reply_text("⚠️ Backend bilan aloqa yo'q / Нет связи с backend")
    
    # Send typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Parse message
    parsed = parse_uzbek_russian_message(message_text)
    
    if not parsed:
        await update.message.reply_text(
            "🤔 Tushunmadim. Iltimos, aniqroq yozing.\n"
            "🤔 Не понял. Пожалуйста, напишите точнее.\n\n"
            "Yordam uchun /help buyrug'ini ishlating"
        )
        return
    
    # Process based on intent
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if parsed['intent'] == 'calendar':
                response = await client.post(
                    f'{BACKEND_URL}/api/calendar/create',
                    json={
                        'user_id': user_id,
                        'title': parsed['title'],
                        'datetime': parsed['datetime'],
                        'description': parsed.get('description', '')
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    await update.message.reply_text(
                        f"✅ Calendar'ga qo'shildi / Добавлено в Calendar\n\n"
                        f"📅 {parsed['title']}\n"
                        f"🕐 {parsed['datetime']}\n"
                        f"🔗 {data.get('link', '')}"
                    )
                else:
                    raise Exception("Calendar creation failed")
                    
            elif parsed['intent'] == 'note':
                response = await client.post(
                    f'{BACKEND_URL}/api/notes/create',
                    json={
                        'user_id': user_id,
                        'title': parsed['title'],
                        'content': parsed.get('content', '')
                    }
                )
                
                if response.status_code == 200:
                    await update.message.reply_text(
                        f"✅ Keep'ga saqlandi / Сохранено в Keep\n\n"
                        f"📝 {parsed['title']}"
                    )
                else:
                    raise Exception("Note creation failed")
                    
        except Exception as e:
            logger.error(f"API Error: {e}")
            await update.message.reply_text(
                "❌ Xatolik yuz berdi / Произошла ошибка\n"
                "Iltimos qayta urinib ko'ring / Попробуйте еще раз"
            )

def main():
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set!")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("auth", auth_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()