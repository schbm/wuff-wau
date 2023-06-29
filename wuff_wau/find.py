import logging
from sys import exit

from wuff_wau.common import print_rich
from wuff_wau.data import validate_dog_dict
from wuff_wau.common import print_rich_table
from wuff_wau.data import filter_data_by_year


# find dogs with a given name and sample year
# input: data, sample_year, dogname
# data: list of dog data
# sample_year: year to sample data from (int)
# dogname: name of the dog to find (str)
# prints dog information to the console
# exits on error
def action_find(data, sample_year, dogname):
    logging.debug(f"finding dogs with name {dogname} from sample year {sample_year}")

    if type(data) != list:
        logging.error("data is not a list")
        exit(1)
    if type(sample_year) != int:
        logging.error("sample year is not an integer")
        exit(1)
    if type(dogname) != str:
        logging.error("dog name is not a string")
        exit(1)

    # filter data for sample year
    data = filter_data_by_year(data, sample_year)
    if len(data) == 0:
        logging.error(f"no data found for sample year {sample_year}")
        return

    validate_dog_dict(data)

    # find dogs with given name
    results = list()
    for data_sample in data:
        if data_sample["HundenameText"].lower() == dogname.lower():
            results.append(data_sample)

    # print results
    col_headers = ("Nr.", "Name", "Birth year", "sex")
    rows = list()
    for i, result in enumerate(results):
        rows.append(
            (
                str(i),
                (result["HundenameText"]),
                (result["GebDatHundJahr"]),
                (result["SexHundLang"]),
            )
        )

    if len(rows) == 0:
        print_rich(f"No dogs found with name {dogname} :thumbs_down:")
    else:
        print_rich_table(col_headers, rows)
