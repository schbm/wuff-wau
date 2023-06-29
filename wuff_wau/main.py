import logging
import argparse
from sys import exit
from os import getcwd

from wuff_wau.data import get_data
from wuff_wau.data import parse_csv
from wuff_wau.find import action_find
from wuff_wau.stats import action_stats
from wuff_wau.data import get_mime_type
from wuff_wau.common import setup_logger
from wuff_wau.create import action_create
from wuff_wau.data import find_newest_sample_year


# check if the sample year is valid
# exits on error
def check_optional_args(args):
    if args.year < 0:
        logging.error("Sample year option cannot be negative")
        exit(1)


# setupt the parser
# returns the parser
def setup_parser():
    # create the top-level parser
    parser = argparse.ArgumentParser(
        prog="WUFF-WAU",
        description="Various operations based on the"
        + " registered dogs in the city of Zurich",
        epilog="thank you for using wuff-wau",
        add_help=True,
    )
    sub_parser = parser.add_subparsers(
        title="actions",
        help="for more help: command --help",
        description="avilable positional arguments",
    )
    parser.set_defaults(func_name="action_none")

    # create the parser for the "stats" command
    stats_parser = sub_parser.add_parser("stats", help="shows stats about dogs")
    stats_parser.add_argument("stats", action="store_true", help="shows stats")
    stats_parser.set_defaults(func_name="action_stats")
    # create the parser for the "find" command
    find_parser = sub_parser.add_parser("find", help="find dogs with name")
    find_parser.add_argument(
        "find",
        action="store",
        metavar="dogname",
        type=str,
        help="name of the dog to find",
    )
    find_parser.set_defaults(func_name="action_find")
    # create the parser for the "create" command
    create_parser = sub_parser.add_parser(
        "create",
        help="gets a random dog image and assembles the file name randomly"
        + " from a name and birthdate from sample data",
    )
    create_parser.add_argument(
        "create", action="store_true", help="generate a random dog"
    )
    create_parser.add_argument(
        "-o",
        "--output-dir",
        action="store",
        type=str,
        default=getcwd(),
        help="full path to the destination directory of the resulting image",
    )
    create_parser.set_defaults(func_name="action_create")

    # add optional parameters
    parser.add_argument(
        "-y",
        "--year",
        action="store",
        default="0",
        type=int,
        help="sample year of the data",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="enables debug output"
    )
    return parser


# main function
# parses the arguments and executes the action
# gets data from the url and parses it
# executes the action
def main():
    parser = setup_parser()
    arguments = parser.parse_args()

    # enable logging if debug is enabled
    setup_logger(arguments.debug)
    # validate input of optional arguments
    # positional arguments are already checked by argparse
    check_optional_args(arguments)

    # get the parsed data
    url = "https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv"
    # check mime type
    if not get_mime_type(url) == "text/csv":
        logging.error("url to sample data returns wrong mime type")
        exit(1)
    # get the decoded data
    data = get_data(url)
    # parse csv text data to list of dict elements
    data = parse_csv(data)

    # check if the sample year is set to the default value
    # if yes find out the most current sample year
    if arguments.year == 0:
        logging.debug("no sample year argument passed")
        arguments.year = find_newest_sample_year(data)

    # execute action according to used positional argument
    # data is filtered by the action functions
    # image data is processed by the action functions
    match arguments.func_name:
        case "action_none":
            parser.print_help()
        case "action_stats":
            action_stats(data, arguments.year)
        case "action_find":
            action_find(data, arguments.year, arguments.find)
        case "action_create":
            action_create(data, arguments.year, arguments.output_dir)


# entry point
if __name__ == "__main__":
    main()
