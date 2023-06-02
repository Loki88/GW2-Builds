#!/usr/bin/env python

from .api_decorator import ApiDecorator
from datetime import datetime


class Build(ApiDecorator):

    def __init__(self, build_number: int) -> None:
        super().__init__(data={
            'build_number': build_number,
            'date': datetime.now()
        },
            attributes=['build_number', 'date'])
