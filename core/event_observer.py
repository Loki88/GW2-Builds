#!/usr/bin/env python

from abc import ABC, abstractmethod
from enum import Enum, auto


class EventType(Enum):
    INIT = auto()


class Event():

    def __init__(self, description: str, severity: EventType):
        self.description = description
        self.severity = EventType


class EventObserver(ABC):

    @abstractmethod
    def observe(self, event: Event):
        pass
