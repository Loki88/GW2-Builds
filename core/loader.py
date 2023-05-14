#!/usr/bin/env python

from gw2api import GuildWars2Client
from model.api import Profession, Specialization

HEAVY_PROFESSIONS = ['Guardian', 'Revenant', 'Warrior']
MEDIUM_PROFESSIONS = ['Engineer', 'Ranger', 'Thief']
LIGHT_PROFESSIONS = ['Elementalist', 'Mesmer', 'Necromancer']

HEAVY_SPECIALIZATIONS = ['Guardian', 'Dragonhunter', 'Firebrand', 'Willbender', 'Revenant', 'Herald', 'Renegade', 'Vindicator', 'Warrior', 'Berserker' \
                   'Spellbreaker', 'Bladesworn']

MEDIUM_SPECIALIZATIONS = ['Engineer', 'Scrapper', 'Holosmith', 'Mechanist', 'Ranger', 'Druid', 'Soulbeast', 'Untamed', 'Thief', 'Daredevil', \
                      'Deadeye', 'Specter']

LIGHT_SPECIALIZATIONS = ['Elementalist', 'Tempest', 'Weaver', 'Catalyst', 'Mesmer', 'Chronomancer', 'Mirage', 'Virtuoso', 'Necromancer', \
                     'Reaper', 'Scourge', 'Harbinger']

ALL_PROFESSIONS = HEAVY_PROFESSIONS + MEDIUM_PROFESSIONS + LIGHT_PROFESSIONS

class Loader():

    def __init__(self) -> None:
        self.client = GuildWars2Client()

    def __del__(self):
        self.client.session.close()

    def load_professions(self, professions: list[str] = ALL_PROFESSIONS) -> list[Profession]:
        response = self.client.professions.get(ids=professions)
        api_professions = [self._load_profession(x) for x in response]
        return api_professions
    
    def _load_profession(self, data: dict) -> Profession:
        return Profession(data)
    
    def load_specializations(self, professions: list[Profession]) -> list[Specialization]:
        if(professions is not None):
            return self._load_specializations(self._flatten([x.specializations for x in professions]))
        else:
            return []
    
    def _load_specializations(self, specializations: list[int]) -> list[Specialization]:
        if(specializations is not None):
            api_specializations = [Specialization(x) for x in self.client.specializations.get(ids=specializations)]
            return api_specializations
        else:
            return []
        
    def load_traits(self, specializations: list[Specialization]):
        if(specializations is not None):
             return self._load_traits(self._flatten([[*x.minor_traits, *x.major_traits] for x in specializations]))
        else:
            return []
        
    def _load_traits(self, traits: list[int]) -> list[Trait]:
        if(traits is not None):
            api_traits = [Trait(x) for x in self.client.traits.get(ids=traits)]
            return api_traits
        else:
            return []

    def _flatten(self, list_of_lists: list) -> list:
        return [item for sublist in list_of_lists for item in sublist]