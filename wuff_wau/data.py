import csv
import json
import logging
import requests
from sys import exit


# requests data content and decodes it if it is text
# input: url a string
# returns the content
# exits on error
def get_data(url):
    logging.debug("getting data")

    if type(url) is not str:
        logging.error("url must be a string")
        exit(1)

    # try to get the content
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.debug(response.headers)
    except (requests.URLRequired):
        logging.error("A valid URL is required to make a request")
        exit(1)
    except (requests.Timeout):
        logging.error("Request timed out - connect or read timeout")
        exit(1)
    except (requests.TooManyRedirects):
        logging.error("Too many redirects.")
        exit(1)
    except (requests.ConnectionError):
        logging.error(
            "Request ran into a network problem"
            + "(e.g. DNS failure, refused connection, etc)"
        )
        exit(1)
    except (requests.HTTPError):
        logging.error("Request got an http error code")
        exit(1)
    except (requests.exceptions):
        logging.error("An unexpected request exception occured")
        exit(1)
    # try to decode the content if it is text
    try:
        if response.apparent_encoding is not None:
            data = response.content.decode(response.apparent_encoding)
            logging.debug(f"got {len(response.content)} bytes")
            logging.debug(f"got {len(data)} decoded characters")
        else:
            logging.debug("returning raw content")
            data = response.content
    except (UnicodeDecodeError):
        logging.error("unicode decode error decoding requested data")
        exit(1)
    except (requests.exceptions):
        logging.error("a exception occured decoding request")
        exit(1)

    return data


# returns reference to a list of parsed csv data
# input: data a string
# returns a list of dicts
# dict keys are the csv headers
# dict values are the csv values
# exits on error
# example:
# [
#     {
#         "header1": "value1",
#         "header2": "value2",
#         "header3": "value3",
#     },
#     {
#         "header1": "value1",
#         "header2": "value2",
#         "header3": "value3",
#     },
# ]
def parse_csv(data):
    logging.debug("parsing csv")

    if type(data) is not str:
        logging.error("data must be a string")
        exit(1)

    # try to parse the data
    try:
        result = list()
        reader = csv.DictReader(data.splitlines(), delimiter=",")
        for row in reader:
            result.append(row)
        if len(result) == 0:
            logging.error("Error parsed data is empty")
            exit(1)
        logging.debug(f"parsed {len(result)} elements")
        logging.debug(f"with headers {reader.fieldnames}")
    except (csv.Error):
        logging.error("unexcpected error occured when csv parsing data")
        exit(1)
    return result


# parses json data
# input: data a string
# returns a list of dicts
# dict keys are the json keys
# dict values are the json values
# exits on error
def parse_json(data):
    logging.debug("parsing json")

    if type(data) is not str:
        logging.error("data must be a string")
        exit(1)

    # try to parse the data
    try:
        data = json.loads(data)
        logging.debug(f"parsed {len(data)} elements")
        logging.debug(data)
    except (json.JSONDecodeError):
        logging.error("unexpected error occured when parsing json data")
        exit(1)
    return data


# returns the newest sample year as a string
# input data is a list of dicts
# exits on error
# example: "2019"
def find_newest_sample_year(data):
    if type(data) is not list:
        logging.error("data is not a list")
        exit(1)
    logging.debug("finding newest sample year from data")
    # find the newest sample year
    sample_year = 0
    for sample_data in data:
        # if the year is newer than the current newest year
        if int(sample_data["StichtagDatJahr"]) > sample_year:
            sample_year = int(sample_data["StichtagDatJahr"])
    logging.debug(f"found newest sample year {sample_year}")
    return sample_year


# returns the mime type of the url as a string
# input url is a string
# returns None if the mime type is not set
# exits on error
def get_mime_type(url):
    # try to get the content type

    if type(url) is not str:
        logging.error("url must be a string")
        exit(1)

    session = requests.Session()
    try:
        response = session.head(url)
        logging.debug(response.headers)
    except (requests.URLRequired):
        logging.error("A valid URL is required to make a request")
        exit(1)
    except (requests.Timeout):
        logging.error("Request timed out - connect or read timeout")
        exit(1)
    except (requests.TooManyRedirects):
        logging.error("Too many redirects.")
        exit(1)
    except (requests.ConnectionError):
        logging.error(
            "Request ran into a network problem"
            + "(e.g. DNS failure, refused connection, etc)"
        )
        exit(1)
    except (requests.HTTPError):
        logging.error("Request got an http error code")
        exit(1)
    except (requests.exceptions):
        logging.error("An unexpected request exception occured")
        exit(1)
    # if the content type is not set return None
    if "content-type" not in response.headers.keys():
        return None

    return response.headers["content-type"]


# filters data by year
# input data is a list of dicts
# input year is an int
# returns a list of dicts
# exits on error
def filter_data_by_year(data, year):
    logging.debug("filtering data by year")

    if type(data) is not list:
        logging.error("data is not a list")
        exit(1)
    if type(year) is not int:
        logging.error("year is not an int")
        exit(1)

    filtered_data = list()
    for sample_data in data:
        if int(sample_data["StichtagDatJahr"]) == year:
            filtered_data.append(sample_data)
    logging.debug(f"filtered {len(filtered_data)} elements")
    return filtered_data


# validates the dog dict
# input data is a list of dicts
# exits on error
def validate_dog_dict(data):
    if type(data) is not list:
        logging.error("data is not a list")
        exit(1)
    logging.debug("validating dog dict")
    # validate the data
    for dog in data:
        if "StichtagDatJahr" not in dog.keys():
            logging.error("there is a dog in the sample data dat has no sample year field")
            exit(1)
        if "SexHundLang" not in dog.keys():
            logging.error("there is a dog in the sample data dat has no sex field")
            exit(1)
        if "HundenameText" not in dog.keys():
            logging.error("there is a dog in the sample data dat has no name field")
            exit(1)
        if "GebDatHundJahr" not in dog.keys():
            logging.error("there is a dog in the sample data dat has no birth year field")
            exit(1)
