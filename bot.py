import discord
import asyncio
import os
from aiohttp import web

BOT_TOKEN  = os.getenv("BOT_TOKEN")
GUILD_ID   = int(os.getenv("GUILD_ID"))

# IDs a ne jamais ban (toi + tes amis)
WHITELIST = [
    # 123456789012345678,
]

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Ban bot actif : {client.user}")

@client.event
async def on_member_join(member):
    if member.guild.id != GUILD_ID: return
    if member.id in WHITELIST: return

    try:
        await member.ban(reason="Serveur ferme", delete_message_days=0)
        print(f"Banni : {member.name} ({member.id})")
    except Exception as e:
        print(f"Erreur ban {member.name} : {e}")

# Keep-alive web server pour Render
async def handle(request):
    return web.Response(text="OK")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)
    app.router.add_get("/health", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server actif sur le port {port}")

async def main():
    await asyncio.gather(
        start_web(),
        client.start(BOT_TOKEN),
    )

asyncio.run(main())
