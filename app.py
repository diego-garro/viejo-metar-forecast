import click

from models.logger import logger
from forecast import cliforecast

@click.group()
def cliapp():
    pass

@cliapp.command()
def hello():
    click.echo('Hola mundo')

@cliapp.command()
def adios():
    click.echo('Adiós')

cli = click.CommandCollection(sources=[cliforecast, cliapp])

if __name__ == "__main__":
    cli()