import click

from .generate_csv import parse_metars_and_write_csv
from models.logger import logger

@click.group()
def cliforecast():
    pass

@cliforecast.command()
@click.option('-s', '--station', required=True, type=str, help='The station ICAO code')
@click.option('-a', '--year-start', type=int, help='The start year to process')
@click.option('-e', '--year-end', type=int, help='The end year to process')
def parse_metars(station, year_start, year_end):
    if year_start is not None and year_end is not None:
        parse_metars_and_write_csv(station.upper(), year_start=year_start, year_end=year_end)
    elif year_start is not None:
        parse_metars_and_write_csv(station.upper(), year_start=year_start)
    elif year_end is not None:
        parse_metars_and_write_csv(station.upper(), year_end=year_end)
    else:
        parse_metars_and_write_csv(station.upper())
