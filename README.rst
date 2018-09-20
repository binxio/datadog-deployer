A simple command line utility to deploy datadog monitors from code.

**dump**

datadog-deployer dump 

dumps the current datadog monitor definitions to the `filename`

Options:
  --account TEXT   name of the Datadog account.
  --filename PATH  to dump the monitors to.
  --help           Show this message and exit.

**deploy**

datadog-deployer deploy

Deploys the datadog monitor definitions from `filename`. Compares the monitors with the deployed monitors and
determines for each monitor whether to insert or update. Monitors defined in datadog which are not in defined in the file are
left, unless `--force-delete` is specified.


Options:
  --account TEXT   name of the Datadog account.
  --filename PATH  to deploy monitors from.
  --verbose        showing change details that are applied.
  --dry-run        only show changes that would be applied.
  --force-delete   monitors in datadog not defined in the file.
  --help           Show this message and exit.


**Example**

Dump the current monitor definitions::

	$ datadog-deployer dump --filename dd-monitors.yaml

Update the monitor definitions::

	$ datadog-deployer deploy --filename dd-monitors.yaml
	INFO: 5 inserts, 1 updates, 2 unmanaged and 33 unchanged.
	INFO: "VPN connectivity" not defined in file. use --force-delete to delete.
	INFO: "Invalid objects in Oracle" not defined in file. use --force-delete to delete.

If you want to delete unmanaged monitors, type::

	$ datadog-deployer deploy --filename dd-monitors.yaml --force-delete 
	INFO: 0 inserts, 0 updates, 2 deletes and 39 unchanged.

**File formats**
The file ~/.datadog.ini is a Python configuration file from which the Datadog connection parameters are read.  At least it will
need the `api_key` and `api_app` attributes in the section DEFAULT::

	[DEFAULT]
	api_key=a77aaaaaaaaaaaaaaaaaaaaa
	app_key=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb

Other attributes you can add are: `proxies`, `api_host`, `statsd_host`, `statsd_port`, `statsd_socket_path`, `cacert`, `mute`

