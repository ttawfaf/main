import discord
from discord.ext import commands
import yt_dlp
import static_ffmpeg

# إضافة مسار ffmpeg تلقائياً للسيستم
static_ffmpeg.add_paths()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extractor_args': {'youtube': ['player_client=android,web']},
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {bot.user}')

@bot.command(name='play', help='تشغيل صوتية')
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send("يجب أن تكون في روم صوتي أولاً!")
        return

    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await channel.connect()

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                info = info['entries'][0]
            url = info['url']
            title = info.get('title', 'صوتية')

        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        ctx.voice_client.play(source)
        await ctx.send(f"🎵 جاري تشغيل: **{title}**")

@bot.command(name='pause')
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ تم الإيقاف المؤقت.")

@bot.command(name='resume')
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ تم الاستئناف.")

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ تم الإيقاف والمغادرة.")

bot.run('MTU0OTc3ODgyODgxNjAyMzYxNg.Goq6RC.gkN0srsXHzqOGi4N2DwghJ6Eca4WbYcPrIlMdo')
