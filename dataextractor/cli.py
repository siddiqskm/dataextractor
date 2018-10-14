# -*- coding: utf-8 -*-

"""Console script for dataextractor."""
import sys
import click
from typing import Optional


@click.command()
def main(args: Optional[str] = None) -> int:
    """Console script for dataextractor."""
    click.echo("Replace this message by putting your code into "
               "dataextractor.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
