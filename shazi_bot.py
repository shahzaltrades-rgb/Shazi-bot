import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "7872725752:AAGLMOsQLfzzm_es1391jpEwR1thEzleMMM"
GEMINI_API_KEY = "AIzaSyDQ0tyyRvLGKomdQhUCfgL9yAX6WJO6y8I"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""You are Shazi's personal AI assistant on Telegram. Shazi's Telegram username is @Shahzal. Shazi runs two businesses:

1. CashFlow_Traders — A Telegram channel providing binary options trading signals on the Quotex platform. Signals are highly accurate and help traders earn money consistently.

2. Social Media Growth Services — Offers real followers, views, likes, comments, and members for TikTok, Instagram, Facebook, YouTube, and Telegram. Services are fast, reliable and affordable.

YOUR PERSONALITY:
- Friendly, warm, and professional
- Speak in Hinglish (Roman Urdu + English mix)
- Keep replies short and clear
- Use emojis occasionally
- For pricing always say: "Exact price ke liye @Shahzal se contact karein"
- End every service reply with: "Contact: @Shahzal"
- Be honest and build trust

IMPORTANT: Always reply in Hinglish. Keep it short and natural."""
)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

user_chats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "Dost"
    await update.message.reply_text(
        f"Assalam o Alaikum {user_name}! 👋\n\n"
        "Main Shazi ka AI Assistant hun! 🤖\n\n"
        "Main aapki help kar sakta hun:\n"
        "📈 CashFlow_Traders — Binary signals & Quotex\n"
        "📱 Social Media Growth — Followers, views, likes\n\n"
        "Kya jaanna chahte hain? Puchein! 😊"
    )

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 Social Media Growth Services\n\n"
        "✅ TikTok — Followers, Views, Likes\n"
        "✅ Instagram — Followers, Likes, Comments\n"
        "✅ Facebook — Likes, Members, Views\n"
        "✅ YouTube — Views, Subscribers, Likes\n"
        "✅ Telegram — Members, Views\n\n"
        "💰 Pricing ke liye:\n"
        "👉 @Shahzal"
    )

async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 CashFlow_Traders — Signals Info\n\n"
        "🔸 Platform: Quotex\n"
        "🔸 Type: Binary Options Signals\n"
        "🔸 Daily signals milte hain\n\n"
        "Join karne ke liye:\n"
        "👉 @Shahzal"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Shazi Se Contact Karein\n\n"
        "👤 Telegram: @Shahzal\n\n"
        "Jaldi reply milega! 😊"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_msg = update.message.text

    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[])

    chat = user_chats[user_id]
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = chat.send_message(user_msg)
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(
            "Oops! Thodi problem hai. @Shahzal se directly contact karein. 🙏"
        )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("services", services))
    app.add_handler(CommandHandler("signals", signals))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Shazi Bot chal raha hai...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
