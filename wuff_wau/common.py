import rich
import logging
from sys import exit

from rich.table import Table
from rich.console import Console
from rich.logging import RichHandler


# enables debug logging if arg set
# to true uses handler of rich library
# if it is not set logging is only used
# for error messages
def setup_logger(enabled=False):
    if enabled:
        logging.basicConfig(
            level="DEBUG",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler()],
        )
    else:
        logging.basicConfig(
            level="ERROR",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler()],
        )


# format a string and print it to the console
# using the rich library
# if the message is not a string it will be logged
# as an error and printed with the print function
def print_rich(message):
    if not isinstance(message, str):
        logging.error("message is not a string")
    try:
        rich.print(f"[magenta]{message}[/magenta]")
    except (rich.console.errors):
        logging.error("rich error printing to console")
        print(message)


# formats header columns and row data to a
# table and prints it to the console
def print_rich_table(col_headers, rows):
    logging.debug("printing table with rich")
    logging.debug("col is of type: " + str(type(col_headers)))
    logging.debug("rows is of type: " + str(type(rows)))

    # if it both arent strings
    # check if rows are of the same length
    # check if col_headers and rows match
    if not isinstance(col_headers, str) and not isinstance(rows, str):
        for row in rows:
            for row_compare in rows:
                if len(row) != len(row_compare):
                    logging.error("rows do not match")
                    exit(1)
        if len(col_headers) != len(rows[0]):
            logging.error("col_headers and rows do not match")
            exit(1)

    table = Table(show_header=True, header_style="bold", expand=True)

    # check if single col table or multiple
    if not isinstance(col_headers, str):
        for col_header in col_headers:
            table.add_column(col_header, style="dim", width=12)
    else:
        table.add_column(col_headers)
    # check if single row table or multiple
    if not isinstance(rows, str):
        for row in rows:
            table.add_row(*row)
    else:
        table.add_row(*rows)

    try:
        Console().print(table)
    except rich.console.errors:
        logging.error("error printing table with rich")
        print(col_headers)
        print(rows)
