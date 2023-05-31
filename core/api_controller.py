#!/usr/bin/env python

from .loader import Loader
from data import *
from model import ItemType, ItemRarity
from model.dao import *
from model.converter.api_to_dao import convert_profession, convert_specialization, convert_trait, convert_skill, convert_stats
from utils import flatten


class ApiController():

    def __init__(self, professions_ids: list[str] = None) -> None:
        loader = Loader()
        api_build: int = loader.load_build_id()
        build: Build = BuildRepository().get_build()
        if (build is None or build.build_number != api_build):
            professions = self._load_professions(loader, professions_ids)
            specializations = self._load_specializations(loader)
            traits = self._load_traits(loader, specializations)
            skills = self._load_skills(loader, specializations, traits)
            stats = self._load_stats(loader)
            items = self._load_items(loader)
            loader.load_items()

    def _load_professions(self, loader: Loader,  professions_ids: list[str] = None) -> list[Profession]:
        repository = ProfessionsRepository()
        repository.delete_professions()
        professions = None
        if (professions_ids is not None):
            professions = loader.load_professions(professions=professions_ids)
        else:
            professions = loader.load_professions()

        return repository.save_profession([convert_profession(x) for x in professions])

    def _load_specializations(self, loader: Loader, professions: list[Profession]) -> list[Specialization]:
        repository = SpecializationsRepository()
        repository.delete_specializations()
        specializations = loader.load_specializations(professions=professions)
        return repository.save_specialization([convert_specialization(x) for x in specializations])

    def _load_traits(self, loader: Loader, specializations: list[Specialization]) -> list[Trait]:
        repository = TraitsRepository()
        repository.delete_trait()
        spec_traits = flatten(
            [flatten([x.minor_traits, x.major_traits]) for x in specializations])
        traits = loader.load_traits(spec_traits)
        return repository.save_trait([convert_trait(x) for x in traits])

    def _load_skills(self, loader: Loader, traits: list[Trait]) -> list[Skill]:
        repository = SkillsRepository()
        repository.delete_skills()

        traits_skills = flatten([x.skills for x in traits])
        skills = loader.load_skills(traits_skills)
        return repository.save_skill([convert_skill(x) for x in skills])

    def _load_stats(self, loader: Loader) -> list[ItemStats]:
        repository = StatsRepository()
        repository.delete_stats()
        stats = loader.load_item_stats()
        return repository.save_stat([convert_stats(x) for x in stats])

    def _load_items(self, loader: Loader) -> list[Item]:
        items_filter = {
            ItemType.Armor: ItemRarity.Legendary,
            ItemType.Back: ItemRarity.Legendary,
            ItemType.Trinket: ItemRarity.Legendary,
            ItemType.UpgradeComponent: None,
            ItemType.Consumable: ItemRarity.Ascended
        }
        items = loader.load_items(items_filter=items_filter)
        items_dict = {}
        for item in items:
            if not item.type in items_dict:
                items_dict[item.type] = []
            items_dict[item.type].append(item)

        if (ItemType.Armor in items_dict):
            self._load_armor(items_dict[ItemType.Armor])

        # if(ItemType.Back in items_dict):
        #     self._load_back(items_dict[ItemType.Back])

        # if(ItemType.Trinket in items_dict):
        #     self._load_trinkets(items_dict[ItemType.Trinket])

        # if(ItemType.UpgradeComponent in items_dict):
        #     self._load_upgrade_components(items_dict[ItemType.UpgradeComponent])

        # if(ItemType.Consumable in items_dict):
        #     self._load_consumables(items_dict[ItemType.Consumable])

    def _load_armor(self, items: list[Item]) -> list[Item]:
        repository = ArmorRepository()
        repository.save_armor(items)
