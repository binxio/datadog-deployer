import sys
from os import path
from configparser import ConfigParser
from datadog import initialize

allowed_properties = {
    'api_key', 'app_key', 'proxies', 'api_host', 'statsd_host', 'statsd_port',
    'statsd_socket_path', 'cacert', 'mute'
}


def read(section: str = 'DEFAULT'):
    """
    reads the ~/.datadog.ini `section` with the following allowed properties

    :param section identifying a specific datadog account


    api_key: Datadog API key
    type api_key: string

    app_key: Datadog application key
    type app_key: string

    proxies: Proxy to use to connect to Datadog API
    type proxies: dictionary mapping protocol to the URL of the proxy.

    api_host: Datadog API endpoint
    type api_host: url

    statsd_host: Host of DogStatsd server or statsd daemon
    type statsd_host: address

    statsd_port: Port of DogStatsd server or statsd daemon
    type statsd_port: port

    statsd_use_default_route: Dynamically set the statsd host to the default route
    (Useful when running the client in a container)
    type statsd_use_default_route: boolean

    statsd_socket_path: path to the DogStatsd UNIX socket. Supersedes statsd_host
    and stats_port if provided.

    cacert: Path to local certificate file used to verify SSL \
        certificates. Can also be set to True (default) to use the systems \
        certificate store, or False to skip SSL verification
    type cacert: path or boolean

    mute: Mute any ApiError or ClientError before they escape \
        from datadog.api.HTTPClient (default: True).
    type mute: boolean
    """
    parser = ConfigParser()
    parser.read(path.expanduser('~/.datadog.ini'))
    return {
        k: v
        for (k, v) in parser.items(section) if k in allowed_properties
    }


def connect(section: str = 'DEFAULT'):
    kwargs = read(section)
    if 'api_key' in kwargs and 'app_key' in kwargs:
        initialize(**kwargs)
    else:
        sys.stderr.write(
            'ERROR: api_key/app_key missing from ~/.datadog.ini\n')
        sys.exit(1)
