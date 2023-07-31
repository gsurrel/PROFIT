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
    analyses = []
    for pid, pid_samples in samples.items():
        analysis = analyzer.find_mem_leak(pid_samples)
        if analysis:
            analyses.append(analysis)

    # Flatten all samples into a single array (not split by stable pid)
    flat_samples = []
    for pid, pid_samples in samples.items():
        flat_samples.extend(pid_samples)

    # Write the collected data
    now = datetime.datetime.now().isoformat().replace(":", ".").replace("T", " ")
    path = Path(args.output) / f"{now} {args.process}"
    os.makedirs(path)
    writer.to_csv(flat_samples, path / "samples.csv")
    writer.to_csv(analyses, path / "analysis.csv")


if __name__ == "__main__":
    main()
