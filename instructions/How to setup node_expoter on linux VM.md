![node_exporter workflow](pngs/node_exporter_workflow.png)


## Steps

- Download `node_exporter` and extract the content to `bin` location.
  
  ```sh
  wget https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz
  tar -xvzf node_exporter-1.0.1.linux-amd64.tar.gz
  sudo mv node_exporter-1.0.1.linux-amd64/node_exporter /usr/local/bin/
  
  ```
 
- Add user to run it as a service and create service configuration file.

```sh
sudo useradd -rs /bin/false node_exporter
sudo bash -c  'cat << EOF >> /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF'

```

- Enable and start the service

```sh
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
sudo systemctl status node_exporter
```
