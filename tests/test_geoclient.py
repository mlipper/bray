import pytest
import json
# import os

from . import getfile
from bray.geoclient import (
    HTTPEndpoint,
    Geoclient,
    # Search,
    SearchDecoder
)

SEARCH_FILES = {
    'ok_exact_match': getfile('search-ok-exact-match.json'),
    'ok_mixed_matches': getfile('search-ok-mixed-matches.json'),
    'ok_possible_matches': getfile('search-ok-possible-matches.json'),
    'rejected_no_rejects': getfile('search-rejected-no-rejects.json'),
    'rejected_with_rejects': getfile('search-rejected-with-rejects.json')
}


#
# The 'decoded_search' marker is registered in <project_root>/pytest.ini.
# This file must updated if this fixture function is renamed.
#
@pytest.fixture
def decoded_search(request):
    """Yields the result of deserializing a JSON response from the search endpoint.
    """
    marker_name = 'decoded_search'
    marker = request.node.get_closest_marker(marker_name)
    if marker is None:
        raise pytest.UsageError(f'Call to request.node.get_closest_marker("{marker_name}") returned None.')

    label = marker.args[0]
    with open(SEARCH_FILES[label], 'r') as f:
        yield json.load(f, cls=SearchDecoder)


class TestSearchDecoder:
    @pytest.mark.decoded_search('ok_exact_match')
    def test_transform_ok_exact_match(self, decoded_search):
        assert decoded_search[SearchDecoder.NEW_RESULT_STATUS] == 'EXACT_MATCH'
        assert decoded_search[SearchDecoder.SUMMARY] == '1 EXACT_MATCH, 0 POSSIBLE_MATCH, 0 REJECTED'

    @pytest.mark.decoded_search('ok_possible_matches')
    def test_transform_ok_possible_matches(self, decoded_search):
        assert decoded_search[SearchDecoder.NEW_RESULT_STATUS] == 'POSSIBLE_MATCH'
        assert decoded_search[SearchDecoder.SUMMARY] == '0 EXACT_MATCH, 3 POSSIBLE_MATCH, 2 REJECTED'

    @pytest.mark.decoded_search('rejected_with_rejects')
    def test_transform_rejected_with_rejects(self, decoded_search):
        assert decoded_search[SearchDecoder.NEW_RESULT_STATUS] == 'REJECTED'
        assert decoded_search[SearchDecoder.SUMMARY] == '0 EXACT_MATCH, 0 POSSIBLE_MATCH, 1 REJECTED'

    @pytest.mark.decoded_search('rejected_no_rejects')
    def test_transform_rejected_no_rejects(self, decoded_search):
        assert decoded_search[SearchDecoder.RESULT_STATUS] == 'REJECTED'
        assert SearchDecoder.NEW_RESULT_STATUS not in decoded_search
        assert SearchDecoder.SUMMARY not in decoded_search

    #
    # This test does not use the search_response fixture because
    # the result_and_stats method is tested in isolation.
    #
    def test_result_and_stats(self):
        # data = None
        with open(SEARCH_FILES['ok_mixed_matches'], 'r') as f:
            data = json.load(f)

        results_fixture = data[SearchDecoder.RESULTS]
        decoder = SearchDecoder()
        actual = decoder.result_and_stats(data)
        assert isinstance(actual, tuple)
        assert results_fixture[0] == actual[0]
        assert decoder.new_stats_map(exact=0, possible=2, rejected=5) == actual[1]


class MockHTTPEndpoint:

    @staticmethod
    def get_json(uri, query, decoder=None):
        return {
            'uri_arg': uri,
            'query_arg': query,
            'decoder_arg': decoder
        }


@pytest.fixture
def mock_json_obj(monkeypatch):
    """Mocks bray.geoclient.HTTPEndpoint.get_json(...) method."""

    def mock_http_get_json(*args, **kwargs):
        return MockHTTPEndpoint().get_json(args[1], args[2], kwargs['decoder'])

    monkeypatch.setattr(HTTPEndpoint, "get_json", mock_http_get_json)


class MockDecoder:
    pass


class EndpointArgs:
    def __init__(self):
        self.uri = 'https://snafubar'
        self.query = {'app_id': 'foobar', 'app_key': 'xxxx'}
        self.runtime_args = {'houseNumber': '2860', 'street': 'broadway', 'borough': 'manhattan'}
        self.expected_query = {
            **self.runtime_args,
            **self.query
        }


@pytest.fixture
def endpoint_args():
    return EndpointArgs()


class TestGeoclient:

    def test_call_no_decoder(self, mock_json_obj, endpoint_args):
        ea = endpoint_args
        geoclient = Geoclient('no-decoder', ea.uri, ea.query)
        result = geoclient(ea.runtime_args)
        assert result['uri_arg'] == ea.uri
        assert result['query_arg'] == ea.expected_query
        assert result['decoder_arg'] is None

    def test_call_with_decoder(self, mock_json_obj, endpoint_args):
        ea = endpoint_args
        geoclient = Geoclient('with-decoder', ea.uri, ea.query, decoder=MockDecoder)
        result = geoclient(ea.runtime_args)
        assert result['uri_arg'] == ea.uri
        assert result['query_arg'] == ea.expected_query
        assert result['decoder_arg'] == MockDecoder
