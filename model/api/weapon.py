#!/usr/bin/env python


class WeaponSkill:
    id: int
    slot: str

    def __init__(self, data: dict[str] = None) -> None:
        self.id = int(data['id'])
        self.slot = data['slot']


class Weapon:
    name: str
    specialization: int # Weapons supported by all specializatiions will have None
    skills: list[WeaponSkill]

    def __init__(self, name: str, data: dict[str] = None) -> None:
        self.name = name
        self.specialization = data['specialization'] if 'specialization' in data else None
        if(data['skills'] is not None):
            self.skills = [WeaponSkill(x) for x in data['skills']]

    def __str__(self) -> str:
        return f'Weapon ({self.name}, spec: {self.specialization})'
    
    def __repr__(self):
        return str(self)
    
