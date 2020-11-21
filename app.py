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
@click.option('-s', '--station', required=True, type=str, help='The station ICAO code')
@click.option('-a', '--year-start', type=int, help='The start year to process')
@click.option('-e', '--year-end', type=int, help='The end year to process')
def parsemetars(station, year_start, year_end):
    if year_start is not None and year_end is not None:
        parse_metars_and_write_csv(station.upper(), year_start=year_start, year_end=year_end)
    elif year_start is not None:
        parse_metars_and_write_csv(station.upper(), year_start=year_start)
    elif year_end is not None:
        parse_metars_and_write_csv(station.upper(), year_end=year_end)
    else:
        parse_metars_and_write_csv(station.upper())

cli = click.CommandCollection(sources=[cliforecast, cliapp])

if __name__ == "__main__":
    cli()