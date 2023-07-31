from progress.bar import Bar

import time


def start(args):
    """Start the sampling of the process metrics. There will be one last sample point after the time has run out to
    ensure all required data is captured."""

    samples = []

    # Using a non-float monotonic clock to avoid being messed-up by clock changes (time-zime or DST changes)
    start_time = time.monotonic_ns()

    continue_sampling = True
    current_time = start_time
    with Bar(
        f"Sampling process {args.process}",
        max=args.duration,
        suffix="%(percent).1f%% - %(index)i/%(max)i seconds",
    ) as bar:
        while continue_sampling:
            # Get the time of the current iteration
            delta = time.monotonic_ns() - current_time
            current_time += delta

            # Simulate sampling
            time.sleep(0.3)
            samples.append({"time": time.time()})

            # Update the progressbar and break-loop condition
            bar.next(delta / 1e9)
            continue_sampling = (current_time - start_time) / 1e9 <= args.duration

            # Sleep until the next iteration (aiming for the same sub-second fraction for all iterations)
            wake_up_delay = (
                args.pace - (time.monotonic_ns() - start_time) / 1e9 % args.pace
            )
            time.sleep(wake_up_delay)

    return samples
