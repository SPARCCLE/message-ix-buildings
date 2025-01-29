import sys
from argparse import ArgumentParser

import dask
from dask import delayed

from message_ix_buildings.chilled.cities.util.climate import process_climate_data
from message_ix_buildings.chilled.util.common import get_logger
from message_ix_buildings.chilled.util.config import Config  # type: ignore

log = get_logger(__name__)


def parse_arguments(arguments):
    """

    :return:
    """
    parser = ArgumentParser(add_help=True)

    parser.add_argument(
        "-version",
        "--version",
        default="ALPS2023",
        help="Version of inputs to run. Default: ALPS2023.",
    )
    parser.add_argument(
        "-gcm",
        "--gcm",
        default="GFDL-ESM4",
        help="GCM to run. Options: GFDL-ESM4, IPSL-CM6A-LR, MPI-ESM1-2-HR, MRI-ESM2-0, \
            UKESM1-0-LL. Default: GFDL-ESM4.",
    )
    parser.add_argument(
        "-lcz",
        "--lcz",
        default=True,
        help="Run with local climate zones. \
            Default: True.",
    )

    # Parse arguments
    parsed_arguments = parser.parse_known_args(args=arguments)[0]

    return parsed_arguments


def print_arguments(parsed_arguments):
    """
    :param parsed_arguments:

    """

    # Print arguments
    log.info(
        "\n"
        + "---------- Parsed arguments ------------"
        + "\n"
        + "Selected version: "
        + parsed_arguments.version
        + "\n"
        + "Selected GCM: "
        + parsed_arguments.gcm
        + "\n"
        + "Run with local climate zones: "
        + str(parsed_arguments.lcz)
    )


# create climate outputs
# def create_config(parsed_arguments):
#     cfg = Config(
#         vstr=parsed_arguments.version,
#         gcm=parsed_arguments.gcm,
#         rcp=parsed_arguments.rcp,
#     )

#     return cfg


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parsed_args = parse_arguments(arguments=args)

    rcps = ["ssp126", "ssp370", "ssp585", "baseline"]
    climate_zones = parsed_args.lcz
    version = parsed_args.version
    gcm = parsed_args.gcm

    # Run the core functions
    print_arguments(parsed_arguments=parsed_args)
    tasks = []
    for rcp in rcps:
        log.info("Running core functions...")
        config = Config(vstr=version, user="MEAS_UNICC", gcm=gcm, rcp=rcp, heat=0)
        task = delayed(process_climate_data)(config, climate_zones)
        tasks.append(task)

    dask.compute(*tasks, scheduler="processes")

    # log.info("Running core functions...")
    # process_climate_data(cfg, parsed_args.lcz)


if __name__ == "__main__":
    main()
