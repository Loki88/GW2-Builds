#!/usr/bin/env python

from enum import Enum
from model.api import Specialization


class SpecializationTraitsSetup():

    def __init__(self, specialization: Specialization) -> None:
        super().__init__()
        self.specialization = specialization

    def is_elite(self) -> bool:
        return self.specialization.elite


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
