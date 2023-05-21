#!/usr/bin/env python

from joblib import Parallel, delayed
from gw2api import GuildWars2Client
from model.api import Profession, Specialization, Trait, Skill, ItemType, ItemRarity, Item, ItemStats, filter_item_data

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

PARTITION_SIZE = 200
PARALLEL_JOBS = 15

class Loader():

    def __init__(self) -> None:
        self.client = GuildWars2Client()

    def __del__(self):
        self.client.session.close()
        
    def load_build_id(self) -> int:
        response = self.client.build.get()
        return response['id']

    def load_professions(self, professions: list[str] = ALL_PROFESSIONS) -> list[Profession]:
        response = self.client.professions.get(ids=professions)
        api_professions = [self._load_profession(x) for x in response]
        return api_professions
    
    def _load_profession(self, data: dict) -> Profession:
        return Profession(data)
    
    def load_specializations(self, professions: list[Profession]) -> list[Specialization]:
        if(professions is not None):
            return self._load_specializations(self._no_duplicates(self._flatten([x.specializations for x in professions])))
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
    
    def load_skills(self, skills: list[int]) -> list[Skill]:
        if(skills is not None):
            api_skills = [Skill(x) for x in self.client.skills.get(ids=self._no_duplicates(skills))]
            return api_skills
        else:
            return []
        
    def load_items(self, ids: list[int] = None, items_filter: dict[ItemType, ItemRarity] = None) -> list[Item]:
        items_id = ids
        if(items_id is None):
            items_id = [int(x) for x in self.client.items.get()]
        
        items = Parallel(n_jobs=PARALLEL_JOBS)(delayed(self._load_items_by_ids)(chunk, items_filter) for chunk in list(self._partition(items_id, PARTITION_SIZE)))
        return self._flatten(items)
    
    def _load_items_by_ids(self, items_ids: list[int], items_filter: dict[ItemType, ItemRarity] = None) -> list[Item]:
        return [Item(x) for x in self._filter_items(self.client.items.get(ids=items_ids), items_filter)]
    
    def _filter_items(self, items: list[dict], items_filter: dict[ItemType, ItemRarity] = None) -> list[Item]:
        if(items_filter is not None):
            return [x for x in items if filter_item_data(x, items_filter)]
        return items
    
    def load_item_stats(self) -> list[ItemStats]:
        item_stats_ids = self.client.itemstats.get()
        return [ItemStats(x) for x in self.client.itemstats.get(ids=item_stats_ids)]

    def _flatten(self, list_of_lists: list) -> list:
        return [item for sublist in list_of_lists for item in sublist]

    def _no_duplicates(self, list_with_duplicates: list) -> list:
        return list(dict.fromkeys(list_with_duplicates))
    
    def _partition(self, lst: list, chunks: int):
        for i in range(0, len(lst), chunks):
            yield lst[i:i + chunks]
        