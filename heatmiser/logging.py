import datetime

log_levels = ['debug1', 'debug', 'info', 'warn', 'error']
LOG_LEVEL = 2

def log(level, message, *args):
    try:
        l = log_levels.index(level.lower())
    except ValueError:
        return
    
    if l >= LOG_LEVEL:
        d = datetime.datetime.now()
        print(d, f"[{level.upper()}]", message, *args)