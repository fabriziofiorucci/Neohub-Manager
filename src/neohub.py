#
# Heatmiser Neohub Gen 2 prometheus exporter
# https://www.heatmiser.com/neohub-smart-control/
#

import os
import time
import socket
import json

from prometheus_client import start_http_server, Gauge

# Exporter port
listen_port = os.environ['LISTEN_PORT'] if 'LISTEN_PORT' in os.environ else '8000'

# Neohub server
neohub_server = os.environ['SERVER'] if 'SERVER' in os.environ else ''
neohub_port = os.environ['SERVER_PORT'] if 'SERVER_PORT' in os.environ else '4242'

# Polling interval
polling_interval = os.environ['INTERVAL'] if 'INTERVAL' in os.environ else '5'


# Poll Neohub - returns a JSON payload
def poll_neohub():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((neohub_server, int(neohub_port)))
  s.sendall(b'{"GET_LIVE_DATA":0}\0\r')

  reply = tcp_recv(s,timeout=1)
  s.close()

  return json.loads(reply.replace('\n\0',''))


# Receive data from TCP socket
def tcp_recv(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)

    #total data partwise in an array
    total_data=[];
    data='';

    #beginning time
    begin=time.time()
    while True:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        #recv something
        try:
            data = the_socket.recv(8192)

            if data:
                total_data.append(data.decode('utf-8'))
                #change the beginning time for measurement
                begin = time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    # Join all parts to make final string
    return ''.join(total_data)


def update_prometheus_metrics(neohub_json: dict):
  neohub_prometheus.labels(name=neohub_json['ZONE_NAME'],variable='set_temperature').set(neohub_json['SET_TEMP'])
  neohub_prometheus.labels(name=neohub_json['ZONE_NAME'],variable='current_temperature').set(neohub_json['ACTUAL_TEMP'])
  neohub_prometheus.labels(name=neohub_json['ZONE_NAME'],variable='heating_on').set(neohub_json['HEAT_ON'])
  neohub_prometheus.labels(name=neohub_json['ZONE_NAME'],variable='away').set(neohub_json['AWAY'])
  neohub_prometheus.labels(name=neohub_json['ZONE_NAME'],variable='standby').set(neohub_json['STANDBY'])
  neohub_prometheus.labels(name=neohub_json['ZONE_NAME'],variable='low_battery').set(neohub_json['LOW_BATTERY'])
  neohub_prometheus.labels(name=neohub_json['ZONE_NAME'],variable='is_thermostat').set(neohub_json['THERMOSTAT'] if 'THERMOSTAT' in neohub_json else 0)


#
# Main
#
print("Heatmiser Neohub Prometheus Exporter")

if listen_port == '':
  print("LISTEN_PORT undefined")
  quit()

if neohub_server == '':
  print("SERVER undefined")
  quit()

if neohub_port == '':
  print("SERVER_PORT undefined")
  quit()

print(f"Using server {neohub_server}:{neohub_port}")
print(f"Polling interval is {polling_interval} seconds")

# Create a Prometheus gauge metric instance
neohub_prometheus = Gauge('neohub','Neohub data', ['name','variable'])

# Start the Prometheus HTTP server
print(f"Starting prometheus exporter on port {listen_port}")
start_http_server(int(listen_port))

# Update the metric every polling_interval seconds
while True:
    neohub = poll_neohub()

    if neohub is not None:
      for device in neohub['devices']:
        update_prometheus_metrics(device)

    time.sleep(int(polling_interval))
