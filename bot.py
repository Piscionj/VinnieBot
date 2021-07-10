from TikTokApi import TikTokApi
import string
import random
import os
import discord
import nest_asyncio
from dotenv import load_dotenv
nest_asyncio.apply()

verifyFp = "verify_kqy12n3c_hkkFwQoe_a0hj_4N5L_BtgN_d9qfFjdTFUsw"
did = ''.join(random.choice(string.digits) for num in range(19))
api = TikTokApi.get_instance(
    custom_verifyFp=verifyFp, use_test_endpoints=True, custom_did=did)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()

latest_tiktok = None


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.content.lower() == "give vinnie":
        print('Starting vinnie download')
        await download_latest_vinnie()
        print('Vinnie download complete!')
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, 'latest_vinnie.mp4')
        await message.channel.send(file=discord.File(filepath))


async def download_latest_vinnie():
    tiktoks = api.byUsername("vhackerr", count=1)

    video_bytes = api.get_video_by_tiktok(tiktoks[0])

    with open("latest_vinnie.mp4", 'wb') as o:
        o.write(video_bytes)

client.run(TOKEN)
