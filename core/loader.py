#!/usr/bin/env python

from joblib import Parallel, delayed
from gw2api import GuildWars2Client
from model import Profession, Specialization, Trait, Skill, ItemType, ItemRarity, Item, ItemStats
from model.api.item import filter_item_data
from utils import flatten, no_duplicates, partition

HEAVY_PROFESSIONS = ['Guardian', 'Revenant', 'Warrior']
MEDIUM_PROFESSIONS = ['Engineer', 'Ranger', 'Thief']
LIGHT_PROFESSIONS = ['Elementalist', 'Mesmer', 'Necromancer']

HEAVY_SPECIALIZATIONS = [
    'Guardian',
    'Dragonhunter',
    'Firebrand',
    'Willbender',
    'Revenant',
    'Herald',
    'Renegade',
    'Vindicator',
    'Warrior',
    'Berserker'
    'Spellbreaker',
    'Bladesworn']

MEDIUM_SPECIALIZATIONS = [
    'Engineer',
    'Scrapper',
    'Holosmith',
    'Mechanist',
    'Ranger',
    'Druid',
    'Soulbeast',
    'Untamed',
    'Thief',
    'Daredevil',
    'Deadeye',
    'Specter']

LIGHT_SPECIALIZATIONS = [
    'Elementalist',
    'Tempest',
    'Weaver',
    'Catalyst',
    'Mesmer',
    'Chronomancer',
    'Mirage',
    'Virtuoso',
    'Necromancer',
    'Reaper',
    'Scourge',
    'Harbinger']

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

    def load_specializations(self, specializations: list[int]) -> list[Specialization]:
        if (specializations is not None):
            api_specializations = [Specialization(
                x) for x in self.client.specializations.get(ids=no_duplicates(specializations))]
            return api_specializations
        else:
            return []

    def load_traits(self, traits: list[int]) -> list[Trait]:
        if (traits is not None):
            chunks = list(partition(no_duplicates(traits), PARTITION_SIZE))
            jobs = PARALLEL_JOBS if PARALLEL_JOBS < len(chunks) else len(chunks)
            api_traits = Parallel(n_jobs=jobs)(delayed(self._load_traits_by_ids)(chunk)
                                               for chunk in chunks)
            return flatten(api_traits)
        else:
            return []

    def _load_traits_by_ids(self, traits: list[int]) -> list[Trait]:
        if (traits is not None):
            return [Trait(x) for x in self.client.traits.get(ids=traits)]
        else:
            return []

    def load_skills(self, skills: list[int] = None) -> list[Skill]:
        if (skills is None):
            skills = self.client.skills.get()

        chunks = list(partition(no_duplicates(skills), PARTITION_SIZE))
        jobs = PARALLEL_JOBS if PARALLEL_JOBS < len(chunks) else len(chunks)
        api_skills = Parallel(n_jobs=jobs)(delayed(self._load_skills_by_ids)(chunk)
                                           for chunk in chunks)
        return flatten(api_skills)

    def _load_skills_by_ids(self, skills: list[int]) -> list[Skill]:
        if (skills is not None):
            return [Skill(x) for x in self.client.skills.get(ids=skills)]
        else:
            return []

    def load_items(self, ids: list[int] = None, items_filter: dict[ItemType, ItemRarity] = None) -> list[Item]:
        items_id = ids
        if (items_id is None):
            items_id = [int(x) for x in self.client.items.get()]

        chunks = list(partition(no_duplicates(items_id), PARTITION_SIZE))
        jobs = PARALLEL_JOBS if PARALLEL_JOBS < len(chunks) else len(chunks)
        items = Parallel(n_jobs=jobs)(delayed(self._load_items_by_ids)
                                      (chunk, items_filter) for chunk in list(partition(items_id, PARTITION_SIZE)))
        return flatten(items)

    def _load_items_by_ids(self, items_ids: list[int], items_filter: dict[ItemType, ItemRarity] = None) -> list[Item]:
        return [Item(x) for x in self._filter_items(self.client.items.get(ids=items_ids), items_filter)]

    def _filter_items(self, items: list[dict], items_filter: dict[ItemType, ItemRarity] = None) -> list[Item]:
        if (items_filter is not None):
            return [x for x in items if filter_item_data(x, items_filter)]
        return items

    def load_item_stats(self) -> list[ItemStats]:
        item_stats_ids = self.client.itemstats.get()
        return [ItemStats(x) for x in self.client.itemstats.get(ids=item_stats_ids)]
