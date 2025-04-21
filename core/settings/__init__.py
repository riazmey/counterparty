
from main import *

try:
    from local import * # type: ignore
except ImportError:
    from environ import *

print('Debug view environments vars:')
if DEBUG:
    print(f'    SECRET_KEY: {SECRET_KEY}')
    print(f'    DEBUG: {DEBUG}')
    print(f'    ALLOWED_HOSTS: {ALLOWED_HOSTS}')
    print(f'    DATABASES: {DATABASES}')
else:
    print(f'    DEBUG: {DEBUG}')