# Palace Quicksight Tools

A suite of command line operations for exporting and importing quicksight dashboards from and to AWS accounts.
Exported resources can be found [here](https://github.com/ThePalaceProject/palace-quicksight-resources).

## Prerequisites

Install Poetry: [Installation instructions here](https://python-poetry.org/docs/).

## Installation

```shell
poetry install
poetry run ./bin/palace-quicksight --help
```

## Usage

```shell
./bin/palace-quicksight --help
Usage: palace-quicksight [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  export-analysis    Creates a template from the analysis and exports at...
  import-template    Import template and datasource files from json
  publish-dashboard  Create/Update a dashboard from a template
```
