# Using create_stack_dash.py to Create Load Generators and Corresponding Dashboards


## Table of Contents
  * [Introduction](#introduction)
  * [Prerequisites](#prerequisites)
  * [Using config.env to pass parameters to create_stack_dash.py](#using-configenv-to-pass-parameters-to-create_stack_dashpy)
  * [Options available for the create_stack_dash.py script](#optionsparameters-available-for-the-create_stack_dashpy-script)
  * [How create_stack_dash.py works](#how-create_stack_dashpy-works)
  * [Running the create_stack_dash.py script](#running-the-create_stack_dashpy-script)
  * [Troubleshooting](#troubleshooting)


## Introduction

This script launches number of pods depend on user count and generate traffic to provided endpoint then creates Grafana Dashboards that display various metrics from said traffic generators.

## Prerequisites

Note: Make sure you have cloned the repo - [https://github.com/k8-proxy/p-k8-jmeter-test-engine.git](https://github.com/k8-proxy/p-k8-jmeter-test-engine.git)

1. Install Python version 3.8 or later (see [Python](https://www.python.org/downloads/))

2. Ensure necessary python packages are installed. Navigate to the scripts folder where the file "requirements.txt" exists, then use the following console command in the terminal:
```
    pip3 install -r requirements.txt
```

3. Nevigate to jmeter-icap/scripts and Create a new config.env file or modify [the existing one here](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/jmeter-icap/scripts/config.env) provided as a sample file. Update the values there to correspond to your test setup - [refer to the table of parameters available below](#options-available-for-the-create-stack-dashpy-script)

5. If using AWS Secrets Manager to store the Grafana API Key, a secret name would need to be provided either in the config.env file or via the command line:

```
GRAFANA_SECRET=MyGrafanaSecretName
```

or

```
python create_stack_dash.py -gs MyGrafanaSecretName
```

## Using config.env to pass parameters to create_stack_dash.py

The config.env file is the preferred way to pass parameters to this script, it should be located in the same folder as create_stack_dash. It contains many parameters that translate to options (listed in options section below) when running the script. For a more detailed description of each parameter, [refer to the table of parameters available below](#options-available-for-the-create-stack-dashpy-script). Below is a sample config.env file:

```
AWS_PROFILE_NAME=default
REGION=eu-west-1
TOTAL_USERS=100
USERS_PER_INSTANCE=25
DURATION=300
TEST_DATA_FILE=files.csv
MINIO_URL=http://minio.minio.svc.cluster.local:9000
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_INPUT_BUCKET=input
MINIO_OUTPUT_BUCKET=output
INFLUXDB_URL=http://influxdb.influxdb.svc.cluster.local:8086
PREFIX=dash-creation
ICAP_SERVER_URL=gw-icap01.westeurope.azurecontainer.io
GRAFANA_URL=a6f57c69583674ff982787e2cbe95cea-713263438.eu-west-1.elb.amazonaws.com
GRAFANA_KEY=
GRAFANA_FILE=../grafana_dashboards/k8-test-engine-dashboard.json
EXCLUDE_DASHBOARD=0
PRESERVE_STACK=0
ICAP_SERVER_PORT=1344
ENABLE_TLS=0
TLS_VERIFICATION_METHOD=no-verify
STORE_RESULTS=1
GRAFANA_USERNAME=admin
GRAFANA_PASSWORD=admin
TENANT_ID=
CLIENT_ID=
CLIENT_SECRET=
```

These parameters have corresponding options that can be used during script execution, they do not have to be set in config.env. Many of the parameters above are also optional, they can be omitted. Any options input manually via the command line will override options within the config.env file. For example, if the config.env file is set to allow dashboard creation:

```
EXCLUDE_DASHBOARD=0
```

But the option to exclude dashboard creation is used:

```
python create_stack_dash.py -x
```
The Dashboard will still not be created (the option -x prevents dashboard creation) despite the content of the config.env file.

## Options/Parameters available for the create_stack_dash.py script

To see the available options for when running the script, use:
```
python create_stack_dash.py -h
```

Below is a table highlighting all the available options. These options correspond to parameters in the config.env file, they share the same names/descriptions and can be used as a reference when creating your own config.env file.

<table>
<tr>
<td width="200"> Option </td> <td> Config.env Parameter </td>  <td> Description </td>
</tr>
<tr>
<td> --total_users, -t </td>  <td> TOTAL_USERS </td>
<td>
Total number of users for the test, Default value is 4000.
</td>
</tr>
<tr>
<td> --users_per_instance, -u </td> <td> USERS_PER_INSTANCE </td>
<td>
Number of users per instance (default: 25)
</td>
</tr>
<tr>
<td> --duration, -d </td> <td>DURATION</td>
<td>
Duration of the test, default value: 900 seconds
</td>
</tr>
<tr>
<td> --list, -l </td> <td>TEST_DATA_FILE</td>
<td>
Path to the test data file that contains the list of files used for testing
</td>
</tr>
<tr>
<td> --minio_url, -m </td> <td>MINIO_URL</td>
<td>
Minio URL
</td>
</tr>
<tr>
<td> --minio_access_key, -a </td> <td>MINIO_ACCESS_KEY</td>
<td>
Minio access key
</td>
</tr>
<tr>
<td> --minio_secret_key, -s </td> <td>MINIO_SECRET_KEY</td>
<td>
Minio secret key
</td>
</tr>
<tr>
<td> --minio_input_bucket, -i </td> <td>MINIO_INPUT_BUCKET</td>
<td>
Minio input bucket name
</td>
</tr>
<tr>
<td>--minio_output_bucket, -o </td> <td>MINIO_OUTPUT_BUCKET</td>
<td>
Minio output bucket name
</td>
</tr>
<tr>
<td> --influxdb_url, -x </td> <td>INFLUXDB_URL</td>
<td>
URL to Influx Database
</td>
</tr>
<tr>
<td> --prefix, -p </td> <td>PREFIX</td>
<td>
Prefix for stack name (default: "")
</td>
</tr>
<tr>
<td> --icap_server_url, -v </td> <td>ICAP_SERVER_URL</td>
<td>
ICAP server endpoint URL
</td>
</tr>
<tr>
<td> --grafana_url, -g </td> <td>GRAFANA_URL</td>
<td>
The URL to the Grafana database's home page (typically this would be the "MachineIP:3000")
</td>
</tr>
<tr>
<td> --grafana_file, -f </td> <td>GRAFANA_FILE</td>
<td>
This takes the tag of the server containing the Grafana database; this server will automatically be started if it is stopped. Tags in AWS have both a key and a value. The key field should contain "Name", only the value of the tag is what should be provided to this option. The tag must have a value field; it should not be empty. (Note: The --grafana_url option will prevent this option from taking effect, as the Grafana server IP would be obtained directly from that).
</td>
</tr>
<tr>
<td>--grafana_secret, -gs</td> <td>GRAFANA_SECRET</td>
<td>
The secret name of the Grafana API Key inside AWS Secrets Manager. This will be used to retrieve the key for use when generating Grafana dashboards. (Note: The --grafana_key option will prevent this option from taking effect; a user directly providing a key would negate the need for a key lookup).
</td>
</tr>
<tr>
<td> --preserve_stack, -s </td> <td>PRESERVE_STACK</td>
<td>
This takes no arguments. If set (ex: create_stack_dash -s), it will prevent the stack created from being automatically deleted after the duration period specified above is complete.
</td>
</tr>
<tr>
<td> --exclude_dashboard, -x </td> <td>EXCLUDE_DASHBOARD</td>
<td>
This takes no arguments. If set (ex: create_stack_dash -x), a Grafana dashboard will not be created when the script is run.
</td>
</tr>
<tr>
<td> --icap_server_port, -port </td> <td>ICAP_SERVER_PORT</td>
<td>
Port used for ICAP server
</td>
</tr>
<tr>
<td> --tls_verification_method, -tls </td> <td>ENABLE_TLS</td>
<td>
Whether or not to enable TLS (=0: disabled, =1: enabled)
</td>
</tr>
<tr>
<td> --enable_tls, -et </td> <td>TLS_VERIFICATION_METHOD</td>
<td>
Method used for TLS verification
</td>
</tr>
<tr>
<td> --load_type, -load </td> <td>LOAD_TYPE</td>
<td>
Type of load being generated: "Direct", "Proxy" or "SharePoint"
</td>
</tr>
<tr>
<tr>
<td> --store_results, -sr </td> <td>STORE_RESULTS</td>
<td>
If set through args (ex: create_stack_dash -sr), test results will not be stored in the database. In config.env, =0: false, =1: true.
</td>
</tr>
<tr>
<td> --grafana_username, -un </td> <td>GRAFANA_USERNAME</td>
<td>
Grafana username to use for Grafana dashboard creation. If this is provided, the grafana_password parameter must also be passed to the script via args or config.env. If an API key is provided, this will not be used.
</td>
</tr>
<tr>
<td> --grafana_password, -pw </td> <td>GRAFANA_PASSWORD</td>
<td>
Grafana password to use for Grafana dashboard creation. If this is provided, the grafana_username parameter must also be passed to the script via args or config.env. If an API key is provided, this will not be used.
</td>
</tr>
<td> --sharepoint_ip, -spip </td> <td>SHAREPOINT_IP</td>
<td>
Sharepoint IP address that will be used in load generators
</td>
</tr>
<tr>
<td> --sharepoint_host_names, -sphosts </td> <td>SHAREPOINT_HOST_NAMES</td>
<td>
SharePoint Hostnames that will be used in load generators
</td>
</tr>
<tr>
<td>--tenant_id, -tid</td><td>TENANT_ID</td>
<td>
Tenant ID value (for use with SharePoint)
</td>
</tr>
<tr>
<td>--client_id, -cid</td><td>CLIENT_ID</td>
<td>
Client ID value (for use with SharePoint)
</td>
</tr>
<tr>
<td>--client_secret, -cs</td><td>CLIENT_SECRET</td>
<td>
Client Secret value (for use with SharePoint)
</td>
</tr>
</table>

## How create_stack_dash.py works

![how_create_stack_dash_works](pngs/create_stack_dash.png)

## Running the create_stack_dash.py script

To run the create_stack_dash.py script, use the following command:
```
python create_stack_dash.py
```

Followed by the options required. This can be done manually, as seen in this example:
```
python create_stack_dash.py -f "grafana_template.json" -k "grafana key" -g "link to grafana home page" -p "test-prefix"
```
Or the Config.env file would contain all the parameters required.

A successful run should output information on number of number of PODs to be cleated and Grafana dashboard. See the example below:
```
...
INFO:create_stack:Number of pods to be created: 1
job.batch/demo-jmeterjob created
Creating dashboard...
Stack will be deleted after 20.0 minutes
0.0 minutes have elapsed, stack will be deleted in 20.0 minutes
10.0 minutes have elapsed, stack will be deleted in 10.0 minutes
...
```

## Troubleshooting

Below is a list of potential issues end users might face along with some suggested solutions:

### Grafana Dashboard is not being created
- Check that the "exclude_dashboard" option is not enabled
- The grafana_key or grafana_secret_id options in config.env must be entered correctly (grafana_secret_id should refer to the name of the secret in AWS Secrets Manager)
- Grafana API Key must have correct permissions (must be Editor or Admin) and that it has not expired. [See this file](https://github.com/k8-proxy/aws-jmeter-test-engine/blob/master/jmeter-icap/instructions/how-to-use-create_dashboards-script.md) for more information on how to create a Grafana API Key.
- If using a custom Grafana URL, make sure the correct port is being used (default port is 3000)
- The machine running this script must have access to the server holding the Grafana instance (i.e. the IP for Grafan POD is exposed and have access outside cluster).
- The Grafana JSON template should be formatted correctly, for more information refer to the [Grafana Dashboard API](https://grafana.com/docs/grafana/latest/http_api/dashboard/).

### Grafana Dashboard is not being created
- make sure datasource is created on grafana when intialise first time. you can nevigate to data source from setting and test to make sure is connected to database.
- Check Jmeter logs to make sure the jmeter pods got access to the influxDB pods an the data base named 'jmeter' and 'icapserver' is created.

### Stacks are not being automatically deleted
- Ensure the option "preserve_stack" is not enabled
- create_stack_dash.py deletes only the stack that was created in an individual run. If the script is stopped before the delete process takes place (i.e. before the duration period + 15 minutes) for any reason, the stack it created will not be deleted and must be deleted manually.
