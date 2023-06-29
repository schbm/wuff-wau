import logging
from sys import exit
from collections import Counter
from wuff_wau.common import print_rich
from wuff_wau.data import validate_dog_dict
from wuff_wau.common import print_rich_table
from wuff_wau.data import filter_data_by_year


# print statistics about dogs with a given name and sample year
# input: data, sample_year
# data: list of dog data (list)
# sample_year: year to sample data from (int)
# prints dog information to the console
# exits on error
def action_stats(data, sample_year):
    logging.debug(f"generating stats for sample year {sample_year}")

    if type(data) != list:
        logging.error("data is not a list")
        exit(1)
    if type(sample_year) != int:
        logging.error("sample year is not an integer")
        exit(1)

    shortest_name = ""
    male_count = 0
    female_count = 0
    longest_name = ""
    shortest_name = ""

    # filter data for sample year
    data = filter_data_by_year(data, sample_year)
    if len(data) == 0:
        logging.error(f"no data found for sample year {sample_year}")
        return

    validate_dog_dict(data)

    # calculate stats
    for i, data_sample in enumerate(data):
        # male dogs count
        if data_sample["SexHundLang"] == "männlich":
            male_count += 1
        # female dogs count
        if data_sample["SexHundLang"] == "weiblich":
            female_count += 1
        # longest name
        if len(data_sample["HundenameText"]) > len(longest_name):
            longest_name = data_sample["HundenameText"]
        # shortest name
        if i == 0:  # first iteration
            shortest_name = data_sample["HundenameText"]
        if (
            len(data_sample["HundenameText"]) < len(shortest_name)
            and data_sample["HundenameText"] != "?"
        ):
            shortest_name = data_sample["HundenameText"]

    # create temporary list for finding out count of names
    dog_names = [
        data_sample["HundenameText"]
        for data_sample in data
        if data_sample["HundenameText"] != "?"  # ignore unknown names
    ]

    # find most common names
    most_common_dog_names = Counter(dog_names).most_common(10)  # (name, count)
    for index, element in enumerate(most_common_dog_names):
        most_common_dog_names[index] = (str(element[1]), str(element[0]))
    logging.debug(most_common_dog_names)

    # print results
    col_headers = ("Stat", "Value")
    rows = (
        ("sample year:", str(sample_year)),
        (
            "sample data count:",
            str(len(data)),
        ),
        ("male count:", str(male_count)),
        ("female count:", str(female_count)),
        ("longest name:", str(longest_name)),
        ("shortest name:", str(shortest_name)),
    )
    print_rich_table(col_headers, rows)
    print_rich("Most common Names :dog:")
    print_rich_table(("Count", "Name"), most_common_dog_names)
