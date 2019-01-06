import yaml
config = {}
# read config file
with open("config.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("Error reading config file: ", exc)
        exit(1)

def get_config():
    return config
