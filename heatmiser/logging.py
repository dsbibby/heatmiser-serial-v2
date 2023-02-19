from datetime import datetime


log_levels = ['debug1', 'debug', 'info', 'warn', 'error']
LOG_LEVEL = 1


def log(level, message, *args):
    try:
        log_level_index = log_levels.index(level.lower())
    except ValueError:
        return

    if log_level_index >= LOG_LEVEL:
        d = datetime.now()
        print(d, f"[{level.upper()}]", message, *args)
