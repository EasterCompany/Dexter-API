from iot import kasa
from models.data.language.english_lists import generics

command_dict = {
  "scan_network_for_devices": {
    "exclusions": lambda: generics + [
      'smart',
      'iot',
      'for',
      'available',
      'discoverable',
      'compatible',
      'accessible',
      'responding'
    ],
    "key_phrase": 'scan network',
    "alt_phrases": [
      'discover',
      'look',
      'search'
    ],
    "triggers": [
      'scan network device',
      'scan network kasa device',
      'scan network casa device',
      'scan network devices',
      'scan network kasa devices',
      'scan network casa devices'
    ],
    "function": kasa.scan_network_for_devices
  },

  "set_iot_device_power_state_on": {
    "inclusions": lambda: kasa.get_all_callable_iot_device_names(),
    "exclusions": lambda: [x for x in generics if x != 'on'] + kasa.get_all_callable_iot_device_names() + [
      'my', 'your', 'our'
    ],
    "key_phrase": 'on',
    "alt_phrases": [
      'up',
      'turn on',
      'power on',
      'switch on'
    ],
    "triggers": [
      'on',
    ],
    "function": kasa.set_device_power_state_on
  },

  "set_iot_device_power_state_off": {
    "inclusions": lambda: kasa.get_all_callable_iot_device_names(),
    "exclusions": lambda: [x for x in generics if x != 'off'] + kasa.get_all_callable_iot_device_names() + [
      'my', 'your', 'our'
    ],
    "key_phrase": 'off',
    "alt_phrases": [
      'down',
      'turn off',
      'power off',
      'switch off'
    ],
    "triggers": [
      'off',
    ],
    "function": kasa.set_device_power_state_off
  }
}
