#!/usr/bin/env python

import click

import ui.cli


@click.group(invoke_without_command=True)
@click.option("--gui", default=False, help="Use GUI")
@click.option("--clear", default=False, help="Clear all cached data")
def main(ctx: click.Context, gui: bool, clear: bool):
    if not gui:
        ui.cli.sync(ctx, clear)


if __name__ == '__main__':
    main(obj={})
