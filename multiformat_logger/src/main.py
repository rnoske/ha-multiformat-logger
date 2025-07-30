import logging
import click

@click.command()
@click.option('--message', default='Hello World', help='Message to log')
@click.option('--level', default='info', type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']), help='Log level')
def main(message: str, level: str):
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('multiformat_logger')
    getattr(logger, level)(message)

if __name__ == '__main__':
    main()
