# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Location: Supaul, Bihar 
#
# All rights reserved.
#
# This code is the intellectual property of @WTF_Phantom.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: king25258069@gmail.com

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import BOT_NAME, START_IMG_URL, HELP_IMG_URL, SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER_LINK
from baka.utils import ensure_user_exists, get_mention, track_group, log_to_channel, SUDO_USERS

# --- 🖼️ IMAGES ---
SUDO_IMG = "https://files.catbox.moe/gyi5iu.jpg"

# --- ⌨️ KEYBOARDS ---

def get_start_keyboard(bot_username):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💌 ᴜᴘᴅᴀᴛᴇ 💌", url=SUPPORT_CHANNEL), InlineKeyboardButton("✴️ Sᴜᴘᴘʀᴏᴛ ✴️", url=SUPPORT_GROUP)],
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("🛡️ Hᴇʟᴘ ᴍᴇɴᴜ 📇", callback_data="help_main"), InlineKeyboardButton("💌 Oᴡɴᴇʀ 💌", url=OWNER_LINK)]
    ])

def get_help_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💍 Sᴏᴄɪᴀʟ", callback_data="help_social"), InlineKeyboardButton("💰 Eᴄᴏɴᴏᴍʏ", callback_data="help_economy")],
        [InlineKeyboardButton("⚔️ Rᴘɢ", callback_data="help_rpg"), InlineKeyboardButton("🧠 Aɪ & Fᴜɴ", callback_data="help_fun")],
        [InlineKeyboardButton("⚙️ Gʀᴏᴜᴘ", callback_data="help_group"), InlineKeyboardButton("🔐 Sᴜᴅᴏ", callback_data="help_sudo")],
        [InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="return_start")]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("💌 Bᴀᴄᴋ", callback_data="help_main")]])

# --- 🚀 COMMANDS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    ensure_user_exists(user)
    track_group(chat, user)
    
    caption = (
        f"👋 <b>Kʀɪᴛɪ'Bᴏᴛ</b> {get_mention(user)}! (⁠≧⁠▽⁠≦⁠)\n\n"
        f"『 <b>{BOT_NAME}</b> 』\n"
        f"<i>The Aesthetic AI-Powered RPG Bot!</i> 🌸\n\n"
        f"🎮 <b>𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬:</b>\n"
        f"‣ <b>RPG:</b> Kill, Rob (100%), Protect\n"
        f"‣ <b>Social:</b> Marry, Couple\n"
        f"‣ <b>Economy:</b> Claim, Give\n"
        f"‣ <b>AI:</b> Sassy Chatbot\n\n"
        f"💭 <b>Nᴇᴇᴅ Hᴇʟᴘ?</b>\n"
        f"Click the buttons below!\n"
    )

    kb = get_start_keyboard(context.bot.username)

    if update.callback_query:
        try: await update.callback_query.message.edit_media(InputMediaPhoto(media=START_IMG_URL, caption=caption, parse_mode=ParseMode.HTML), reply_markup=kb)
        except: await update.callback_query.message.edit_caption(caption=caption, parse_mode=ParseMode.HTML, reply_markup=kb)
    else:
        if START_IMG_URL and START_IMG_URL.startswith("http"):
            try: await update.message.reply_photo(photo=START_IMG_URL, caption=caption, parse_mode=ParseMode.HTML, reply_markup=kb)
            except: await update.message.reply_text(caption, parse_mode=ParseMode.HTML, reply_markup=kb)
        else: await update.message.reply_text(caption, parse_mode=ParseMode.HTML, reply_markup=kb)

    if chat.type == ChatType.PRIVATE and not update.callback_query:
        await log_to_channel(context.bot, "command", {"user": f"{get_mention(user)} (`{user.id}`)", "action": "Started Bot", "chat": "Private"})

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=HELP_IMG_URL,
        caption=f"📖 <b>{BOT_NAME} 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐃𝐢𝐚𝐫𝐲</b> 🌸\n\n<i>Select a category below to explore all features!</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=get_help_keyboard()
    )

