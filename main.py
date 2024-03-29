import os
import time
import logging
import pixeldrain 
import pyrogram
import aiohttp
import requests
import aiofiles
from random import randint
from pyrogram import Client, filters, idle
from progress import progress
from config import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

DOWNLOAD = "./"


APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN

   
OC_AnonFilesBot = Client(
    "AnonFilesBot",
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)


START_TEXT = """
<b>Hey There,
Bankai!!


Don't hit 'How To Use' button to find out more about how to use me</b>
"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('How To Use', callback_data='help')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        ]]
    )
HELP_TEXT = """
No one helps you.
"""


@OC_AnonFilesBot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@OC_AnonFilesBot.on_message(filters.channel & (filters.document | filters.video | filters.audio ) & ~filters.edited, group=-1)
async def upload(client, message):
    file_caption = message.caption
    m = await message.edit(file_caption + "\n" + "━━━━━━━━━━━━━━━━━━━" + "\n"  + "`Uploading to filechan`", parse_mode = "markdown")
    now = time.time()
    sed = await OC_AnonFilesBot.download_media(
                message, DOWNLOAD,          
          progress_args=(
            "**𝚄𝚙𝚕𝚘𝚊𝚍 𝙿𝚛𝚘𝚐𝚛𝚎𝚜𝚜 𝚂𝚝𝚊𝚛𝚝𝚎𝚍, 𝙿𝚕𝚎𝚊𝚜𝚎 𝚆𝚊𝚒𝚝 !**\n**𝕀ᴛ𝕤 𝕋ᴀᴋᴇ ᴛɪᴍᴇ 𝔸ᴄᴄᴏʀᴅɪɴɢ 𝕐ᴏᴜʀ 𝔽ɪʟᴇ𝕤 𝕊ɪᴢᴇ** \n\n**ᴇᴛᴀ:** ", 
            m,
            now
            )
        )
    try:
        files = {'file': open(sed, 'rb')}
        await m.edit("**𝕌𝕡𝕝𝕠𝕒𝕕𝕚𝕟𝕘 𝕋𝕠 𝔸𝕟𝕠𝕟𝔽𝕚𝕝𝕖𝕤! ℙ𝕝𝕖𝕒𝕤𝕖 𝕎𝕒𝕚𝕥**")
        
        repz = pixeldrain.upload_file(sed)
        if repz["success"]:               
               data = pixeldrain.info(repz["id"])   
        else:
          print("Failed!")
        dlpage = f"https://pixeldrain.com/u/{data['id']}"
        ddl = f"https://pixeldrain.com/api/file/{data['id']}"
       
        output = f"""
━━━━━━━━━━━━━━━━━━━
**External Download Links**
 {dlpage} | {ddl}"""
        daze = await m.edit(output, parse_mode = "markdown")
    except Exception:
       await OC_AnonFilesBot.send_message(message.chat.id, text="Something Went Wrong!")
    os.remove(sed)



@OC_AnonFilesBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    else:
        await update.message.delete()

OC_AnonFilesBot.start()
print("""AnonFilesBot Is Started!
Send me any media file, I will upload it to anonfiles.com and give the download link
""")
idle()
