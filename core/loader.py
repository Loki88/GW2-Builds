#!/usr/bin/env python

from gw2api import GuildWars2Client
from model.api import Profession

HEAVY_PROFESSIONS = ['Guardian', 'Dragonhunter', 'Firebrand', 'Willbender', 'Revenant', 'Herald', 'Renegade', 'Vindicator', 'Warrior', 'Berserker' \
                   'Spellbreaker', 'Bladesworn']

MEDIUM_PROFESSIONS = ['Engineer', 'Scrapper', 'Holosmith', 'Mechanist', 'Ranger', 'Druid', 'Soulbeast', 'Untamed', 'Thief', 'Daredevil', \
                      'Deadeye', 'Specter']

LIGHT_PROFESSIONS = ['Elementalist', 'Tempest', 'Weaver', 'Catalyst', 'Mesmer', 'Chronomancer', 'Mirage', 'Virtuoso', 'Necromancer', \
                     'Reaper', 'Scourge', 'Harbinger']

ALL_PROFESSIONS = HEAVY_PROFESSIONS + MEDIUM_PROFESSIONS + LIGHT_PROFESSIONS

class Loader():

    def __init__(self) -> None:
        self.client = GuildWars2Client()

    def __del__(self):
        self.client.session.close()

    def load_professions(self, professions: list[str] = ALL_PROFESSIONS):
        professions_list: list[str] = self.client.professions.get()
        return [Profession(x) for x in self.client.professions.get(ids=professions_list)]
