from TikTokApi import TikTokApi
import string
import random
import os
import time
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

channel_id = '863218054511329303'

latest_tiktok_id = 0


async def check_for_upload():
    global latest_tiktok_id, channel_id
    while(1):
        post_id = api.byUsername("vhackerr", count=1)[0].get('id')
        if post_id != latest_tiktok_id:
            print('New post detected!')
            channel = await client.fetch_channel(channel_id)
            await download_latest_vinnie()
            dirname = os.path.dirname(__file__)
            filepath = os.path.join(dirname, 'latest_vinnie.mp4')
            await channel.send(file=discord.File(filepath), content='New vinnie just dropped!')
            os.remove(filepath)
            latest_tiktok_id = post_id
        time.sleep(10)

    # threading.Timer(10, await check_for_upload()).start()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # Start recurring check uploads thread
    global latest_tiktok_id
    latest_tiktok_id = api.byUsername("vhackerr", count=1)[0].get('id')
    await check_for_upload()


# @client.event
# async def on_message(message):
#     if message.content.lower() == "give vinnie":
#         print(message.channel.id)
    # await download_latest_vinnie()
    # dirname = os.path.dirname(__file__)
    # filepath = os.path.join(dirname, 'latest_vinnie.mp4')
    # await message.channel.send(file=discord.File(filepath))
    # os.remove(filepath)


async def download_latest_vinnie():
    tiktoks = api.byUsername("vhackerr", count=1)
    video_bytes = api.get_video_by_tiktok(tiktoks[0])

    with open("latest_vinnie.mp4", 'wb') as o:
        o.write(video_bytes)

client.run(TOKEN)
