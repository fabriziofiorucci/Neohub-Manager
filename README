# Heatmiser Neohub Gen 2 Prometheus Exporter

This is a [Prometheus](https://prometheus.io/) exporter for [Neohub Gen 2](https://www.heatmiser.com/neohub-smart-control/)

# Prerequisites

- Docker 23.0+
- Kubernetes cluster
- Heatmiser Neohub Smart Heating Hub

# Building the image

The docker image can be built using:

```code
docker build -t neohub-prometheus-exporter:latest .
```

A pre-built image is available through docker hub:

```code
docker pull fiorucci/neohub-prometheus-exporter:latest
```

# Running

- On [Kubernetes](/contrib/kubernetes)
- Using [docker-compose](/contrib/docker-compose)

# Example output

```
$ curl http://127.0.0.1
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 334.0
python_gc_objects_collected_total{generation="1"} 0.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 33.0
python_gc_collections_total{generation="1"} 2.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="12",patchlevel="8",version="3.12.8"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 3.0912512e+07
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.1131264e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.73715446194e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 10.83
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 6.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP neohub Neohub data
# TYPE neohub gauge
neohub{name="Master Bedroom",variable="set_temperature"} 18.5
neohub{name="Master Bedroom",variable="current_temperature"} 18.5
neohub{name="Master Bedroom",variable="heating_on"} 0.0
neohub{name="Master Bedroom",variable="away"} 0.0
neohub{name="Master Bedroom",variable="standby"} 0.0
neohub{name="Master Bedroom",variable="low_battery"} 0.0
neohub{name="Master Bedroom",variable="is_thermostat"} 1.0
neohub{name="Hallway",variable="set_temperature"} 18.0
neohub{name="Hallway",variable="current_temperature"} 19.2
neohub{name="Hallway",variable="heating_on"} 0.0
neohub{name="Hallway",variable="away"} 0.0
neohub{name="Hallway",variable="standby"} 0.0
neohub{name="Hallway",variable="low_battery"} 0.0
neohub{name="Hallway",variable="is_thermostat"} 1.0
neohub{name="Upstairs Hall",variable="set_temperature"} 0.0
neohub{name="Upstairs Hall",variable="current_temperature"} 255.255
neohub{name="Upstairs Hall",variable="heating_on"} 0.0
neohub{name="Upstairs Hall",variable="away"} 0.0
neohub{name="Upstairs Hall",variable="standby"} 0.0
neohub{name="Upstairs Hall",variable="low_battery"} 0.0
neohub{name="Upstairs Hall",variable="is_thermostat"} 0.0
```
