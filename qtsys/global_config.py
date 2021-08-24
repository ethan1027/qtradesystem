import yaml

with open('config.yml', 'r') as stream:
  try:
    global_config = yaml.safe_load(stream)
  except yaml.YAMLError as e:
    print(e)