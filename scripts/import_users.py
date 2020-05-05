import os
import json

from peachy.db.models import User
from peachy.db.base import scoped_session


PACK_PATH = os.path.dirname(os.path.abspath(__file__))
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


def import_users():
    people = load_people(PEOPLE_PATH)
    users = []

    for discord_id, person in people.items():
        user = User(discord_id=discord_id, first_name=person.firstname, last_name=person.lastname)
        users.append(user)

    with scoped_session() as session:
        session.add_all(users)
