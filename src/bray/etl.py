import argparse
import bonobo
from bonobo.config import use

from bray.errors import NotImplementedError
from bray.geoclient import Endpoint

class Job:
    def __init__(self, project):
        self._project = project

    def datadir(self):
        return self._project.datadir

    def geoclient(self, endpoint=Endpoint.SEARCH):
        if endpoint == Endpoint.SEARCH:
            return self._project.search_endpoint
        raise NotImplementedError(f'geoclient endpoint {endpoint} is not implemented.')

@use("search")
def search(integration_id, site_name, full_address, borough, status, search):
    #row = {
    #    'integration_id': integration_id,
    #    'site_name': site_name,
    #    'address': full_address,
    #    'borough': borough,
    #    'status': status
    #}
    #print(f'row={row}')
    #return search.call({'input': full_address})
    result = search.call({'input': full_address})
    #print(f'result.__class__=={result.__class__}')
    return {
        'integration_id': integration_id,
        **result
    }


def get_argument_parser(parser=None):
    parser = bonobo.get_argument_parser(parser=parser)

    parser.add_argument('--limit',
                        '-l',
                        type=int,
                        default=None,
                        help='If set, limits the number of processed lines.'
    )
    parser.add_argument('--print',
                        '-p',
                        action='store_true',
                        default=False,
                        help='If set, pretty prints before writing to output file.'
    )

    return parser

def get_graph(graph=None, *, _limit=(), _print=()):
    """
    This function builds the graph that needs to be executed.

    :return: bonobo.Graph
    """
    graph = graph or bonobo.Graph()
    writer = bonobo.CsvWriter('output.csv', fs='fs.out', fields=[
                              'integration_id', 'site_name', 'address', 'borough', 'status'])
    graph.add_chain(
        bonobo.CsvReader('input.csv', fs='fs.in'),
        *_limit,
        #bonobo.Filter(lambda *row: len(row) == 5),
        search,
        bonobo.UnpackItems(0),
        #bonobo.JsonWriter('output.json', fs='fs.out'),
        bonobo.CsvWriter('output.csv', fs='fs.out'),
        *_print,
    )
    return graph

def get_graph_options(options):
    _limit = options.pop("limit", None)
    _print = options.pop("print", False)

    return {"_limit": (bonobo.Limit(_limit),) if _limit else (), "_print": (bonobo.PrettyPrinter(),) if _print else ()}


def get_services(job, **options):
    """
    This function builds the services dictionary, which is a simple dict of names-to-implementation used by bonobo
    for runtime injection.

    It will be used on top of the defaults provided by bonobo (fs, http, ...). You can override those defaults, or just
    let the framework define them. You can also define your own services and naming is up to you.

    :return: dict
    """
    return {
        "fs.in": bonobo.open_fs(job.datadir()),
        "fs.out": bonobo.open_fs(job.datadir()),
        "search": job.geoclient(),
    }
