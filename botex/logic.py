import subprocess

from telebot.types import logger

from botex import config


def nothrow(func) :
    def wrapper(*args, **kwargs) :
        try :
            return func(*args, **kwargs)
        except Exception as e :
            logger.error(f'Exception raised from the logic module:\n{e}')
    return wrapper

def latex2string(latex: str, limit: int | None = None) -> tuple[bool, str] :
    timeout = config['process'].getfloat('timeout')

    if not limit:
        limit = config['message'].getint('length')

    if len(latex) > limit :
        return False, f'Expression too long (maximum length: {limit} characters)'

    try :
        p = subprocess.run(['/usr/local/bin/utftex', '-e', latex],
                           capture_output = True,
                           check = True,
                           timeout = timeout)

        return True, p.stdout.decode('utf8')
    except subprocess.CalledProcessError as e :
        return False, e.stderr.decode('utf8')
    except subprocess.TimeoutExpired as e :
        return False, f'Timeout expired ⏰'

