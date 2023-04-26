#!/usr/bin/env python

import click


@click.command()
@click.option("--profession", default=None, help="Profession for generating a rotation")
def main():
    pass

if __name__ == '__main__':
    main()