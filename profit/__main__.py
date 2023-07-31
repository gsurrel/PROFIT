from profit.args import get_args

import profit.sampler as sampler
import profit.writer as writer

import datetime

from pathlib import Path


def main():
    args = get_args()

    # Start collecting samples
    samples = sampler.start(args)

    # Write the collected data
    now = datetime.datetime.now().isoformat().replace(":", ".").replace("T", " ")
    path = Path(args.output) / f"{now} {args.process}.csv"
    writer.to_csv(samples, path)


if __name__ == "__main__":
    main()
