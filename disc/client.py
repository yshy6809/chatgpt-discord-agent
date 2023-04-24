import discord
from discord import Interaction, option, ApplicationContext

from disc.bot_manager import bot_manager
from disc.send_message import send_message
from loguru import logger

client = discord.Bot()


@client.event
async def on_ready():
    logger.info(f'We have logged in as {client.user}')


@client.slash_command(name="chat")
async def chat(ctx: ApplicationContext, *, message: str):
    logger.info(f"Received message from {ctx.user.name}: {message}")
    resp_message: str = f'> **{message}** - <@{str(ctx.user.id)}' + '> \n\n'
    await ctx.response.defer()
    resp_message += bot_manager.ask(message, str(ctx.channel_id))
    await send_message(ctx, resp_message)


@client.slash_command(name="select-model")
@option(name="model", description="select a model of bot", choices=["api", "web"])
async def select_model(ctx: ApplicationContext, model:str):
    await ctx.response.defer()
    logger.info(f"Received select from {ctx.user.name}: {model}")
    bot_manager.set_mode(model, str(ctx.channel_id))
    await ctx.respond(f"设置模型为 {model}")


@client.slash_command(name="select-character")
@option(name="character", description="select a character of bot", choices=["普通", "非常傲娇", "一般傲娇", "傲娇sp", "大小姐"])
async def select_character(ctx: ApplicationContext, character: str):
    await ctx.response.defer()
    logger.info(f"Received select from {ctx.user.name}: {character}")
    bot_manager.set_character(character, str(ctx.channel_id))
    await ctx.respond(f"设置角色为 {character}")





