#!/usr/bin/env python

class Specialization():

    id: int
    name: str
    profession: str
    elite: bool
    icon: str
    background: str
    minor_traits: list[int] = []
    major_traits: list[int] = []

    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.id = data['id']
            self.name = data['name']
            self.profession = data['profession']
            self.elite = data['elite']
            self.icon = data['icon']
            self.background = data['background']
            self.minor_traits = [int(x) for x in data['minor_traits']]
            self.major_traits = [int(x) for x in data['major_traits']]
        