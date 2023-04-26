#!/usr/bin/env python


class WeaponSkill:
    id: int
    slot: str

    def __init__(self, data: dict[str] = None) -> None:
        self.id = int(data['id'])
        self.slot = data['slot']


class Weapon:
    name: str
    specialization: int
    skills: list[WeaponSkill]

    def __init__(self, data: dict[str] = None) -> None:
        self.name = data['name']
        self.specialization = int(data['specialization'])
        if(data['skills'] is not None):
            self.skills = [WeaponSkill(x) for x in data['skills']]
    