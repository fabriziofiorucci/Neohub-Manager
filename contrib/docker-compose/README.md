# Docker compose

Neohub Prometheus Exporter can be deployed using docker compose on a Linux virtual machine running docker-compose v2.20+

Running with docker-compose:

```code
git clone https://github.com/fabriziofiorucci/Neohub-Prometheus-Exporter
cd Neohub-Prometheus-Exporter/contrib/docker-compose
```

Edit `docker-compose.yaml` and configure the following fields:

- `image:` - The docker image (default: `fiorucci/neohub-prometheus-exporter:latest`)
- `server:` - Neohub IP address or FQDN
- `server_port` - Neohub TCP port, defaults to 4242
- `interval:` - Polling interval to collect telemetry from Neohub, default to 5 seconds

```code
docker-compose -f docker-compose.yaml up -d
```

Testing:

```code
curl 127.0.0.1:8000
```

Stopping:

```code
docker-compose -f docker-compose.yaml down
[+] Running 2/2
 ✔ Container neohub                Removed    0.3s 
 ✔ Network docker-compose_default  Removed    0.1s 
```
