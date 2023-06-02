#!/usr/bin/env python

from .loader import Loader
from data import *
from model import ItemType, ItemRarity, Build, Profession, Specialization, Trait, Skill,\
    ItemStats, Item, UpgradeComponentType, ConsumableType
from utils import flatten, no_duplicates


class ApiController():

    def __init__(self, professions_ids: list[str] = None) -> None:
        conn = Db().get_connection()
        loader = Loader()
        api_build: int = loader.load_build_id()
        build: Build = BuildRepository().get_build()
        if (build is None or build.build_number != api_build):
            professions = self._load_professions(loader, professions_ids)
            specializations = self._load_specializations(loader, professions)
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
        repository.save_profession(professions)
        return repository.get_professions()

    def _load_specializations(self, loader: Loader, professions: list[Profession]) -> list[Specialization]:
        repository = SpecializationsRepository()
        repository.delete_specializations()
        specializations = loader.load_specializations(
            no_duplicates(flatten([x.specializations for x in professions])))
        repository.save_specialization(specializations)
        return repository.get_specializations()

    def _load_traits(self, loader: Loader, specializations: list[Specialization]) -> list[Trait]:
        repository = TraitsRepository()
        repository.delete_trait()
        spec_traits = flatten(
            [flatten([x.minor_traits, x.major_traits]) for x in specializations])
        traits = loader.load_traits(spec_traits)
        repository.save_trait(traits)
        return repository.get_trait()

    def _load_skills(self, loader: Loader, traits: list[Trait]) -> list[Skill]:
        repository = SkillsRepository()
        repository.delete_skills()

        traits_skills = flatten([x.skills for x in traits])
        skills = loader.load_skills(traits_skills)
        return repository.save_skill(skills)

    def _load_stats(self, loader: Loader) -> list[ItemStats]:
        repository = StatsRepository()
        repository.delete_stats()
        stats = loader.load_item_stats()
        return repository.save_stat(stats)

    def _load_items(self, loader: Loader) -> list[Item]:
        items_filter = {
            ItemType.Armor: ItemRarity.Legendary,
            ItemType.Back: ItemRarity.Legendary,
            ItemType.Trinket: ItemRarity.Legendary,
            ItemType.UpgradeComponent: None,
            ItemType.Consumable: ItemRarity.Ascended,
            ItemType.Weapon: ItemRarity.Legendary
        }
        items = loader.load_items(items_filter=items_filter)
        items_dict = {}
        for item in items:
            if not item.type in items_dict:
                items_dict[item.type] = []
            items_dict[item.type].append(item)

        loaded_items = []

        if (ItemType.Armor in items_dict):
            loaded_items = loaded_items + \
                self._load_armor(items_dict[ItemType.Armor])

        if (ItemType.Weapon in items_dict):
            loaded_items = loaded_items + \
                self._load_weapon(items_dict[ItemType.Weapon])

        if (ItemType.Back in items_dict):
            loaded_items = loaded_items + \
                self._load_back(items_dict[ItemType.Back])

        if (ItemType.Trinket in items_dict):
            loaded_items = loaded_items + \
                self._load_trinkets(items_dict[ItemType.Trinket])

        if (ItemType.UpgradeComponent in items_dict):
            loaded_items = loaded_items + \
                self._load_upgrade_components(
                    items_dict[ItemType.UpgradeComponent])

        if (ItemType.Consumable in items_dict):
            loaded_items = loaded_items + \
                self._load_consumables(items_dict[ItemType.Consumable])

    def _load_armor(self, items: list[Item]) -> list[Item]:
        repository = ArmorRepository()
        repository.delete_armor()
        return repository.save_armor(items)

    def _load_weapon(self, items: list[Item]) -> list[Item]:
        repository = WeaponsRepository()
        repository.delete_weapon()
        return repository.save_weapon(items)

    def _load_back(self, items: list[Item]) -> list[Item]:
        repository = BackRepository()
        repository.delete_back()
        return repository.save_back(items)

    def _load_trinkets(self, items: list[Item]) -> list[Item]:
        repository = TrinketsRepository()
        repository.delete_trinket()
        return repository.save_trinket(items)

    def _load_upgrade_components(self, items: list[Item]) -> list[Item]:
        # upgrade components contain infusions, sigils and runes
        infu = self._load_infusions(
            [x for x in items if x.details.type == UpgradeComponentType.Default])
        sig = self._load_sigils(
            [x for x in items if x.details.type == UpgradeComponentType.Default])
        run = self._load_runes(
            [x for x in items if x.details.type == UpgradeComponentType.Default])
        return infu + sig + run

    def _load_infusions(self, items: list[Item]) -> list[Item]:
        repository = InfusionRepository()
        repository.delete_infusion()
        return repository.save_infusion(items)

    def _load_sigils(self, items: list[Item]) -> list[Item]:
        repository = SigilsRepository()
        repository.delete_sigil()
        return repository.save_sigil(items)

    def _load_runes(self, items: list[Item]) -> list[Item]:
        repository = RunesRepository()
        repository.delete_rune()
        return repository.save_rune(items)

    def _load_consumables(self, items: list[Item]) -> list[Item]:
        foods = self._load_foods(
            [x for x in items if x.details.type == ConsumableType.Food])
        utils = self._load_utilities(
            [x for x in items if x.details.type == ConsumableType.Utility])
        return foods + utils

    def _load_foods(self, items: list[Item]) -> list[Item]:
        repository = FoodsRepository()
        repository.delete_food()
        return repository.save_food(items)

    def _load_utilities(self, items: list[Item]) -> list[Item]:
        repository = UtilitiesRepository()
        repository.delete_utility()
        return repository.save_utility(items)
