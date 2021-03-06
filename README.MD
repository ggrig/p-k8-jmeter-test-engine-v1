# 100k traffic generation

## The system overview

The traffic to the ICAP server is generated by working PODs running on dedicated JMeter nodes within a Kubernetes cluster. Along with the working Nodes/Pods, the cluster setup includes a Minio File Server, an InfluxDB Metrics Server, and a Grafana server with the corresponding dashboard(s).

![traffic](instructions/pngs/jmeter-test.png)

Each of the pods runs an instance of JMeter with X number of threads where each of the threads emulates the specified ICAP server user. So, "users" get files from the Minio file server, send those to the ICAP server to be processed/rebuild and then upload the rebuilt files back to the Minio file server. The metrics of the operations are gathered by JMeter and uploaded to InfluxDB. Grafana gets those metrics from InfluxDB and visualizes those in the dashboard.
Also, JMeter logs generated on the PODs are uploaded to the Minio server for further analysis.

## 1. Prerequisites

- An Azure AKS or Amazon EKS cluster  that can autoscale to have a sufficient number of nodes to run the test.

## 2. Provision a cluster

In order to deploy the cluster clone the current repo and nevigate to deployment/terraform 

For Azure AKS - ["Provision an AKS Cluster"](deployment/terraform/aks/README.MD)<br/>
For AWS EKS see ["Provision an EKS Cluster"](deployment/terraform/eks/README.md)

Note: The cluster deployment is done using Terraform Script which is tested on Linux Platform. Try and use Linux Platform for Cluster Deployment.

## 3. Load Generation Instructions
 - ["Using create_stack_dash.py to Create Load Generators and Corresponding Dashboards"](jmeter-icap/scripts/README.md)
 - ["How to generate Scaled Load Via UI"](instructions/How-to-generate-Scaled-Load-via-UI.md)
 - ["How to generate load against proxied Sharepoint site"](instructions/How-to-Generate-Load-against-Proxied-SharePoint.md)
