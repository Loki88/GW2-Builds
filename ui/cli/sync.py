#!/usr/bin/env python

import click
from .cli import cli, CtxObjects

from core import ApiController


@cli.command()
@click.pass_context
def sync(ctx: click.Context):
    click.echo(click.style('Welcome to GW2-Builds!', fg='green'))
    if (ctx.obj[CtxObjects.CLEAR.name]):
        click.echo(click.style('ATTENTION: clearing existing data.', blink=True, bold=True))
        # TODO: clearing is included in ApiController.__init__ and it will need a rework

    with click.progressbar(range(1), label='Checking for GW2 updates (this could take some time)'):
        ctx.api = ApiController(wipe_existing=ctx.obj[CtxObjects.CLEAR.name])
        # TODO: update process should be monitorable (Observer pattern)

    ctx.get_build()
    click.echo(click.style('ATTENTION: clearing existing data.', blink=True, bold=True))

    # print menu
