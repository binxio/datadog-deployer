from ruamel import yaml
from collections import OrderedDict
from datadog_deployer.monitor import Monitor, read_all


class LiteralString(str):
    pass


def ordered_dict_representer(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


def literal_string_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


def normalize(monitor: Monitor) -> OrderedDict:
    result = monitor.normalized()
    if 'message' in result:
        result['message'] = LiteralString(result['message'])
    return result


def dump(filename):
    yaml.add_representer(OrderedDict, ordered_dict_representer)
    yaml.add_representer(LiteralString, literal_string_representer)

    monitors = sorted(
        map(lambda m: normalize(m), read_all()), key=lambda m: m['name'])
    print('INFO: writing {} monitors to {}.'.format(len(monitors), filename))
    with open(filename, 'w') as stream:
        yaml.dump({
            'monitors': monitors
        },
                  stream=stream,
                  indent=2,
                  default_flow_style=False)
