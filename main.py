import os
import gdown
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram import Update
from config import BOT_TOKEN

def start(update: Update, context):
    update.message.reply_text("Selamat datang! Gunakan /mirror <link> untuk mendownload dan membuat mirror link.")

def mirror(update: Update, context):
    # Ambil link dari perintah /mirror
    if not context.args:
        update.message.reply_text("Silakan masukkan link, contoh: /mirror https://drive.google.com/file/abc123")
        return
    
    link = context.args[0]
    chat_id = update.effective_chat.id
    
    # Kirim pesan status awal
    status_msg = context.bot.send_message(chat_id=chat_id, text="Downloading... Please wait.")
    
    try:
        # Tentukan folder output untuk menyimpan file
        output_dir = "downloads"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Simulasi nama file output (bisa diganti dengan nama unik)
        output_file = os.path.join(output_dir, "mirrored_file")
        
        # Download file menggunakan gdown (contoh untuk Google Drive)
        gdown.download(link, output_file, quiet=False)
        
        # Update status menjadi selesai
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_msg.message_id,
            text="Download completed! Generating mirror link..."
        )
        
        # Simulasi link mirror (di produksi, unggah file ke server/layanan seperti Google Drive)
        mirror_link = f"file://{output_file}"  # Ganti dengan URL publik jika di-host
        context.bot.send_message(chat_id=chat_id, text=f"Mirror link: {mirror_link}")
        
        # Kirim file langsung ke Telegram jika ukurannya kecil (< 50MB)
        if os.path.getsize(output_file) < 50 * 1024 * 1024:  # Cek ukuran file
            with open(output_file, 'rb') as file:
                context.bot.send_document(chat_id=chat_id, document=file)
        
    except Exception as e:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_msg.message_id,
            text=f"Error: {str(e)}. Pastikan link valid dan coba lagi."
        )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Tambahkan handler untuk perintah /start dan /mirror
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mirror", mirror, pass_args=True))
    
    # Mulai bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
