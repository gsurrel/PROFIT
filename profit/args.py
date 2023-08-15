import argparse
import tempfile


def get_args():
    parser = argparse.ArgumentParser(
        description="""PROFIT: Process Resource Oversight and Information Tracker

    Profit is a process sampler to gather CPU usage, (private) memory usage, and number of file
    handles opened for a given amount of time, at a given pace."""
    )
    parser.add_argument(
        "process",
        help="name of the process to watch, can be a glob pattern",
    )
    parser.add_argument(
        "--duration",
        action="store",
        help="duration for which to record",
        required=True,
        type=int,
    )
    parser.add_argument(
        "--pace",
        action="store",
        default=5,
        help="pace at which to sample (in seconds)",
        type=int,
    )
    parser.add_argument(
        "--output",
        action="store",
        default=tempfile.mkdtemp(),
        help="directory in which to write the collected data",
    )
    return parser.parse_args()