# --- 🖱️ CALLBACK HANDLER ---

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "return_start":
        await start(update, context)
        return

    if data == "help_main":
        try: await query.message.edit_media(InputMediaPhoto(media=HELP_IMG_URL, caption=f"📖 <b>{BOT_NAME} 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐃𝐢𝐚𝐫𝐲</b> 🌸\n\n<i>Select a category below to explore all features!</i>", parse_mode=ParseMode.HTML), reply_markup=get_help_keyboard())
        except: await query.message.edit_caption(caption=f"📖 <b>{BOT_NAME} 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐃𝐢𝐚𝐫𝐲</b> 🌸\n\n<i>Select a category below to explore all features!</i>", parse_mode=ParseMode.HTML, reply_markup=get_help_keyboard())
        return

    target_photo = HELP_IMG_URL
    kb = get_back_keyboard()
    text = ""
    
    if data == "help_social":
        text = (
            "💍 <b>𝐒𝐨𝐜𝐢𝐚𝐥 & 𝐋𝐨𝐯𝐞</b>\n\n"
            "<b>/propose @user</b>\n"
            "↳ Marry someone (5% Tax Perk).\n\n"
            "<b>/marry</b>\n"
            "↳ Check relationship status.\n\n"
            "<b>/divorce</b>\n"
            "↳ Break up (Cost: 2k).\n\n"
            "<b>/couple</b>\n"
            "↳ Matchmaking Fun!"
        )

    elif data == "help_economy":
        text = (
            "💰 <b>𝐄𝐜𝐨𝐧𝐨𝐦𝐲 & 𝐒𝐡𝐨𝐩</b>\n\n"
            "<b>/bal</b>\n"
            "↳ Check Wallet, Rank & Inventory.\n\n"
            "<b>/shop</b>\n"
            "↳ Buy Weapons & Armor.\n\n"
            "<b>/give [amt] [user]</b>\n"
            "↳ Transfer (10% Tax).\n\n"
            "<b>/claim</b>\n"
            "↳ Group Bonus (2k).\n\n"
            "<b>/daily</b>\n"
            "↳ Streak Rewards.\n\n"
            "<b>/ranking</b>\n"
            "↳ Global Leaderboards."
        )

    elif data == "help_rpg":
        text = (
            "⚔️ <b>𝐑𝐏𝐆 & 𝐖𝐚𝐫</b>\n\n"
            "<b>/kill [user]</b>\n"
            "↳ Murder. 50% Chance to loot Items!\n"
            "<b>/rob [amt] [user]</b>\n"
            "↳ Steal coins + 20% Chance to steal Items.\n"
            "<b>/protect 1d</b>\n"
            "↳ Buy Shield. Protects partner too!\n"
            "<b>/revive</b>\n"
            "↳ Revive instantly for 500 coins."
        )

    elif data == "help_fun":
        text = (
            "🧠 <b>𝐀𝐈 & 𝐅𝐮𝐧</b>\n\n"
            "<b>/draw [prompt]</b> ➪ AI Art (Flux Anime).\n"
            "<b>/speak [text]</b> ➪ Anime Voice.\n"
            "<b>/chatbot</b> ➪ AI Settings.\n"
            "<b>/riddle</b> ➪ AI Quiz.\n"
            "<b>/dice</b> | <b>/slots</b> ➪ Gambling."
        )

    elif data == "help_group":
        text = (
            "⚙️ <b>𝐆𝐫𝐨𝐮𝐩 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬</b>\n\n"
            "<b>/welcome on/off</b> ➪ Welcome Images.\n"
            "<b>/ping</b> ➪ System Status."
        )

    elif data == "help_sudo":
        if query.from_user.id not in SUDO_USERS: return await query.answer("❌ Baka! Owner Only!", show_alert=True)
        target_photo = SUDO_IMG
        text = (
            "🔐 <b>𝐒𝐮𝐝𝐨 𝐏𝐚𝐧𝐞𝐥</b>\n\n"
            "<b>/addcoins [amt] [user]</b>\n"
            "<b>/rmcoins [amt] [user]</b>\n"
            "<b>/freerevive [user]</b>\n"
            "<b>/unprotect [user]</b>\n"
            "<b>/broadcast -user/-group -clean</b>\n\n"
            "<b>👑 Owner Only:</b>\n"
            "<b>/update</b> (Restart System)\n"
            "<b>/addsudo [user]</b>\n"
            "<b>/rmsudo [user]</b>\n"
            "<b>/cleandb</b> (Wipe Data)"
        )

    try: await query.message.edit_media(InputMediaPhoto(media=target_photo, caption=text, parse_mode=ParseMode.HTML), reply_markup=kb)
    except: await query.message.edit_caption(caption=text, parse_mode=ParseMode.HTML, reply_markup=kb)
