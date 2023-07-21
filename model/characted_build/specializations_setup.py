#!/usr/bin/env python

from enum import Enum
from model.api import Specialization


class SpecializationTraitsSetup():

    class Slot(Enum):
        TRAIT_1 = 1
        TRAIT_2 = 3
        TRAIT_3 = 5
        MINOR_TRAIT_1 = 0
        MINOR_TRAIT_2 = 2
        MINOR_TRAIT_3 = 4

    def __init__(self, specialization: Specialization) -> None:
        super().__init__()
        self.specialization = specialization
        self.traits = (self._get_minor_trait(0), None,
                       self._get_minor_trait(1), None,
                       self._get_minor_trait(2), None)

    def _get_minor_trait(self, pos: int) -> int:
        return self.specialization.minor_traits[pos]

    def is_elite(self) -> bool:
        return self.specialization.elite

    def set_trait(self, slot: Slot, trait: int):
        if (slot in [SpecializationTraitsSetup.Slot.TRAIT_1,
                     SpecializationTraitsSetup.Slot.TRAIT_2,
                     SpecializationTraitsSetup.Slot.TRAIT_3]):
            self.traits[slot.value] = trait
        else:
            raise ValueError(slot)

    def get_traits(self) -> tuple[int, int, int, int, int, int]:
        return self.traits

    def get_trait(self, slot: Slot):
        return self.traits[slot.value]


class SpecializationsSetup():

    class Slot(Enum):
        SLOT_1 = 0
        SLOT_2 = 1
        SLOT_3 = 2

    def __init__(self) -> None:
        super().__init__()
        self.specializations = tuple(None, None, None)

    def _is_elite_set(self):
        return any(x.is_elite() for x in self.specializations)

    def set_specialization(self, slot: Slot, specialization: Specialization):
        self.specializations[slot.value] = SpecializationTraitsSetup(specialization)
