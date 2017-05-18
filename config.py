import os
import json

MONKEY_ROOT = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(MONKEY_ROOT, 'config.json')) as f:
    MONKEY_CONFIG = json.load(f)

