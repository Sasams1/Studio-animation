import requests
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re

# المفاتيح (تلقائيًا من طلبك)
TELEGRAM_TOKEN = "7798617257:AAEZ4rtUyV2N8dE5SJ5ExfwhPMLtxrocc4E"
API_NINJAS_KEY = "fdRFECtjOBl1XvQYZbiOzA==dZFz16DOo7QVZraS"

# استخراج اسم النطاق من الرابط (للتسمية)
def extract_domain(url):
    match = re.search(r"https?://([^/]+)", url)
    return match.group(1).replace(".", "_") if match else "site"

# دالة لجلب HTML
def scrape_website_html(url):
    api_url = f"https://api.api-ninjas.com/v1/webscraper?url={url}"
    headers = {"X-Api-Key": API_NINJAS_KEY}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", "")
    else:
        return f"<!-- Error {response.status_code}: {response.text} -->"

# الدالة الأساسية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()
    if user_message.startswith("http"):
        await update.message.reply_text("🔄 جاري تحميل نسخة HTML من الموقع...")

        html_data = scrape_website_html(user_message)
        domain = extract_domain(user_message)
        filename = f"{domain}.html"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_data)

        with open(filename, "rb") as file:
            await update.message.reply_document(InputFile(file, filename), caption=f"🌐 نسخة HTML من: {user_message}")
    else:
        await update.message.reply_text("⚠️ أرسل رابط موقع يبدأ بـ http أو https فقط.")

# تشغيل البوت
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()