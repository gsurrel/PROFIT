from profit.args import get_args

import profit.analyzer as analyzer
import profit.sampler as sampler
import profit.writer as writer
import profit.server as server

import datetime
import os

from pathlib import Path


def main():
    args = get_args()

    # Start collecting samples
    samples = sampler.start(args)

    # Analyze the data
    analyses = []
    stats = []
    for pid, samples_per_pid in samples.items():
        stats.append(analyzer.get_average(samples_per_pid))
        analysis = analyzer.find_mem_leak(samples_per_pid)
        if analysis:
            analyses.append(analysis)

    # Flatten all samples into a single array (not split by stable pid)
    # in order to write the CSV file easily
    flat_samples = []
    for pid, samples_per_pid in samples.items():
        flat_samples.extend(samples_per_pid)

    # Write the collected data
    now = datetime.datetime.now().isoformat().replace(":", ".").replace("T", " ")
    path = Path(args.output) / f"{now} {args.process}"
    os.makedirs(path)
    writer.to_csv(flat_samples, path / "samples.csv")
    writer.to_csv(analyses, path / "analysis.csv")
    writer.to_csv(stats, path / "stats.csv")

    # Manage the visualization
    writer.generate_visualization(path)
    if args.serve_viz:
        server.start(path)


if __name__ == "__main__":
    main()
