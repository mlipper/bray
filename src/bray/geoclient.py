import json

from dataclasses import dataclass
from json import JSONDecoder
from urllib import parse, request

from bray import logger


# FIXME replace with dependency-injection. E.g., function, etc.
SERVICE_NAMESPACE = "gc"
SEARCH_SERVICE_ID = f"{SERVICE_NAMESPACE}.search"


class SearchDecoder(JSONDecoder):

    NEW_RESULT_STATUS = 'resultStatus'
    RESPONSE = 'response'
    RESULTS = 'results'
    RESULT_STATUS = 'status'
    SUMMARY = 'summary'

    def __init__(self):
        JSONDecoder.__init__(self, object_hook=self.transform)
        self.call_count = 0

    def debug_data(self, data):
        logger.debug('----------------')
        self.call_count += 1
        logger.debug(f'   call#: {self.call_count}')
        logger.debug(f'   class: {type(data)}')
        logger.debug(f'  length: {len(data)}')
        ident = data['id'] if 'id' in data else 'null'
        logger.debug(f'      id: {ident}')
        results = len(data['results']) if 'results' in data else 'null'
        logger.debug(f' results: {results}')
        request = data['request'] if 'request' in data else 'null'
        logger.debug(f' request: {request}')
        response = len(data['response']) if 'response' in data else 'null'
        logger.debug(f'response: {response}')

    def transform(self, data):
        # Note-to-self: this method is called recursively by json.load
        # starting from the innermost to the outermost nested dict and
        # (I think) list references
        if SearchDecoder.RESULTS in data and len(data[SearchDecoder.RESULTS]) > 0:
            first_result, stats = self.result_and_stats(data)
            # Summarize results and add to data map
            data[SearchDecoder.SUMMARY] = self.summarize(stats)
            # Remove all 'RESULTS' since we have a reference to the first
            # and will be updating the top-level dict with its contents
            data.pop(SearchDecoder.RESULTS)
            # Remove 'RESULT_STATUS' item from 'first_result' dict
            # (because otherwise it will overwrite the outer 'status'
            # key) and use a different key name to populate outer dict.
            data[SearchDecoder.NEW_RESULT_STATUS] = first_result.pop(
                SearchDecoder.RESULT_STATUS)
            # Un-nest 'response' and merge dict value to top level
            data.update(first_result.pop(SearchDecoder.RESPONSE))
            # Add 'first_result' dict itself
            data.update(first_result)
        return data

    def result_and_stats(self, data):
        stats = self.new_stats_map()
        if SearchDecoder.RESULTS not in data or data[SearchDecoder.RESULTS] is None:
            return (None, stats)
        all_results = data[SearchDecoder.RESULTS]
        if(len(all_results) == 0):
            return (None, stats)
        result = all_results[0]
        for r in all_results:
            result_status = r[SearchDecoder.RESULT_STATUS]
            stats[result_status] += 1
        return (result, stats)

    def new_stats_map(self, exact=0, possible=0, rejected=0):
        stats = dict()
        stats['EXACT_MATCH'] = exact
        stats['POSSIBLE_MATCH'] = possible
        stats['REJECTED'] = rejected
        return stats

    def summarize(self, stats):
        return f"{stats['EXACT_MATCH']} EXACT_MATCH, {stats['POSSIBLE_MATCH']} POSSIBLE_MATCH, {stats['REJECTED']} REJECTED"


@dataclass
class HTTPEndpoint:
    """Encapsulates use of urllib.parse and urllib.request in order to
       make it easier to mock URL encoding and HTTP calls issued by
       these external libraries.
    """
    # Uncomment to make this class Callable
    # def __call__(self, uri, query, decoder=None):
    #     return self.get_json(uri, query, decoder)

    def get_json(self, uri, query, decoder=None):
        encoded_url = f'{uri}?{parse.urlencode(query)}'
        with request.urlopen(encoded_url) as f:
            stream = f.read().decode('utf-8')
        if decoder is None:
            return json.loads(stream)
        return json.loads(stream, cls=decoder)


class Geoclient:
    """
    Geocodes locations with provided endpoint configurations.
    """
    def __init__(self, id, uri, query, decoder=None):
        self._id = id
        self._uri = uri
        self._query = query
        self._decoder = decoder
        self.http_endpoint = HTTPEndpoint()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        self._uri = uri

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    @property
    def decoder(self):
        return self._decoder

    @decoder.setter
    def decoder(self, decoder):
        self._decoder = decoder

    def __call__(self, endpoint_args):
        qry = {
            **endpoint_args,
            **self.query
        }
        return self.http_endpoint.get_json(self.uri, qry, decoder=self.decoder)

    def __repr__(self):
        return f'{self.__class__!r}({self._id!r}, {self._uri!r}, {self._query!r}, {self._decoder!r})'


class Search(Geoclient):
    def __init__(self, id, uri, query, decoder=SearchDecoder):
        super().__init__(id, uri, query, decoder)


def register_services(settings, registry):
    if settings.geoclient is not None:
        base_settings = settings.geoclient
        if base_settings.search is not None:
            search_settings = base_settings.search
            search_id = SEARCH_SERVICE_ID
            registry[search_id] = Search(search_id, search_settings.uri, search_settings.query.to_dict())
