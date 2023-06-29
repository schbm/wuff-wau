import random
import logging
import pathlib

from sys import exit

from wuff_wau.data import get_data
from wuff_wau.data import parse_json
from wuff_wau.common import print_rich
from wuff_wau.data import get_mime_type
from wuff_wau.common import print_rich_table
from wuff_wau.data import filter_data_by_year
from wuff_wau.data import validate_dog_dict


# validates the output directory
# exits on error
# returns the path as a pathlib.Path object
def validate_dir_path(output_dir):
    if type(output_dir) != str:
        logging.error("output directory is not a string")
        exit(1)
    logging.debug(f"validating output directory: {output_dir}")
    path = pathlib.Path(output_dir)
    if path == pathlib.Path.cwd():
        logging.debug("output directory is current working directory")
    if path == pathlib.Path.home():
        logging.debug("output directory is home directory")
    if path.is_dir():
        logging.debug("output directory is a directory")
    if path.is_file():
        logging.error("output directory is a file")
        exit(1)
    if not path.exists():
        logging.error("output directory does not exist")
        exit(1)
    return path


# Creates a image file with a random dog image
# input: data, sample_year, output_dir
# data: list of dog data (list)
# sample_year: year to sample data from (int)
# output_dir: directory to save the image file (str)
# and a random dog name, birth date
# prints random dog information to the console
def action_create(data, sample_year, output_dir):
    logging.debug(f"creating from data of sample year {sample_year}")

    if type(data) != list:
        logging.error("data is not a list")
        exit(1)
    if type(sample_year) != int:
        logging.error("sample year is not an integer")
        exit(1)
    if type(output_dir) != str:
        logging.error("output directory is not a string")
        exit(1)

    # filter data for sample year
    data = filter_data_by_year(data, sample_year)
    if len(data) == 0:
        logging.error(f"no data found for sample year {sample_year}")
        return

    validate_dog_dict(data)

    # validate output directory
    path = validate_dir_path(output_dir)

    # get random data from sample data
    random_name = data[random.randint(0, len(data))]["HundenameText"]
    random_birth = data[random.randint(0, len(data))]["GebDatHundJahr"]
    random_sex = data[random.randint(0, len(data))]["SexHundLang"]

    # create file name
    file_name = f"{random_name}_{random_birth}.jpg"
    logging.debug(f"filename: {file_name}")

    # create file path
    result_path = path / file_name
    # check if file already exists
    if result_path.exists():
        logging.error(f"image file already exists: {result_path.as_posix()}")
        # check image url returned from api until it is a jpeg
        mime_type = ""
        logging.debug("checking until a jpeg image is found")
        while mime_type != "image/jpeg":
            url = "https://random.dog/woof.json"
            json_data = get_data(url)
            json_data = parse_json(json_data)
            mime_type = get_mime_type(json_data["url"])
            logging.debug(f"random.dog returned url with mime type: {mime_type}")
        image_data = get_data(json_data["url"])
        logging.debug("writing new image file")

        # write the image to file
        try:
            with result_path.open("wb") as image_file:
                image_file.write(image_data)
            print_rich(f"url: {result_path.as_posix()} :thumbs_up:")
        except FileNotFoundError:
            logging.error("image file could not be created: no such directory found")
        except IOError:
            logging.error("error creating or writing image file")

    # print random dog information to console
    col_headers = ("Name", "Birth Date", "Sex")
    rows = list()
    rows.append((random_name, random_birth, random_sex))
    logging.debug(col_headers)
    logging.debug(rows)
    logging.debug(type(col_headers))
    logging.debug(type(rows))
    print_rich_table(col_headers, rows)
