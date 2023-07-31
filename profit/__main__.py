from profit.args import get_args
from pprint import pprint

import profit.sampler as sample


def main():
    args = get_args()

    # Start collecting samples
    samples = sample.start(args)

    # Results
    pprint(samples)


if __name__ == "__main__":
    main()
