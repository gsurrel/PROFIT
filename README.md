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

This tool has been tested on Linux and macOS. It may work on other platforms, but this is untested. In particular, the library used to retrieve the process information (`psutil`) provides different features for the different platforms. For example, there is no good way to have the private memory used on macOS, and the number of open files are accessed differently on Unix systems and on Windows. Creating a full wrapper over `psutil` to abstract this kind of information is out of scope of this project.


# Design decisions

This tool should not require installing 3rd party dependencies.

## Time management

The clock used for the duration of the sampling is a monotonic clock, to avoid any problems with time-zone changes or Daylight Saving Time (DST) where the wall clock can jump back and forth. This also applies to leap seconds and similar matters.

However, the samples are timestamped using the Unix Epoch, in order to know when an event happened, according to the date and time used by humans.

Finally, the sampling will stop with exactly one sample after the moment the duration timer has expired. This is to ensure to have at least the range asked for. For example, sampling a process every 5 seconds, for a duration of 7 seconds will yield 3 samples at times t=0, t=5, and t=7.

## Data collected

The library used to collect data is `https://pypi.org/project/psutil/`, which has some limitations. Namely, it doesn't expose the private memory used by a process in a cross-platform way (or at all in the case of macOS). Therefore, the reported memory is the (resident set size)[https://en.wikipedia.org/wiki/Resident_set_size], which means the actual RAM used by the process.

*Note:* Accessing some information from a different user (*eg.* `root`) might be forbidden. Starting the tool using `sudo` may be a legitimate workaround in some cases.

## Writing to CSV

Even though CSV files are very loosely defined and should not be used as a database, they are very often used to exchange data. Generating a CSV file from the collected data is an easy way to import it in another software. The CSV format is as follows:

| pid | name | cpu_percent | mem_real | num_open_files | creation_epoch | timestamp |
|-----|------|-------------|----------|----------------|----------------|-----------|
| int | str  | float       | int      | int            | float          | float     |

Example of data collected:

```csv
pid,name,cpu_percent,mem_real,num_open_files,creation_epoch,timestamp
846,firefox,0.2,313929728,64,1689698014.07237,1690821721.743656
846,firefox,0.2,313933824,64,1689698014.07237,1690821723.630731
846,firefox,0.9,313933824,64,1689698014.07237,1690821725.6158972
846,firefox,0.2,313933824,64,1689698014.07237,1690821727.634214
```

## Detecting memory leaks

Memory leaks should be diagnosed with proper tools, such as [Valgrind](https://valgrind.org/). However, `PROFIT` tries to guess if there is some possible leak using the following heuristic:

> For a process recorded, a memory leak is considered as happening if the trend line of its memory usage `real_mem` has been strictly increasing for the second half of the recording.


# Changelog

All notable changes to this project will be documented in this section. It may move to a dedicated file in the future.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support multiple processes with the same name.

### Changed
- The CSV output has one more column to get stable and unique PIDs in case of recycling.

### Deprecated

### Removed

### Fixed

### Security


## [1.0.0]

First release, for fun and `PROFIT`! 🎉

### Added
- Create the initial project.


## Why the name

Finding a name is difficult, especially when looking for a playful and memorable name in a language that's not your own native language. It was a good opportunity to see what a machine running a generative large language-model could come-up with. I selected the following out if the three tries I did:

> How about `PROFIT` - Process Resource Oversight and Information Tracker? It's a playful and amusing acronym that highlights the utility's purpose of keeping an eye on resource usage while also suggesting that it helps you make more "profitable" decisions regarding system resources.

Here is what you avoided:

> How about `RUMPER` - which stands for "Resource Usage Monitor for Process Efficiency and Reporting"? It combines the playful connotation of "rumper" with the utility's primary purpose of tracking resource usage for a process. It's memorable and might bring a smile to the users' faces.

> How about `WASTE` - Whimsical Analysis of System's Tracked Expenditure? This humorous acronym playfully suggests that the utility helps you identify and manage any wasteful resource usage by processes on your system. It adds a fun and quirky touch to the otherwise serious task of resource tracking.
