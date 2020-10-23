from collections import namedtuple
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import os, Path
import json
import pytest
import re

from bray import config

Expected = namedtuple("Expected", "expected_token expected_value expected_default")

tokenvalues = {'first': 'val1', 'second': None, 'third': 'val3'}
default_default = 'double default value'
token_data = [
    #1 - Arguments
    (tokenvalues, {'first': 'defaultval1', 'second': 'defaultval2'}, default_default,
        [ # Expected results #1
        #1.1
        Expected('first', 'val1', 'defaultval1'),
        #1.2
        Expected('second', 'defaultval2', 'defaultval2'),
        #1.3
        Expected('third', 'val3', 'defaultval3'),
        ]),
    #2 - Arguments
    (tokenvalues, {'random': None}, default_default,
        [  # Expected results #2
        #2.1
        Expected('first', 'val1', default_default),
        #2.2
        Expected('second', default_default, default_default),
        #2.3
        Expected('third', 'val3', default_default),
    ])
]
token_keyword_data = [
    #1 - Keyword arguments
    ({'tokenvalues': tokenvalues, 'tokendefaults': {'first': 'defaultval1', 'second': 'defaultval2'}, 'default_default': default_default},
        [  # Expected kw results #1
        #1.1
        Expected('first', 'val1', 'defaultval1'),
        #1.2
        Expected('second', 'defaultval2', 'defaultval2'),
        #1.3
        Expected('third', 'val3', 'defaultval3'),
    ]),
    #2 - Keyword arguments
    ({'tokenvalues': tokenvalues, 'default_default': default_default},
        [  # Expected kw results #2
        #2.1
        Expected('first', 'val1', default_default),
        #2.2
        Expected('second', default_default, default_default),
        #2.3
        Expected('third', 'val3', default_default),
    ])
]

@pytest.mark.parametrize('tvalues,tdefaults,ddefaults,expected', token_data)
def test_filterset_positional_args(tvalues, tdefaults, ddefaults, expected):
    filterset = config.FilterSet(tvalues, tdefaults, ddefaults)
    actual = filterset.getfilters()
    assert len(actual) == len(expected)

@pytest.mark.parametrize('kwargs,expected', token_keyword_data)
def test_filterset_keyword_args(kwargs, expected):
    filterset = config.FilterSet(**kwargs)
    actual = filterset.getfilters()
    assert len(actual) == len(expected)

def test_project_load_no_decode(config_json):
    project = config.Project('example', config_json)
    assert 'example' == project.name
    config_obj = project.load()
    assert config_obj['name'] == 'example-etl'

def test_project_load_decode(config_json, mock_env_app_id, mock_env_app_key):
    project = config.Project('example', config_json, decoder=True)
    assert 'example' == project.name
    config_obj = project.load()
    assert config_obj['name'] == 'example-etl'
    assert config_obj['geoclient']['query']['app_id'] == mock_env_app_id
    assert config_obj['geoclient']['query']['app_key'] == mock_env_app_key

def test_how_parser_works(example_config_ini):
    override = { 'all.query1': 'OVERRIDDEN', 'APP_KEY': 'REPLACED APP KEY'}
    svparser = config.StringValueParser(override)
    cfg = ConfigParser(interpolation=ExtendedInterpolation(), converters={'tokenval': svparser})
    cfg.read(example_config_ini)
    for section in cfg.sections():
        print(section)
        print('-' * len(section))
        for k in cfg[section]:
            #strval = cfg.get(section, k, vars=override)
            #val = sparser(strval)
            strval = cfg.gettokenval(section, k, vars=override)
            val = strval
            print(f'- {k} = {val}')
        print()

# [i.strip() for i in re.split(r'\n|[,]', 'a, b , c, ', re.DOTALL) if i != ' ']
# [i.strip() for i in re.split(r'\n|[,]', 'a, b , c, ', re.DOTALL) if len(i.strip()) >0]
# re.sub(r'\n',',',s)
