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

import random
from bytez import Bytez
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction, ChatType
from telegram.error import BadRequest
from baka.config import BYTEZ_API_KEY, BOT_NAME, OWNER_LINK
from baka.database import chatbot_collection
from baka.utils import stylize_text

# Bytez SDK Setup
sdk = Bytez(BYTEZ_API_KEY)
MODEL_NAME = "Qwen/Qwen3-0.6B"
model = sdk.model(MODEL_NAME)
MAX_HISTORY = 12

# --- CUTE STICKER PACKS ---
STICKER_PACKS = [
    "https://t.me/addstickers/RandomByDarkzenitsu",
    "https://t.me/addstickers/Null_x_sticker_2",
    "https://t.me/addstickers/pack_73bc9_by_TgEmojis_bot",
    "https://t.me/addstickers/animation_0_8_Cat",
    "https://t.me/addstickers/vhelw_by_CalsiBot",
    "https://t.me/addstickers/Rohan_yad4v1745993687601_by_toWebmBot",
    "https://t.me/addstickers/MySet199",
    "https://t.me/addstickers/Quby741",
    "https://t.me/addstickers/Animalsasthegtjtky_by_fStikBot",
    "https://t.me/addstickers/a6962237343_by_Marin_Roxbot"
]

# --- Fallback Responses ---
FALLBACK_RESPONSES = [
    "Achha ji? (⁠•⁠‿⁠•⁠)",
    "Hmm... aur batao?",
    "Okk okk!",
    "Sahi hai yaar ✨",
    "Toh phir?",
    "Interesting! 😊",
    "Aur kya chal raha?",
    "Sunao sunao!",
    "Haan haan, aage bolo",
    "Achha theek hai (⁠≧⁠▽⁠≦⁠)"
]

