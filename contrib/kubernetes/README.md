# Running on Kubernetes

1. Configure the relevant fields in the [Kubernetes manifest](/contrib/kubernetes/neohub-prometheus-exporter.yaml)
- `<DOCKER_IMAGE_NAME>` - The docker image (default: `fiorucci/neohub-prometheus-exporter:latest`)
- `<SERVER>` - Neohub IP address or FQDN
- `<SERVER_PORT>` - Neohub TCP port, defaults to 4242
- `<INTERVAL>` - Polling interval to collect telemetry from Neohub
- `<NEOHUB_EXPORTER_FQDN>` - FQDN published through the Kubernetes Ingress Controller

2. Deploy the manifest:

```
kubectl apply -f neohub-prometheus-exporter.yaml
```

3. Test the prometheus scraping endpoint:

```
curl http://<NEOHUB_EXPORTER_FQDN>
```
