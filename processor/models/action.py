import string
from numba import njit
from .actions import iot_commands


class ActionProcessor():
  active_model = None
  models = {
    'public': 'PUBLIC',
    'private': 'PRIVATE'
  }

  def __init__(self, model:str='public') -> None:
    self.active_model = self.models[model]

  def prompt(self, tokens:str, *args, **kwargs) -> str:
    action_prompt = cleanse_user_input(tokens)
    potential_action = detect_action_from_prompt(prompt=action_prompt)
    if callable(potential_action.get('function')):
      potential_action['result'] = potential_action['function'](
        inclusion_parameters=potential_action.get('inclusion_parameters')
      )
      return potential_action
    return None


def detect_action_from_prompt(prompt:str) -> dict:
  action_response = {}

  for action in iot_commands.command_dict.values():
    pas = prompt

    # Replace phrases with key phrase
    if 'alt_phrases' in action and 'key_phrase' in action:
      for alt_phrase in action['alt_phrases']:
        pas = pas.replace(alt_phrase, action['key_phrase'])

    # Check for at least 1 inclusion (and remove them from pas)
    if 'inclusions' in action:
      _inclusions = []
      if callable(action['inclusions']):
        action['inclusions'] = action['inclusions']()

      for inclusion in action['inclusions']:
        if inclusion.lower() in pas:
          _inclusions.append(inclusion)

      if len(_inclusions) == 0:
        continue

      action['inclusion_parameters'] = _inclusions

    # Remove excluded words from pas
    if 'exclusions' in action:
      if callable(action['exclusions']):
        action['exclusions'] = action['exclusions']()
      for exclusion in action['exclusions']:
        pas = pas.replace(' ' + exclusion + ' ', ' ')

    # Remove padding
    pas = pas.strip()
    while '  ' in pas:
      pas = pas.replace('  ', ' ')

    # Compare pas to key phrase
    if pas == action['key_phrase']:
      action_response = action
      break

    # Compare pas to triggers
    for trigger in action['triggers']:
      if calculate_similarity(trigger, pas) >= 0.33:
        action_response = action
        break

  return action_response


def cleanse_user_input(user_input:str) -> str:
  s = user_input.strip().lower()
  for punctuation in string.punctuation:
    s = s.replace(punctuation, '')
  while '  ' in s:
    s = s.replace('  ', ' ')
  s = ' ' + s + ' '
  return s


def calculate_similarity(str1, str2) -> float:
  set1 = set(str1.split(' '))
  set2 = set(str2.split(' '))
  intersection = len(set1.intersection(set2))
  union = len(set1.union(set2))
  return intersection / union
