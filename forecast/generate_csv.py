import os
from datetime import datetime
from rich.progress import track

from models.metar_class import MetarClass
from .console import console

today = datetime.now()

def _handle_metar(code):
    metar_date = code[0:12]
    metar = code[13:]
    date = datetime.strptime(metar_date, '%Y%m%d%H%M')
    return date, metar

def parse_metars_from_file(station, start_year=2005, end_year=today.year):
    main_path = os.getcwd()
    
    for year in range(start_year, end_year):
        path = main_path + f'/data/{station}/{year}.txt'
        lines = open(path, 'r').readlines()
        message = f'{station}: {year}...'
        for n in track(range(len(lines)), description=message):
            #console.print(f'[white]{lines[n]}', end='')
            metar_date, metar_code = _handle_metar(lines[n].replace('=', ''))
            try:
                metar = MetarClass(metar_date, metar_code)
            except Exception as error:
                console.print(f'\n\n[white]{lines[n]}')
                console.print(f'[bold rgb(175,0,0)]Parser Error: ', end='')
                console.print(f'[italic rgb(175,175,0)]{error}')
                error = 1
                exit()
            yield metar

def write_csv(station, start_year=2005, end_year=today.year):
    path = os.getcwd() + f'/data/{station}/'
    csv = open(path + 'data.csv', 'w')
    
    count = 0
    for metar in parse_metars_from_file(station.upper(), start_year=start_year, end_year=end_year):
        d = metar.to_dict()
        if count == 0:
            csv.write(','.join(header.capitalize() for header in d.keys()))
            csv.write('\n')
        count += 1
        csv.write(','.join(value for value in d.values()))
        csv.write('\n')
        yield list(metar.to_dict().keys())