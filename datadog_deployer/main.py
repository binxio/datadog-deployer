import click
from datadog_deployer import dump
from datadog_deployer import deploy
from datadog_deployer import connect


@click.group()
def main():
    pass


@main.command(name='dump')
@click.option(
    '--account',
    required=False,
    default="DEFAULT",
    help='name of the Datadog account.')
@click.option(
    '--filename',
    required=True,
    type=click.Path(exists=False, file_okay=True),
    help='to dump the monitors to.')
def do_dump(account, filename):
    connect(account)
    dump(filename)


@main.command(name='deploy')
@click.option(
    '--account',
    required=False,
    default="DEFAULT",
    help='name of the Datadog account.')
@click.option(
    '--filename',
    required=True,
    type=click.Path(exists=True, file_okay=True),
    help='to deploy the monitors from.')
@click.option(
    '--verbose',
    default=False,
    is_flag=True,
    help='showing change details that are applied.')
@click.option(
    '--dry-run',
    default=False,
    is_flag=True,
    help='only show changes that would be applied.')
@click.option(
    '--force-delete',
    default=False,
    is_flag=True,
    help='monitors in datadog not defined in the file.')
def do_deploy(account, filename, force_delete, verbose, dry_run):
    connect(account)
    deploy(
        filename, force_delete=force_delete, verbose=verbose, dry_run=dry_run)


if __name__ == '__main__':
    main()
