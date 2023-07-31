from profit.args import get_args
import profit.sampler as sample

from pprint import pprint


def main():
    args = get_args()

    # Start collecting samples
    samples = sample.start(args)

    # Results
    pprint(samples)


if __name__ == "__main__":
    main()
