import sys
from ruamel import yaml
from datadog_deployer.monitor import Monitor, read_all
from typing import List
from datadog import api


def calculate_operations(new_monitors: List[Monitor]):
    monitors = {v['name']: v for v in new_monitors}
    deployed = {v['name']: v for v in read_all()}

    insert = []
    delete = []
    update = []
    noop = []

    for name, monitor in monitors.items():
        if name in deployed:
            if monitor.normalized() == deployed[name].normalized():
                noop.append(monitor)
            else:
                monitor['id'] = deployed[name]['id']
                update.append(monitor)
        else:
            insert.append(monitor)

    for name, monitor in deployed.items():
        if name not in monitors:
            monitor['id'] = deployed[name]['id']
            delete.append(monitor)

    return insert, update, delete, noop


def deploy(filename, force_delete=False, verbose=True, dry_run=True):
    errors = []
    with open(filename, 'r') as stream:
        dsc = yaml.load(stream, Loader=yaml.Loader)

    monitors = list(map(lambda m: Monitor(m), dsc['monitors']))
    inserts, updates, deletes, noops = calculate_operations(monitors)
    print('INFO: {} inserts, {} updates, {} {} and {} unchanged.'.format(
        len(inserts), len(updates), len(deletes),
        ('deletes' if force_delete else 'unmanaged'), len(noops)))

    for monitor in inserts:
        if dry_run or verbose:
            print('INFO: inserting "{}"'.format(monitor['name']))
        if not dry_run:
            result = api.Monitor.create(**monitor)
            if 'errors' in result:
                errors.append(result['errors'])
                sys.stderr.write('ERROR: {}\n'.format(result['errors']))

    for monitor in updates:
        if dry_run or verbose:
            print('INFO: updating "{}"'.format(monitor['name']))
        if not dry_run:
            result = api.Monitor.update(**monitor)
            if 'errors' in result:
                errors.append(result['errors'])
                sys.stderr.write('ERROR: {}\n'.format(result['errors']))

    if force_delete:
        for monitor in deletes:
            if dry_run or verbose:
                print('INFO: deleting "{}"'.format(monitor['name']))
            if not dry_run:
                result = api.Monitor.delete(id=monitor['id'])
                if 'errors' in result:
                    errors.append(result['errors'])
                    sys.stderr.write('ERROR: {}\n'.format(result['errors']))
    else:
        for monitor in deletes:
            if dry_run or verbose:
                print(
                    'INFO: "{}" not defined in file. use --force-delete to delete.'
                    .format(monitor['name']))

    if errors:
        sys.exit(1)
