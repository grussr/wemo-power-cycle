import pywemo
import time
import argparse

import socket

def internet_on(host="8.8.8.8", port=53, timeout=3):
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except socket.error as ex:
    print(ex)
    return False

parser = argparse.ArgumentParser()
parser.add_argument('wemo_ip')
parser.add_argument('--wait', default=60, type=int)
parser.add_argument('--check-ip', default='8.8.8.8')
args = parser.parse_args()
check_ip = args.check_ip

if (internet_on(check_ip)):
    exit()

address = args.wemo_ip
wait_time = args.wait

print('Probing for Wemo at %s...' % (address))
port = pywemo.ouimeaux_device.probe_wemo(address)
print('Found wemo on port %i' % (port))
url = 'http://%s:%i/setup.xml' % (address, port)
device = pywemo.discovery.device_from_description(url, None)

print('Wemo name: ' + device.name)
print("Turning off...")
device.off()
print("Waiting %i seconds..." % (wait_time))
time.sleep(wait_time)
print("Turning on...")
device.on()
