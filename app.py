import click

from models.logger import logger
from forecast import forecast

@click.group()
def cliapp():
    pass

@cliapp.command()
def hello():
    click.echo('Hola mundo')

@cliapp.command()
def adios():
    click.echo('Adiós')

cli = click.CommandCollection(sources=[forecast, cliapp])

if __name__ == "__main__":
    cli()