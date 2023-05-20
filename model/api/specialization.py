#!/usr/bin/env python

from .utils import *

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
            self.id = get_or_none('id', data)
            self.name = get_or_none('name', data)
            self.profession = get_or_none('profession', data)
            self.elite = get_or_none('elite', data)
            self.icon = get_or_none('icon', data)
            self.background = get_or_none('background', data)
            self.minor_traits = [int(x) for x in get_list_or_empty('minor_traits', data)]
            self.major_traits = [int(x) for x in get_list_or_empty('major_traits', data)]
        