import click

from models.logger import logger
from forecast import cliforecast
from forecast.generate_csv import parse_metars_and_write_csv

@click.group()
def cliapp():
    pass

@cliapp.command()
def hello():
    click.echo('Hola mundo')

@cliapp.command()
def adios():
    click.echo('Adiós')

@cliapp.command()
@click.option('-s', '--station', required=True, type=str)
def parsemetars(station):
    parse_metars_and_write_csv(station.upper())

cli = click.CommandCollection(sources=[cliforecast, cliapp])

if __name__ == "__main__":
    cli()