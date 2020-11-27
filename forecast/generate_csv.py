import click
from datetime import datetime

from models.metar_class import MetarClass

today = datetime.now()

def handle_metar(code):
    metar_date = code[0:12]
    metar = code[13:]
    date = datetime.strptime(metar_date, '%Y%m%d%H%M')
    return date, metar

def parse_metars_and_write_csv(station, year_start=2005, year_end=today.year):
    data = open(f'data/{station}/data.csv', 'w')
    
    for year in range(year_start, year_end):
        with open(f'data/{station}/{year}.txt', 'r') as f:
            for line in f:
                print(line, end='')
                metar_date, metar_code = handle_metar(line.replace('=', ''))
                try:
                    metar = MetarClass(metar_date, metar_code)
                except Exception as error:
                    click.echo(click.style('\nError: ', fg='red', bold=True), nl=False)
                    click.echo(click.style(str(error), fg='yellow'))
                    exit()