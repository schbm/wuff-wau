# wuff-wau CLI 

This command-line tool offers lookup operations on the open data of the registered dogs in the city of Zurich,
which can be found here: https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002

Additionally, it provides an option to create your own dog, with a random name, birth year, sex and media.
In the end the dog will be saved as a file to a provided directory
(if not provided, it will be saved in the current directory) in the following format:

## installation
poetry install

## usage
potry run wuff-wau
usage: WUFF-WAU [-h] [-y YEAR] [-d] {stats,find,create} ...

Various operations based on theregistered dogs in the city of Zurich

options:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  sample year of the data
  -d, --debug           enables debug output

actions:
  avilable positional arguments

  {stats,find,create}   for more help: command --help
    stats               shows stats about dogs
    find                find dogs with name
    create              gets a random dog image and assembles the file name randomlyfrom a name and birthdate  
                        from sample data

### Additional information

The projects dependencies and packaging is managed with poetry (https://python-poetry.org)

The minimum required version of python to run the script is python 3.10 (defined in pyproject.toml)

GL HF :)
