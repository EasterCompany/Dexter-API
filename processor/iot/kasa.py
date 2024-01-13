import asyncio
import urllib.parse
from kasa import Discover


def scan_network_for_devices(*args, **kwargs):
  from worker import REDIS_DB
  devices = []
  found_devices = asyncio.run(Discover.discover())

  for dev in found_devices:
    cur_dev = {
      'ip': dev,
      'alias': found_devices[dev].alias,
      'type': str(found_devices[dev].device_type).replace('DeviceType.', '').lower()
    }
    REDIS_DB.hset(
      ("iot-device:" + urllib.parse.quote(cur_dev['alias'])).lower().strip(),
      mapping=cur_dev
    )
    devices.append(cur_dev)

  if len(devices) == 0:
    return "I couldn't find any compatible smart devices on the local network."

  if len(devices) == 1:
    for dev in devices:
      if dev['type'] != 'unknown':
        dev['type'] = 'smart ' + dev['type']
      return f"I found a compatible device called '{dev['alias']}' which is a {dev['type']} on {dev['ip']}"

  response = f"I found {len(devices)} compatible devices on the local network.\n"
  for dev in devices:
    response += f"\n{dev['alias']} ({dev['type']}): {dev['ip']}"


def set_device_power_state(power_on:bool, device_names:list, *args, **kwargs):
  from worker import REDIS_DB
  device_errors = []

  for device_name in device_names:
    device_id = f"iot-device:{urllib.parse.quote(device_name)}"
    device_ip = REDIS_DB.hget(device_id, 'ip')

    devices = asyncio.run(Discover.discover(target=device_ip, timeout=0.25))
    for device in devices:
      if devices[device].alias.lower() == device_name:
        if power_on:
          asyncio.run(devices[device].turn_on())
        else:
          asyncio.run(devices[device].turn_off())

    devices = asyncio.run(Discover.discover(target=device_ip, timeout=0.25))
    for device in devices:
      if devices[device].alias.lower() == device_name:
        if power_on and devices[device].is_off:
          device_errors.append(device_name)
        elif not power_on and devices[device].is_on:
          device_errors.append(device_name)

  if len(device_errors) == 0:
    return "Done."

  if len(device_errors) == 1:
    return f"Sorry, I can't seem to turn {'on' if power_on else 'off'} {device_errors[0]}"

  return f"Some devices didn't respond to my command:\n\n" + '\n'.join(device_errors)


def get_all_callable_iot_device_names():
  from worker import REDIS_DB
  device_names = []
  for key in REDIS_DB.scan_iter("iot-device:*"):
    device_names.append(urllib.parse.unquote(key).replace('iot-device:', '', 1))
  device_names.sort(key=len, reverse=True)
  return device_names


set_device_power_state_on = lambda inclusion_parameters: set_device_power_state(
  power_on=True,
  device_names=inclusion_parameters
)

set_device_power_state_off = lambda inclusion_parameters: set_device_power_state(
  power_on=False,
  device_names=inclusion_parameters
)
