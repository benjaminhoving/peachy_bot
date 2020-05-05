import re
import sys

import discord
from sqlalchemy.orm.exc import NoResultFound

from peachy.db.base import scoped_session
from peachy.db.models import User


client = discord.Client()


DAD_JOKE_RE = r"[Ii]\'?[mM]\s(?P<name>[^\.]*)\.?"
DAD_JOKE_PROG = re.compile(DAD_JOKE_RE)

AMPD_GUILD_ID = 691335993764216872

DISCORD_KEY = None


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$who"):
        for member in message.mentions:
            with scoped_session() as session:
                try:
                    user = session.query(User).filter(User.discord_id == member.id).one()
                except NoResultFound:
                    message.channel.send(f"No real name found for {member.display_name}.")
                response_message = f"{member.display_name} is {user.full_name}"

            await message.channel.send(response_message)

    if message.content.startswith("$hello"):
        await message.channel.send(f"Hello, {message.author.display_name}!")

    match = DAD_JOKE_PROG.match(message.content)
    if match:
        name = match["name"]
        if name != "":
            await message.channel.send(f"Hi, {name}. I'm Peachy's Bot.")


def main():
    global DISCORD_KEY
    try:
        DISCORD_KEY = sys.argv[1]
    except IndexError:
        print("please supply the file containing the discord key")

    client.run(DISCORD_KEY)


if __name__ == "__main__":
    main()
