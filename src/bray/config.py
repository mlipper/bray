from collections import namedtuple
import functools
import json
from json import JSONDecoder
import logging
from pathlib import (
    os,
    Path
)

from . import errors

logger = logging.getLogger(__name__)


class FilterSet:

    TokenValue = namedtuple("TokenValue", "token value default_value")

    def __init__(self, tokenvalues={}, tokendefaults={}, default_default=None):
        self.filters = []
        for k, v in tokenvalues.items():
            tk, val = k, v
            default_value = default_default
            if tk in tokendefaults:
                default_value = tokendefaults[tk]
            token = self.TokenValue(tk, val, default_value)
            logger.debug(f'Created token {token}')
            self.filters.append(token)

    def getfilters(self):
        return self.filters

def replace_tokens(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            print(f'[{k}] {v!r}')
            replace_tokens(v)
    else:
        val = obj
        if isinstance(val, str):
            val = f'::{val}'
        print(f'    ----{val!r}')
        return val

def token_context(func):
    @functools.wraps(func)
    def wrapper_token_context(*args, **kwargs):
        wrapper_token_context.num_calls += 1
        print(f'args={args}')
        print(f'kwargs={kwargs}')
        print(f"Call {wrapper_token_context.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_token_context.num_calls = 0
    return wrapper_token_context

class ConfigDecoder(JSONDecoder):

    def __init__(self):
        JSONDecoder.__init__(self, object_hook=self.transform)
        self._token_filter = os.environ

    @token_context
    def transform(self, data):
        new_data = { **data }
        for k, v in data.items():
            if isinstance(v, str) and v.startswith('<env>:'):
                envvar = v.lstrip('<env>:')
                new_data[k] = self._token_filter.get(envvar, None)
                logger.debug(f'Replaced original value "{v}" of key "{k}" with new value "{new_data[k]}".')
        return new_data

class Project:
    CONFIG_FILE = 'config.json'

    def __init__(self, name, config_file=CONFIG_FILE, decoder=False):
        if name is None:
            raise errors.ConfigurationError("Project name argument is required.")
        self._name = name
        f = Path(config_file)
        if not f.is_file():
            raise errors.ConfigurationError(f'Could not find file {config_file}')

        self._config_file = f
        self._decoder = ConfigDecoder if decoder else None

    @property
    def name(self):
        return self._name

    @property
    def config_file(self):
        return self._config_file

    def load(self):
        # self-encapsulate by accessing config file using property
        with self.config_file.open() as f:
            if self._decoder is not None:
                return json.load(f, cls=self._decoder)
            else:
                return json.load(f)

    def __repr__(self):
        return f'{self.__class__!r}({self._path!r}, {self._path!r}, {self._config_file!r})'
