import os
from .local import config as local_config
from .staging import config as stag_config

env = os.environ.get('PYTHON_ENV', 'local')
# mongodb_user = os.environ['mongodb_user']
# mongodb_pass = os.environ['mongodb_pass']

__all__ = ['config']

if env == 'local':
    config = local_config
elif env == 'staging':
    config = stag_config
    
