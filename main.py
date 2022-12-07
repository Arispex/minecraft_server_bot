import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.context import Context
from discord.message import Message
import loguru
import tortoise
import models

logger = loguru.logger

TOKEN = "YOURTOKEN"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    logger.info("Bot is ready")
    try:
        await tortoise.Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['models.orm']}
        )
        logger.info("Successfully connected to database")
    except Exception as e:
        logger.error("Failed to connect to database")
        logger.error(e)
        exit(-1)
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return
    logger.info(f'{message.author} said {message.content}')
    await bot.process_commands(message)


@bot.command()
@has_permissions(administrator=True)
async def config(ctx: Context):
    try:
        await models.orm.guilds.get(guild_id=ctx.guild.id)
    except tortoise.exceptions.DoesNotExist:
        logger.info(f"Guild({ctx.guild.id}) not found in database, creating new entry")
        await models.orm.guilds.create(guild_id=ctx.guild.id)
        logger.info(f"Guild({ctx.guild.id}) created")

    guild = await models.orm.guilds.get(guild_id=ctx.guild.id)
    msg = []
    for key, value in guild.__dict__.items():
        if key == "id" or key.startswith("_"):
            continue
        msg.append(f"{key} = {value}")
    await ctx.send("\n".join(msg))


@bot.command()
@has_permissions(administrator=True)
async def setconfig(ctx: Context, key: str, value: str):
    try:
        await models.orm.guilds.get(guild_id=ctx.guild.id)
    except tortoise.exceptions.DoesNotExist:
        logger.info(f"Guild({ctx.guild.id}) not found in database, creating new entry")
        await models.orm.guilds.create(guild_id=ctx.guild.id)
        logger.info(f"Guild({ctx.guild.id}) created")

    guild = await models.orm.guilds.get(guild_id=ctx.guild.id)
    keys = [k for k in guild.__dict__.keys() if not k.startswith("_") or k == "id"]
    if key in keys:
        guild.__dict__[key] = value
        await guild.save()
        logger.info(f"Send message to {ctx.guild.name}<{ctx.guild.id}>: Successfully updated {key} to {value}")
        await ctx.send(f"Successfully updated {key} to {value}")
    else:
        logger.info(f"Send message to {ctx.guild.name}<{ctx.guild.id}>: {key} is not a valid key")
        await ctx.send(f"{key} is not a valid key")


@bot.command()
async def playing(ctx: Context):
    server = await models.Server.get(guild_id=ctx.guild.id)
    try:
        query = server.query.query()
    except:
        await ctx.send("Can't connect to server")

    max_player = query.players.max
    online_player = query.players.online
    online_player_names = query.players.names

    await ctx.send(f"The following players are playing the server({online_player}/{max_player}):\n" +
                   ' '.join(map(lambda x: f'[{x}]', online_player_names)))

bot.run(TOKEN)
