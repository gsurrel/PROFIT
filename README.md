# Process Resource Oversight and Information Tracker: `PROFIT`

`PROFIT` is a sampling resource tracker that can look very similar to other tools:

- Periodically samples CPU, (private) memory, and number of file descriptors opened,
- Limits the processes selected for sampling,
- Samples for a predefined amount of time,
- Logs the data as a CSV file.

## Installation

Currently, this tools lives only on this repository. Clone it to run it.

## Dependencies

Install the dependencies required using the following:

```
pip install -r requirements.txt
```

The Python code is formatted with [`black`](https://pypi.org/project/black/) using the default configuration.

## Running `PROFIT`

You can run `PROFIT` from the command-line as follows, which will display the help page:

```
$ python -m profit
```

Sampling the process `acme` every second for 60 seconds, do as follows:

```
$ python profit acme --pace=1 --duration=60
```


## Supported platforms

This tool has been tested on Linux and macOS. It may work on other platforms, but this is untested.


# Design decisions

This tool should not require installing 3rd party dependencies.


# Changelog

All notable changes to this project will be documented in this section. It may move to a dedicated file in the future.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

First release of PROFIT.

### Added
- Create the initial project

### Changed


### Deprecated


### Removed


### Fixed


### Security



## Why the name

Finding a name is difficult, especially when looking for a playful and memorable name in a language that's not your own native language. It was a good opportunity to see what a machine running a generative large language-model could come-up with. I selected the following out if the three tries I did:

> How about `PROFIT` - Process Resource Oversight and Information Tracker? It's a playful and amusing acronym that highlights the utility's purpose of keeping an eye on resource usage while also suggesting that it helps you make more "profitable" decisions regarding system resources.

Here is what you avoided:

> How about `RUMPER` - which stands for "Resource Usage Monitor for Process Efficiency and Reporting"? It combines the playful connotation of "rumper" with the utility's primary purpose of tracking resource usage for a process. It's memorable and might bring a smile to the users' faces.

> How about `WASTE` - Whimsical Analysis of System's Tracked Expenditure? This humorous acronym playfully suggests that the utility helps you identify and manage any wasteful resource usage by processes on your system. It adds a fun and quirky touch to the otherwise serious task of resource tracking.
