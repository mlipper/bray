from dataclasses import dataclass, field
from typing import Any
import bonobo
from bonobo.config import use, use_raw_input

from bray import logger
from bray.errors import ConfigurationError
from bray.geoclient import SEARCH_SERVICE_ID, Geoclient

# FIXME replace with dependency-injection. E.g., function, etc.
SERVICE_NAMESPACE = "fs"
FS_IN_SERVICE_ID = f"{SERVICE_NAMESPACE}.in"
FS_OUT_SERVICE_ID = f"{SERVICE_NAMESPACE}.out"
INPUT_FILE_SERVICE_ID = f"{SERVICE_NAMESPACE}.infile"
OUTPUT_FILE_SERVICE_ID = f"{SERVICE_NAMESPACE}.outfile"
DATA_DIR_SERVICE_ID = f"{SERVICE_NAMESPACE}.data_dir"
JOB_ID = f"{SERVICE_NAMESPACE}.job"


@dataclass
class Job:
    """Class for encapsulating ETL job configuration data.
    """
    input_file: Any  # Usually str or Path
    output_file: Any  # Usually str or Path
    data_dir: Any  # Usually str or Path
    search: Geoclient = field(repr=False)


@use("search")
@use_raw_input
def duh(args, search):
    logger.info("[DUH] %s", str(args))
    logger.info("[ARGS] %s", args)
    integration_id, __, full_address, __, __ = args
    query = {"input": full_address}
    logger.info("[QUERY] %s", str(query))
    result = search.call(query)
    logger.info("[RESULT] %s", result)
    return {"id": integration_id, **result}


@use("search")
def search(integration_id, site_name, full_address, Borough, Status, search):
    """Call the geoclient search endpoint.

    :param integration_id: Caller-provided identifier
    :type integration_id: str
    :param site_name: Pass-through value (not used)
    :type site_name: str
    :param full_address: Location string to be passed as the input parameter to the geoclient search endpoint
    :type full_address: str
    :param borough: Pass-through value (not used)
    :type borough: str
    :param status: Pass-through value (not used)
    :type status: str
    :param search: Function which invokes the geoclient remote search endpoint (injected by bonobo framework)
    :type search: bray.geoclient.Search
    :return: Dictionary-like object containing the integration_id argument and all geocoding response attributes as key-value pairs.
    :rtype: dict

        row = {
            'integration_id': integration_id,
            'attr1': 'value1',
            'attr2': 'value2',
            ...
        }

    """
    # logger.info("etl.search called with arguments: '%s' '%s' '%s' '%s' '%s' '%s'",
    #             integration_id, site_name, full_address, borough, status, search)
    result = search({'input': full_address})
    return {
        'integration_id': integration_id,
        **result
    }


def get_argument_parser(parser=None):
    parser = bonobo.get_argument_parser(parser=parser)

    parser.add_argument("--limit", "-l", type=int, default=None, help="If set, limits the number of processed lines.")
    parser.add_argument(
        "--print", "-p", action="store_true", default=False, help="If set, pretty prints before writing to output file."
    )

    return parser


def get_graph(job, graph=None, *, _limit=(), _print=()):
    """
    This function builds the graph that needs to be executed.

    :return: bonobo.Graph
    """
    graph = graph or bonobo.Graph()
    # writer = bonobo.CsvWriter('output.csv', fs='fs.out', fields=[
    #                           'integration_id', 'site_name', 'address', 'borough', 'status'])
    graph.add_chain(
        bonobo.CsvReader(job.input_file,
                         fs=FS_IN_SERVICE_ID,
                         fields=['integration_id', 'site_name', 'address', 'borough', 'status']),
        # *_limit,
        # bonobo.Filter(lambda *row: len(row) == 5),
        search,
        # duh,
        bonobo.UnpackItems(0),
        # bonobo.JsonWriter('output.json', fs='fs.out'),
        bonobo.CsvWriter(job.output_file, fs=FS_OUT_SERVICE_ID),
        *_print,
    )
    return graph


def get_graph_options(options):
    _limit = options.pop("limit", None)
    _print = options.pop("print", False)

    return {"_limit": (bonobo.Limit(_limit),) if _limit else (), "_print": (bonobo.PrettyPrinter(),) if _print else ()}


def run(job):
    parser = get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(job, **get_graph_options(options)), services=get_services(job)
        )


def get_services(job):
    """
    This function builds the services dictionary, which is a simple dict of names-to-implementation used by bonobo
    for runtime injection.

    It will be used on top of the defaults provided by bonobo (fs, http, ...). You can override those defaults, or just
    let the framework define them. You can also define your own services and naming is up to you.

    :return: dict
    """
    return {
        FS_IN_SERVICE_ID: bonobo.open_fs(job.data_dir),
        FS_OUT_SERVICE_ID: bonobo.open_fs(job.data_dir),
        "search": job.search,
    }


def register_services(settings, registry):
    # FIXME replace hard-coded id's with methods on Registry class
    search = registry[SEARCH_SERVICE_ID]
    if search is None:
        raise ConfigurationError("search cannot be None.")

    if settings.default is None:
        raise ConfigurationError("settings.default cannot be None.")

    base_settings = settings.default

    if base_settings.input_file is None:
        raise ConfigurationError("input_file cannot be None.")

    if base_settings.output_file is None:
        raise ConfigurationError("output_file cannot be None.")

    if base_settings.data_dir is None:
        raise ConfigurationError("data_dir cannot be None.")

    input_file = base_settings.input_file
    registry[INPUT_FILE_SERVICE_ID] = input_file

    output_file = base_settings.output_file
    registry[OUTPUT_FILE_SERVICE_ID] = output_file

    data_dir = base_settings.data_dir
    registry[DATA_DIR_SERVICE_ID] = data_dir

    registry[JOB_ID] = Job(input_file, output_file, data_dir, search)
