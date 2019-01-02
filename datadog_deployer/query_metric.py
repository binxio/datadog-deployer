from datadog import api
from json import dump
from sys import stdout


def query_metric(query, start, end):
    results = api.Metric.query(start=start, end=end, query=query)
    dump(results, stdout)
