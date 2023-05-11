import discord
from discord import option, ApplicationContext

from disc.bot_manager import bot_manager
from disc.send_message import send_message
from cost import cost_log
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
    response_message, prompt_cost, complete_cost, model_name = bot_manager.ask(message, str(ctx.channel_id))
    resp_message += response_message
    if prompt_cost or complete_cost:
        try:
            cost_log.CostLogManager.insert(str(ctx.user.id), prompt_cost, complete_cost, model_name)
        except Exception as e:
            logger.error(e)
            resp_message += "\n\n **消费记录写入失败，请联系管理员。**"
    await send_message(ctx, resp_message)


@client.slash_command(name="chat_no_mem", description="无记忆问答，更加节省token")
async def chat_no_mem(ctx: ApplicationContext, *, message: str):
    logger.info(f"Received message from {ctx.user.name}: {message}")
    resp_message: str = f'> **{message}** - <@{str(ctx.user.id)}' + '> \n\n'
    await ctx.response.defer()
    response, prompt_cost, complete_cost, model_name = bot_manager.ask_api_without_memory(message, str(ctx.channel_id))
    resp_message += response
    if prompt_cost or complete_cost:
        try:
            cost_log.CostLogManager.insert(str(ctx.user.id), prompt_cost, complete_cost, model_name)
        except Exception as e:
            logger.error(e)
            resp_message += "\n\n **消费记录写入失败，请联系管理员。**"
    await send_message(ctx, resp_message)


@client.slash_command(name="选择模型", description="为bot选择模型,gpt-4更精准,3.5更便宜响应更快" )
@option(name="model", choices=["gpt-4", "gpt-3.5-turbo"])
async def select_model(ctx: ApplicationContext, model: str):
    await ctx.response.defer()
    logger.info(f"Received select from {ctx.user.name}: {model}")
    bot_manager.reset(str(ctx.channel_id))
    bot_manager.set_model(model, str(ctx.channel_id))
    await ctx.respond(f"设置模型为 {model}")


@client.slash_command(name="选择人格", description="为bot选择人格")
@option(name="character", choices=["普通", "非常傲娇", "一般傲娇", "傲娇sp", "大小姐"])
async def select_character(ctx: ApplicationContext, character: str):
    await ctx.response.defer()
    logger.info(f"Received select from {ctx.user.name}: {character}")
    bot_manager.reset(str(ctx.channel_id))
    bot_manager.set_character(character, str(ctx.channel_id))
    await ctx.respond(f"设置角色为 {character}")


@client.slash_command(name="清空记忆")
async def reset(ctx: ApplicationContext):
    await ctx.response.defer()
    logger.info(f"Received reset from {ctx.user.name}")
    bot_manager.reset(str(ctx.channel_id))
    await ctx.respond(f"清空记忆成功")
