from profit.args import get_args

import profit.analyzer as analyzer
import profit.sampler as sampler
import profit.writer as writer

import datetime
import os

from pathlib import Path


def main():
    args = get_args()

    # Start collecting samples
    samples = sampler.start(args)

    # Analyze the data
    analysis = list(filter(lambda i: i != None, analyzer.find_mem_leak(samples)))

    # Write the collected data
    now = datetime.datetime.now().isoformat().replace(":", ".").replace("T", " ")
    path = Path(args.output) / f"{now} {args.process}"
    os.makedirs(path)
    writer.to_csv(samples, path / "samples.csv")
    writer.to_csv(analysis, path / "analysis.csv")


if __name__ == "__main__":
    main()
