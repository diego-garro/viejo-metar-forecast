import click

from models.logger import logger
from forecast import forecast

@click.group()
def cliapp():
    pass

@cliapp.command()
@click.argument('name', type=click.STRING)
def hello(name):
    click.echo(f'Hola mundo, {name.upper()}')

@cliapp.command()
def adios():
    click.echo('Adiós')

cli = click.CommandCollection(sources=[forecast, cliapp])

if __name__ == "__main__":
    cli()