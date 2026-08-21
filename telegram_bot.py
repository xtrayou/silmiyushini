import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_USER_IDS = os.getenv('ALLOWED_USER_IDS', '').split(',')

# Folder paths
FOTO_FOLDER = 'foto'
DOKUMENTASI_FOLDER = 'dokumentasimagang'

# Create folders if they don't exist
os.makedirs(FOTO_FOLDER, exist_ok=True)
os.makedirs(DOKUMENTASI_FOLDER, exist_ok=True)

# User session storage
user_sessions = {}

def is_authorized(user_id: int) -> bool:
    """Check if user is authorized to use the bot"""
    if not ALLOWED_USER_IDS or ALLOWED_USER_IDS[0] == '':
        return True  # If no restriction, allow all
    return str(user_id) in ALLOWED_USER_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message and show menu"""
    user = update.effective_user
    
    if not is_authorized(user.id):
        await update.message.reply_text("⛔ Maaf, Anda tidak memiliki akses ke bot ini.")
        return
    
    keyboard = [
        [InlineKeyboardButton("📸 Upload Foto Portfolio", callback_data='upload_foto')],
        [InlineKeyboardButton("📂 Upload Dokumentasi Magang", callback_data='upload_dokumentasi')],
        [InlineKeyboardButton("📊 Lihat Status", callback_data='status')],
        [InlineKeyboardButton("❓ Bantuan", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
🎨 *Selamat datang di Portfolio Update Bot!*

Halo {user.first_name}! 👋

Bot ini membantu Anda memperbarui foto di website portfolio dengan mudah.

Pilih menu di bawah untuk memulai:
    """
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_authorized(user_id):
        await query.answer("⛔ Akses ditolak!")
        return
    
    await query.answer()
    
    if query.data == 'upload_foto':
        user_sessions[user_id] = {'mode': 'foto'}
        await query.edit_message_text(
            "📸 *Upload Foto Portfolio*\n\n"
            "Silakan kirim foto yang ingin Anda upload ke folder portfolio.\n"
            "Foto akan disimpan di folder `foto/`\n\n"
            "Anda bisa mengirim beberapa foto sekaligus.\n"
            "Ketik /cancel untuk membatalkan.",
            parse_mode='Markdown'
        )
    
    elif query.data == 'upload_dokumentasi':
        user_sessions[user_id] = {'mode': 'dokumentasi'}
        await query.edit_message_text(
            "📂 *Upload Dokumentasi Magang*\n\n"
            "Silakan kirim foto dokumentasi magang Anda.\n"
            "Foto akan disimpan di folder `dokumentasimagang/`\n\n"
            "Anda bisa mengirim beberapa foto sekaligus.\n"
            "Ketik /cancel untuk membatalkan.",
            parse_mode='Markdown'
        )
    
    elif query.data == 'status':
        foto_count = len([f for f in os.listdir(FOTO_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
        dok_count = len([f for f in os.listdir(DOKUMENTASI_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
        
        status_text = f"""
📊 *Status Website Portfolio*

📁 *Folder Foto:* {foto_count} gambar
📁 *Folder Dokumentasi:* {dok_count} gambar

💾 Total: {foto_count + dok_count} gambar
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            status_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif query.data == 'help':
        help_text = """
❓ *Bantuan - Portfolio Update Bot*

*Cara Menggunakan:*

1️⃣ Pilih jenis upload (Foto Portfolio atau Dokumentasi)
2️⃣ Kirim foto yang ingin diupload
3️⃣ Bot akan menyimpan foto secara otomatis
4️⃣ Foto siap digunakan di website!

*Perintah Tersedia:*
/start - Tampilkan menu utama
/cancel - Batalkan upload saat ini
/status - Lihat status folder

*Format Foto yang Didukung:*
JPG, JPEG, PNG, GIF

*Catatan:*
• Anda bisa mengirim beberapa foto sekaligus
• Foto akan diberi nama dengan timestamp otomatis
• Pastikan ukuran foto tidak terlalu besar (maks 10MB)
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            help_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif query.data == 'back_to_menu':
        keyboard = [
            [InlineKeyboardButton("📸 Upload Foto Portfolio", callback_data='upload_foto')],
            [InlineKeyboardButton("📂 Upload Dokumentasi Magang", callback_data='upload_dokumentasi')],
            [InlineKeyboardButton("📊 Lihat Status", callback_data='status')],
            [InlineKeyboardButton("❓ Bantuan", callback_data='help')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🎨 *Portfolio Update Bot*\n\nPilih menu di bawah:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo uploads"""
    user_id = update.effective_user.id
    
    if not is_authorized(user_id):
        await update.message.reply_text("⛔ Anda tidak memiliki akses ke bot ini.")
        return
    
    # Check if user has an active session
    if user_id not in user_sessions:
        keyboard = [
            [InlineKeyboardButton("📸 Upload Foto Portfolio", callback_data='upload_foto')],
            [InlineKeyboardButton("📂 Upload Dokumentasi Magang", callback_data='upload_dokumentasi')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Silakan pilih jenis upload terlebih dahulu:",
            reply_markup=reply_markup
        )
        return
    
    mode = user_sessions[user_id]['mode']
    
    # Determine save folder
    save_folder = FOTO_FOLDER if mode == 'foto' else DOKUMENTASI_FOLDER
    
    # Get the largest photo
    photo = update.message.photo[-1]
    
    # Download photo
    file = await context.bot.get_file(photo.file_id)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_extension = 'jpg'
    filename = f"{timestamp}_{photo.file_id[:8]}.{file_extension}"
    file_path = os.path.join(save_folder, filename)
    
    # Save photo
    await file.download_to_drive(file_path)
    
    folder_name = "Foto Portfolio" if mode == 'foto' else "Dokumentasi Magang"
    
    await update.message.reply_text(
        f"✅ Foto berhasil disimpan!\n\n"
        f"📁 Folder: {folder_name}\n"
        f"📄 Nama file: `{filename}`\n"
        f"📍 Lokasi: `{file_path}`\n\n"
        f"Kirim foto lain atau ketik /cancel untuk selesai.",
        parse_mode='Markdown'
    )
    
    logger.info(f"Photo saved: {file_path} by user {user_id}")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancel current operation"""
    user_id = update.effective_user.id
    
    if user_id in user_sessions:
        del user_sessions[user_id]
        await update.message.reply_text(
            "❌ Upload dibatalkan.\n\nKetik /start untuk kembali ke menu utama."
        )
    else:
        await update.message.reply_text(
            "Tidak ada operasi yang sedang berlangsung.\n\nKetik /start untuk membuka menu."
        )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show folder status"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("⛔ Akses ditolak!")
        return
    
    foto_count = len([f for f in os.listdir(FOTO_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
    dok_count = len([f for f in os.listdir(DOKUMENTASI_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
    
    status_text = f"""
📊 *Status Website Portfolio*

📁 *Folder Foto:* {foto_count} gambar
📁 *Folder Dokumentasi:* {dok_count} gambar

💾 Total: {foto_count + dok_count} gambar
    """
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

def main() -> None:
    """Start the bot"""
    if not BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN tidak ditemukan!")
        print("Silakan buat file .env dan tambahkan token bot Anda:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Start the bot
    print("🤖 Bot started! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
