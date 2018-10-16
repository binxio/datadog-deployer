from collections import OrderedDict
from typing import List

from datadog import api


class Monitor(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def normalized(self) -> OrderedDict:
        property_order = [
            'name', 'type', 'query', 'message', 'options', 'tags', 'deleted'
        ]
        meta = {
            'id', 'matching_downtimes', 'created', 'created_at', 'creator',
            'org_id', 'modified', 'overall_state_modified', 'overall_state'
        }
        result = OrderedDict()

        for p in property_order:
            if p in self and self[p]:
                result[p] = order_dictionary(self[p])

        for p in self.keys():
            if p not in property_order and p not in meta:
                result[p] = self[p]

        return result


def order_dictionary(d):
    if isinstance(d, dict):
        result = OrderedDict()
        for key in sorted(d):
            result[key] = order_dictionary(d[key])
        return result
    else:
        return d


def read_all() -> List[Monitor]:
    result = []
    for monitor in api.Monitor.get_all():
        if 'deleted' not in monitor or not monitor['deleted']:
            result.append(Monitor(monitor))
    return result
