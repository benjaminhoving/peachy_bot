import re
import json
import os
import sys

import discord

client = discord.Client()


DAD_JOKE_RE = r"[Ii]\'?[mM]\s(?P<name>[^\.]*)\.?"
DAD_JOKE_PROG = re.compile(DAD_JOKE_RE)

AMPD_GUILD_ID = 691335993764216872

DISCORD_KEY = None

PACK_PATH = os.path.dirname(os.path.abspath(__file__))
print(PACK_PATH)
PEOPLE_PATH = os.path.join(PACK_PATH, "people.json")


class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return f"{self.fullname}"


    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"


def load_people(filename):
    people = {}

    with open(filename, 'r') as infile:
        raw_data = json.load(infile)

        for raw_key, raw_person in raw_data.items():
            key = int(raw_key)
            first_name = raw_person['first_name']
            last_name = raw_person['last_name']

            people[key] = Person(first_name, last_name)

    return people


USER_MAP = load_people(PEOPLE_PATH)
print(USER_MAP)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$who"):
        members = message.mentions
        for member in members:
            try:
                person = USER_MAP[member.id]
            except KeyError:
                await message.channel.send(
                    f"no real name found for {member.display_name}. go harass peachy pie about it"
                )
                return

            await message.channel.send(f"{member.display_name} is {person.fullname}")

    if message.content.startswith("$hello"):
        await message.channel.send(f"Hello, {message.author.display_name}!")

    match = DAD_JOKE_PROG.match(message.content)
    if match:
        name = match["name"]
        if name != "":
            await message.channel.send(f"Hi, {name}. I'm Peachy's Bot.")


if __name__ == "__main__":
    try:
        DISCORD_KEY = sys.argv[1]
    except IndexError:
        print("please supply the file containing the discord key")

    client.run(DISCORD_KEY)
