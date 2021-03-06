from nose.tools import raises

from . import get_fixture
import yamale as sch
from .. import validators as val

types = {
    'schema': 'types.yaml',
    'bad': 'types_bad_data.yaml',
    'good': 'types_good_data.yaml'
}

nested = {
    'schema': 'nested.yaml',
    'bad': 'nested_bad_data.yaml',
    'good': 'nested_good_data.yaml'
}

custom = {
    'schema': 'custom_types.yaml',
    'bad': 'custom_types_bad.yaml',
    'good': 'custom_types_good.yaml'
}

keywords = {
    'schema': 'keywords.yaml',
    'bad': 'keywords_bad.yaml',
    'good': 'keywords_good.yaml'
}

lists = {
    'schema': 'lists.yaml',
    'bad': 'lists_bad.yaml',
    'good': 'lists_good.yaml'
}

test_data = [types, nested, custom, keywords, lists]

for d in test_data:
    for key in d.keys():
        if key == 'schema':
            d[key] = sch.make_schema(get_fixture(d[key]))
        else:
            d[key] = sch.make_data(get_fixture(d[key]))


def test_tests():
    ''' Make sure the test runner is working.'''
    assert 1 + 1 == 2


def test_flat_make_schema():
    assert isinstance(types['schema']['string'], val.String)


def test_nested_schema():
    nested_schema = nested['schema']
    assert isinstance(nested_schema['string'], val.String)
    assert isinstance(nested_schema.dict['list'], (list, tuple))
    assert isinstance(nested_schema['list.0'], val.String)


def test_good():
    for data_map in test_data:
        yield good_gen, data_map


def good_gen(data_map):
    sch.validate(data_map['schema'], data_map['good'])


@raises(ValueError)
def test_bad_validate():
    sch.validate(types['schema'], types['bad'])


@raises(ValueError)
def test_bad_nested():
    sch.validate(nested['schema'], nested['bad'])


@raises(ValueError)
def test_bad_custom():
    assert sch.validate(custom['schema'], custom['bad'])


@raises(ValueError)
def test_bad_lists():
    assert sch.validate(lists['schema'], lists['bad'])


@raises(ValueError)
def test_bad_keywords():
    assert sch.validate(keywords['schema'], keywords['bad'])
