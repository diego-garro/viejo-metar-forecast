import click

from rich.progress import track

from .generate_csv import write_csv, parse_metars_from_file
from .download_metars import download_metars_by_year, download_most_recent_metar
from models.logger import logger

@click.group()
def forecast():
    pass

@forecast.command()
@click.option('-s', '--start-year', type=int, help='The start year to process')
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
@click.option('-s', '--start-year', type=click.INT, help='The start year to process')
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

@forecast.command()
@click.option('-m', '--most-recent', is_flag=True)
@click.option('-s', '--start-year', type=click.INT, help='The start year to process')
@click.option('-e', '--end-year', type=click.INT, help='The end year to process')
@click.argument('station', type=click.STRING, required=True)
def download(most_recent, station, start_year, end_year):
    if most_recent:
        download_most_recent_metar(station)
    else:
        if start_year is not None and end_year is not None:
            download_metars_by_year(station, year_from=start_year, year_end=end_year)
        elif start_year is not None and end_year is None:
            download_metars_by_year(station, year_from=start_year)
        elif start_year is None and end_year is not None:
            download_metars_by_year(station, year_end=end_year)
        else:
            download_metars_by_year(station)

if __name__ == '__main__':
    forecast()