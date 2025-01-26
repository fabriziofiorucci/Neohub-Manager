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


# Formats Neohub command '{"CMD_NAME":PARM}\0\r'
def make_neohub_command(cmd,parm):
  return '{"'+cmd+'":'+str(parm)+'}\0\r'


# Send command to Neohub - returns a JSON payload
def poll_neohub(cmd,parm):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((neohub_server, int(neohub_port)))
  s.sendall(make_neohub_command(cmd=cmd,parm=parm).encode())

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


def update_prometheus_metrics(live_data: dict, hours_run: dict):
  zn = live_data['ZONE_NAME']

  neohub_prometheus.labels(name=zn,variable='set_temperature').set(live_data['SET_TEMP'])
  neohub_prometheus.labels(name=zn,variable='current_temperature').set(live_data['ACTUAL_TEMP'])
  neohub_prometheus.labels(name=zn,variable='heating_on').set(live_data['HEAT_ON'])
  neohub_prometheus.labels(name=zn,variable='away').set(live_data['AWAY'])
  neohub_prometheus.labels(name=zn,variable='standby').set(live_data['STANDBY'])
  neohub_prometheus.labels(name=zn,variable='low_battery').set(live_data['LOW_BATTERY'])
  neohub_prometheus.labels(name=zn,variable='is_thermostat').set(live_data['THERMOSTAT'] if 'THERMOSTAT' in live_data else 0)
  neohub_prometheus.labels(name=zn,variable='hours_run').set(hours_run['today'][zn])


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
    live_data = poll_neohub(cmd="GET_LIVE_DATA",parm=0)

    if live_data is not None:
      for device in live_data['devices']:
        device_id = device['DEVICE_ID']
        hours_run = poll_neohub(cmd="GET_HOURSRUN",parm=device_id)

        update_prometheus_metrics(live_data=device, hours_run=hours_run)

    time.sleep(int(polling_interval))
