import os
import time
import logging
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
        callapi = requests.post("https://api.filechan.org/upload", files=files)
        text = callapi.json()
        long_url = text['data']['file']['url']['full']
        api_url = f"https://flashlink.in/api?api=aafa2d36a38398631679a74769a071b2154e08e7&url={long_url}&format=text"
        result = requests.get(api_url)
        nai_text = result.text
        da_url = "https://da.gd/"
        url = nai_text
        shorten_url = f"{da_url}shorten"
        response = requests.get(shorten_url, params={"url": url})
        nyaa_text = response.text.strip()                                     
        await asyncio.sleep(6)
        server = requests.get(url="https://api.gofile.io/getServer").json()["data"]["server"]
        uploadxz = requests.post(url=f"https://{server}.gofile.io/uploadFile", files={"upload_file": open(sed, 'rb')}).json()
        directlink = uploadxz["data"]["downloadPage"]    
        gotn_url = f"https://flashlink.in/api?api=aafa2d36a38398631679a74769a071b2154e08e7&url={directlink}&format=text"
        gofinal = requests.get(gotn_url)
        go_text = gofinal.text
        gourl = go_text
        gofile_url = f"{da_url}shorten"
        goresponse = requests.get(gofile_url, params={"url": gourl})
        gofuk_text = goresponse.text.strip()
        await asyncio.sleep(6)
        krakenapi = requests.get(url="https://krakenfiles.com/api/server/available").json()
        krakenxurl = krakenapi['data']['url']
        krakentoken = krakenapi['data']['serverAccessToken']
        params = {'serverAccessToken': krakentoken} 
        krakenupload = requests.post(krakenxurl, files={'file': open(sed, 'rb')}, data=params).json()
        krakenlink = krakenupload['data']['url']
        krtn_url = f"https://flashlink.in/api?api=aafa2d36a38398631679a74769a071b2154e08e7&url={krakenlink}&format=text"
        krfinal = requests.get(krtn_url)
        kr_text = krfinal.text
        krurl = kr_text
        krfile_url = f"{da_url}shorten"
        krresponse = requests.get(krfile_url, params={"url": krurl})
        krfuk_text = krresponse.text.strip()
        output = f"""
━━━━━━━━━━━━━━━━━━━
**External Download Links**
[Filechan]({nyaa_text})  |  [Gofile]({gofuk_text})  |  [KrakenFiles]({krfuk_text})"""
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
