from models.logger import logger
import click

@click.group()
def cliforecast():
    pass

@cliforecast.command()
def hello2():
    click.echo('Hola mundo desde hello 2')
