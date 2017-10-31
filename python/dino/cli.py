import click

@click.command()
@click.option('-n', '--num-workers', default=1, type=int, help='number of workers')
def cli(num_workers):
    click.echo('Hello! Welcome to Dino!')
