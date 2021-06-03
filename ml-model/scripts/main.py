"""Control logic for running skyscan data and model functionality."""

import argparse
import configparser
import logging
import os
import sys

from customvox51 import (
    add_faa_data_to_voxel51_dataset,
    add_sample_images_to_voxel51_dataset,
    build_image_list,
    create_voxel51_dataset,
)

# pylint: disable=C0330, W0621


def read_config(config_file=os.path.join("config", "config.ini")):
    """Read in config file values.

    Use python standard library configparser module
    to read in user-defined values. This enables configurability.

    For more info on configparser, see here:
    https://docs.python.org/3/library/configparser.html#module-configparser

    Args:
        config file (str) - name of config file. Default is config.ini

    Returns:
        config - a config object similar to a dict
    """

    logging.info("Starting to read config file.")
    config = configparser.ConfigParser()
    config.read(config_file)
    logging.info("Finished reading config file.")
    return config


def parse_command_line_arguments():
    """Parse command line arguments with argparse."""
    parser = argparse.ArgumentParser(
        description="Run skyscan data and model scripts.",
        epilog="For help with this program, contact John Speed at jmeyers@iqt.org.",
    )
    parser.add_argument(
        "--prep",
        default=False,  # default value is False
        action="store_true",
        help="Prepare voxel51 dataset.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line_arguments()
    config = read_config()

    # check if user selected data preparation stage
    if args.prep:
        # check that config file contains both dataset name and
        # image_directory
        if (
            config["file_names"]["dataset_name"]
            and config["file_locations"]["image_directory"]
        ):
            logging.info("Entering 'prepare data' route.")
            image_list = build_image_list(config["file_locations"]["image_directory"])
            dataset = create_voxel51_dataset(config["file_names"]["dataset_name"])
            modified_dataset = add_sample_images_to_voxel51_dataset(image_list, dataset)
            dataset_with_faa_data = add_faa_data_to_voxel51_dataset(
                config["file_names"]["dataset_name"],
                "../notebooks/aircraftDatabase.csv",
            )
            logging.info("Exiting 'prepare data' route.")
        # exit if config file does not contain image directory or dataset name.
        else:
            logging.info(
                "Missing config file value image for image directory or dataset_name."
            )
            sys.exit(1)  # exit program
