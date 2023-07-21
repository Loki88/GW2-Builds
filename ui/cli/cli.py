#!/usr/bin/env python

from enum import Enum, auto
import click


class CtxObjects(Enum):
    CLEAR = auto()


@click.group(chain=True)
@click.option("--clear", default=False, help="Clear all cached data")
@click.pass_context
def cli(ctx, clear: bool):
    ctx.ensure_object(dict)
    ctx.obj[CtxObjects.CLEAR.name] = clear
    click.echo('Clear cache: %b' % ('yes' if clear else 'no'))
