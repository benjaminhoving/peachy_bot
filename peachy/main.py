import re
import json
import sys

import discord
from sqlalchemy.orm.exc import NoResultFound

from peachy.db.base import scoped_session
from peachy.db.models import User


client = discord.Client()


DAD_JOKE_RE = r"[Ii]\'?[mM]\s(?P<name>[^\.]*)\.?"
DAD_JOKE_PROG = re.compile(DAD_JOKE_RE)

AMPD_GUILD_ID = 691335993764216872


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


def load_settings(settings_filename):
    with open(settings_filename, 'r') as infile:
        settings = json.load(infile)
    return settings


def main(settings):
    try:
        discord_key = settings["discord_key"]
    except KeyError:
        print("configuration file does not contain 'discord_key'")
        sys.exit()

    client.run(discord_key)


def bootstrap():
    try:
        settings_filename = sys.argv[1]
    except IndexError:
        print("please provide the path to a configuration json file")
        sys.exit()
    settings = load_settings(settings_filename)
    while True:
        try:
            main(settings)
        except Exception as e:
            with open('peachy_log.log', 'a') as outfile:
                print('something went wrong', e, file=outfile)


if __name__ == "__main__":
    bootstrap()
