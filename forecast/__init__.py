import click

from rich.progress import track

from .generate_csv import write_csv, parse_metars_from_file
from models.logger import logger

@click.group()
def forecast():
    pass

@forecast.command()
@click.option('-a', '--start-year', type=int, help='The start year to process')
@click.option('-e', '--end-year', type=int, help='The end year to process')
@click.argument('station', type=click.STRING)
def parse_metars(station, start_year, end_year):
    if start_year is not None and end_year is not None:
        for metar in parse_metars_from_file(station.upper(), start_year=start_year, end_year=end_year):
            pass
    elif start_year is not None:
        for metar in parse_metars_from_file(station.upper(), start_year=start_year):
            pass
    elif end_year is not None:
        for metar in parse_metars_from_file(station.upper(), end_year=end_year):
            pass
    else:
        for metar in parse_metars_from_file(station.upper()):
            pass

@forecast.command()
@click.option('-a', '--start-year', type=click.INT, help='The start year to process')
@click.option('-e', '--end-year', type=click.INT, help='The end year to process')
@click.argument('station', type=click.STRING)
def export(station, start_year, end_year):
    if start_year is not None and end_year is not None:
        for dic in write_csv(station.upper(), start_year=start_year, end_year=end_year):
            pass
    elif start_year is not None:
        for dic in write_csv(station.upper(), start_year=start_year):
            pass
    elif end_year is not None:
        for dic in write_csv(station.upper(), end_year=end_year):
            pass
    else:
        for dic in write_csv(station.upper()):
            pass

if __name__ == '__main__':
    forecast()