# --- HELPER FUNCTIONS ---
async def send_ai_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random sticker from configured packs with error handling."""
    max_attempts = 5
    tried_packs = set()

    for _ in range(max_attempts):
        available_packs = [p for p in STICKER_PACKS if p not in tried_packs]
        if not available_packs:
            break

        raw_link = random.choice(available_packs)
        tried_packs.add(raw_link)
        pack_name = raw_link.split('/')[-1]

        try:
            sticker_set = await context.bot.get_sticker_set(pack_name)
            if sticker_set and sticker_set.stickers:
                sticker = random.choice(sticker_set.stickers)
                await update.message.reply_sticker(sticker.file_id)
                return True
        except BadRequest:
            continue
        except Exception as e:
            print(f"Sticker error: {e}")
            continue
    return False

# --- MENU HANDLERS ---
async def chatbot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == ChatType.PRIVATE:
        return await update.message.reply_text("🧠 <b>Haan baba, DM me active hu!</b> 😉", parse_mode=ParseMode.HTML)

    member = await chat.get_member(user.id)
    if member.status not in ['administrator', 'creator']:
        return await update.message.reply_text("❌ <b>Tu Admin nahi hai, Baka!</b>", parse_mode=ParseMode.HTML)

    doc = chatbot_collection.find_one({"chat_id": chat.id})
    is_enabled = doc.get("enabled", True) if doc else True
    status = "🟢 Enabled" if is_enabled else "🔴 Disabled"

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Enable", callback_data="ai_enable"),
         InlineKeyboardButton("❌ Disable", callback_data="ai_disable")],
        [InlineKeyboardButton("🗑️ Bhula Do (Reset)", callback_data="ai_reset")]
    ])
    await update.message.reply_text(f"🤖 <b>AI Settings</b>\nStatus: {status}\n<i>She is active by default!</i>",
                                    parse_mode=ParseMode.HTML, reply_markup=kb)

async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    member = await query.message.chat.get_member(query.from_user.id)
    if member.status not in ['administrator', 'creator']:
        return await query.answer("❌ Hatt! Sirf Admin.", show_alert=True)

    data = query.data
    chat_id = query.message.chat.id

    if data == "ai_enable":
        chatbot_collection.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
        await query.message.edit_text("✅ <b>Enabled!</b>\n<i>Ab ayega maza! (⁠≧⁠▽⁠≦⁠)</i>", parse_mode=ParseMode.HTML)
    elif data == "ai_disable":
        chatbot_collection.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
        await query.message.edit_text("❌ <b>Disabled!</b>\n<i>Ja rahi hu... (⁠｡⁠•́⁠︿⁠•̀⁠｡⁠)</i>", parse_mode=ParseMode.HTML)
    elif data == "ai_reset":
        chatbot_collection.update_one({"chat_id": chat_id}, {"$set": {"history": []}}, upsert=True)
        await query.answer("🧠 Sab bhool gayi main!", show_alert=True)

# --- AI RESPONSE FUNCTION USING BYTEZ SDK ---
async def get_ai_response(chat_id: int, user_input: str, user_name: str):
    if not BYTEZ_API_KEY:
        return "⚠️ API Key Missing"

    # Chat history
    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])

    # System prompt
    system_prompt = f"Tum {BOT_NAME} ho - ek cute aur sassy Indian girlfriend jo naturally Hinglish mein baat karti hai."

    # Prepare messages for Bytez
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-MAX_HISTORY:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_input})

    # Call Bytez SDK
    output, error = model.run(messages)
    if error:
        print("Bytez Error:", error)
        reply = random.choice(FALLBACK_RESPONSES)
    else:
        reply = output[0]["content"] if output else random.choice(FALLBACK_RESPONSES)

    # Update history
    new_hist = history + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": reply}
    ]
    if len(new_hist) > MAX_HISTORY * 2:
        new_hist = new_hist[-MAX_HISTORY * 2:]
    chatbot_collection.update_one({"chat_id": chat_id}, {"$set": {"history": new_hist}}, upsert=True)

    return reply

# --- MESSAGE HANDLER ---
async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg: return
    chat = update.effective_chat

    # Sticker reply
    if msg.sticker:
        if (msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id) or chat.type == ChatType.PRIVATE:
            success = await send_ai_sticker(update, context)
            if not success:
                cute_responses = ["😊", "💕", "✨", "(⁠≧⁠▽⁠≦⁠)", "Cute! 💖"]
                await msg.reply_text(random.choice(cute_responses))
        return

    # Text reply
    if not msg.text or msg.text.startswith("/"): return
    text = msg.text
    should_reply = False

    if chat.type == ChatType.PRIVATE:
        should_reply = True
    else:
        doc = chatbot_collection.find_one({"chat_id": chat.id})
        is_enabled = doc.get("enabled", True) if doc else True
        if not is_enabled: return

        bot = context.bot.username.lower() if context.bot.username else "bot"
        if msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id:
            should_reply = True
        elif f"@{bot}" in text.lower():
            should_reply = True
            text = text.replace(f"@{bot}", "").replace(f"@{context.bot.username}", "")
        elif any(text.lower().startswith(word) for word in ["hey", "hi", "sun", "oye", "baka", "ai", "hello", "baby", "babu", "oi"]):
            should_reply = True

    if should_reply:
        if not text.strip(): text = "Hi"
        await context.bot.send_chat_action(chat_id=chat.id, action=ChatAction.TYPING)
        res = await get_ai_response(chat.id, text, msg.from_user.first_name)
        await msg.reply_text(stylize_text(res), parse_mode=None)

        # Random sticker 30% chance
        if random.random() < 0.30:
            await send_ai_sticker(update, context)

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not context.args:
        return await msg.reply_text("🗣️ <b>Bol kuch:</b> <code>/ask Kya chal raha hai?</code>", parse_mode=ParseMode.HTML)
    
    await context.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    res = await get_ai_response(msg.chat.id, " ".join(context.args), msg.from_user.first_name)
    await msg.reply_text(stylize_text(res), parse_mode=None)
