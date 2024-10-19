import asyncio
import os
from random import choice, shuffle

import discord
from discord.ext import commands
from discord.utils import get

from mongodb import Guild

TOKEN = os.getenv("LS_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!sp ", intents=intents)


@bot.command(name="create_server")
async def create_server(ctx) -> None:
    result = Guild.create_document(str(ctx.guild.id))
    await ctx.send("Server sucessefully created!")


@bot.command(name="change_topics")
async def change_topics(ctx, *topics) -> None:
    topics = "".join(topics)
    topics = [topic.strip() for topic in topics.split(",")]

    result = Guild.change_Topic(str(ctx.guild.id), topics)
    if result == 0:
        await ctx.send("Topics updated!")
    else:
        await ctx.send("Something gone wrong!")


@bot.command(name="reset_topics")
async def reset_topics(ctx) -> None:
    result = Guild.reset_topics(str(ctx.guild.id))
    if result == 0:
        await ctx.send("Resetd topics")
    else:
        await ctx.send("Something gone wrong")


@bot.command(name="topics")
async def show_topics(ctx) -> None:
    topics = Guild.get_topics(str(ctx.guild.id))
    await ctx.send(topics)


@bot.command(name="change_time")
async def change_time(ctx, time) -> None:
    result = Guild.change_time(str(ctx.guild.id), time)
    if result == 0:
        await ctx.send(f"Time changed to {time}")
    else:
        await ctx.send("Something gone wrong!")


@bot.command(name="change_upr")
async def change_UPR(ctx, UPR) -> None:
    result = Guild.change_UPR(str(ctx.guild.id), int(UPR))
    if result == 0:
        await ctx.send(f"User per rooms updated to {UPR}")
    else:
        await ctx.send("Something gone wrong!")


@bot.command(name="delete_server")
async def delete_server(ctx) -> None:
    Guild.delete_document(str(ctx.guild.id))
    await ctx.send("Server Deleted from the Splitter database!")


@bot.command(name="split")
async def listas(ctx):

    guild_id = str(ctx.guild.id)
    room_topics = Guild.get_topics(guild_id)
    upr = Guild.get_UPR(guild_id)
    time = Guild.get_time(guild_id)
    origin_channel = ctx.author.voice.channel
    last_room_name = ""
    users = []

    created_rooms = []
    moved_users = []
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True),
    }

    if origin_channel.members:
        members = [member.name for member in origin_channel.members]
        shuffle(members)

        # Loop para enviar os members de 2 em 2
        for i in range(0, len(members), upr):

            users = members[i : i + upr]
            moved_users.extend(users)

            new_room = await ctx.guild.create_voice_channel(
                choice(room_topics), overwrites=overwrites, user_limit=upr
            )

            created_rooms.append(new_room)
            last_room_name = new_room

            if last_room_name.name == new_room:
                choice(room_topics)

            # Mover users para sala
            for member in users:
                member = get(ctx.guild.members, name=member)
                if member and member.voice:
                    await member.move_to(new_room)

        await asyncio.sleep(time)

        for old_moved_user in moved_users:
            user = get(ctx.guild.members, name=old_moved_user)
            await user.move_to(origin_channel)

        for room in created_rooms:
            await room.delete()

    else:
        await ctx.send("Não há usuários no origin_channel.")


@bot.event
async def on_ready():
    print(f"{bot.user.name} online.")


if __name__ == "__main__":
    bot.run(TOKEN)
