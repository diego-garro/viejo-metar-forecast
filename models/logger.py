import logging

logger = logging

logger.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p',
    handlers=[
        logging.FileHandler('../logging.log'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logging.warning('mensaje a nivel warning')
    logging.info('mensaje a nivel info')
    logging.debug('mensaje a nivel debug')
    logging.error('ocurrió un error en la base de datos')