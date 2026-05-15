import os
import requests

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Telegram Bot Token
TOKEN = "8755118440:AAGmpVErk7E133E2aCf4MCEA-_qZxnnKl-c"

# Your Instagram API
API_URL = "https://xeon-insta-api.koyeb.app/pin?msg="


# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Instagram Downloader Bot\n\n"
        "Commands:\n"
        "/download instagram_link\n"
        "/ping"
    )


# Ping Command
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🏓 Pong! Bot is Alive."
    )


# Download Command
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage:\n/download instagram_link"
        )

        return

    insta_link = context.args[0]

    try:

        await update.message.reply_text(
            "⏳ Fetching reel..."
        )

        # Request API
        response = requests.get(
            API_URL + insta_link,
            timeout=30
        )

        if response.status_code != 200:

            await update.message.reply_text(
                "❌ API Error"
            )

            return

        data = response.json()

        print(data)

        # Get video URL
        video_url = data.get("video")

        if not video_url:

            await update.message.reply_text(
                "❌ No video found"
            )

            return

        await update.message.reply_text(
            "📥 Downloading video..."
        )

        # Download video locally
        video_response = requests.get(
            video_url,
            stream=True,
            timeout=120
        )

        file_name = "instagram.mp4"

        with open(file_name, "wb") as file:

            for chunk in video_response.iter_content(
                chunk_size=1024
            ):

                if chunk:
                    file.write(chunk)

        await update.message.reply_text(
            "📤 Uploading..."
        )

        # Send video to Telegram
        with open(file_name, "rb") as video:

            await update.message.reply_video(
                video=video,
                caption="✅ Download Complete"
            )

        # Remove file
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{str(e)}"
        )


# Build Bot
app = ApplicationBuilder().token(TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("download", download))

# Run Bot
print("🚀 Bot Running...")

app.run_polling()
