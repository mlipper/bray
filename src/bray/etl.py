import logging

from dataclasses import dataclass, field
from typing import Any

import bonobo

from bonobo.config import use, use_raw_input

from bray.errors import ConfigurationError
from bray.geoclient import SEARCH_SERVICE_ID, Geoclient

logger = logging.getLogger(__name__)

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


@use_raw_input
def log_raw(args):
    logger.info("args==%s", args)
    # integration_id, __, full_address, __, __ = args
    # query = {"input": full_address}
    # logger.info("[QUERY] %s", str(query))
    # result = search(query)
    # logger.info("[RESULT] %s", result)
    # return {"id": integration_id, **result}


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


def get_argument_parser(argparser):
    """Augments the given ArgumentParser for use with the Bonobo ETL framework."""
    return bonobo.get_argument_parser(parser=argparser)


def get_debug_graph(job, graph=None, *, _limit=(), _print=()):
    """Builds a simple graph for debugging."""
    graph = graph or bonobo.Graph()
    graph.add_chain(
        bonobo.CsvReader(job.input_file, fs=FS_IN_SERVICE_ID),
        *_limit,
        # bonobo.Filter(lambda *row: len(row) == 5),
        # bonobo.JsonWriter('output.json', fs='fs.out'),
        # bonobo.CsvWriter(job.output_file, fs=FS_OUT_SERVICE_ID,
        #   fields=['integration_id', 'site_name', 'address', 'borough', 'status']),
        log_raw,
        *_print,
    )
    return graph


def get_graph(job, graph=None, *, _limit=(), _print=()):
    """Builds the execution graph."""
    graph = graph or bonobo.Graph()
    graph.add_chain(
        bonobo.CsvReader(job.input_file,
                         fs=FS_IN_SERVICE_ID,
                         fields=['integration_id', 'site_name', 'address', 'borough', 'status'],
                         skip=1),
        *_limit,
        search,
        bonobo.UnpackItems(0),
        bonobo.CsvWriter(job.output_file, fs=FS_OUT_SERVICE_ID),
        *_print,
    )
    return graph


def get_graph_options(options):
    logger.debug("Unpacking command line options %s.", options)
    _limit = options.pop("limit", None)
    _print = options.pop("print", False)
    graph_options = {
        "_limit": (bonobo.Limit(_limit),) if _limit else (),
        "_print": (bonobo.PrettyPrinter(),) if _print else ()}
    logger.debug("Created graph options %s.", graph_options)
    return graph_options


# TODO Replace with Etl class to avoid passing parser around?
def run(job, argparser):
    parser = get_argument_parser(argparser)
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(job, **get_graph_options(options)),
            services=get_services(job)
        )


def get_services(job):
    """Return the names-to-services dict Bonobo uses for runtime injection."""
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
