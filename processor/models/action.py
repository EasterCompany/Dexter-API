import string
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
    action_prompt = self.cleanse_user_input(tokens)
    potential_action = self.detect_action_from_prompt(prompt=action_prompt)
    if potential_action is not None:
      potential_action['result'] = potential_action['function'](
        inclusion_parameters=potential_action.get('inclusion_parameters')
      )
      return potential_action
    return None

  def detect_action_from_prompt(self, prompt:str):
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

      # Compare pas to key phrase
      if pas == action['key_phrase']:
        return action

      # Compare pas to triggers
      for trigger in action['triggers']:
        if trigger in pas:
          return action

    return None

  def cleanse_user_input(self, user_input:str):
    s = user_input.strip().lower()

    # Remove punctuation
    for punctuation in string.punctuation:
      s = s.replace(punctuation, '')

    # Remove double (or greater) spacing
    while '  ' in s:
      s = s.replace('  ', ' ')
    s = ' ' + s + ' '

    return s
