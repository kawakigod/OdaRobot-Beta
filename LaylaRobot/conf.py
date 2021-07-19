from envparse import env
from LaylaRobot import LOGGER

DEFAULTS = {
    "LOAD_MODULES": True,
    "REDIS_HOST": "localhost",
    "REDIS_PORT": 6379,
    "REDIS_DB_FSM": 1,
}

def get_str_key(name, required=False):
    if name in DEFAULTS:
        default = DEFAULTS[name]
    else:
        default = None
    if not (data := env.str(name, default=default)) and not required:
        LOGGER.warn("No str key: " + name)
        return None
    elif not data:
        LOGGER.critical("No str key: " + name)
        sys.exit(2)
    else:
        return data

def get_int_key(name, required=False):
    if name in DEFAULTS:
        default = DEFAULTS[name]
    else:
        default = None
    if not (data := env.int(name, default=default)) and not required:
        LOGGER.warn("No int key: " + name)
        return None
    elif not data:
        LOGGER.critical("No int key: " + name)
        sys.exit(2)
    else:
        return data
