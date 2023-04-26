#!/usr/bin/env python

from gw2api import GuildWars2Client

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
        

    def load_professions(self, professions: list[str] = ALL_PROFESSIONS):
        self.client.dir()