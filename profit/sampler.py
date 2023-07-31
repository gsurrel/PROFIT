from progress.bar import Bar
import psutil

import time
from pprint import pprint


def start(args):
    """Start the sampling of the process metrics. There will be one last sample point after the time has run out to
    ensure all required data is captured."""

    samples_per_pid = {}

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

            # Sampling (getting multiple samples if several processes match)
            samples = get_sample(args.process, sample_duration=args.pace * 0.8)
            now = time.time()
            for sample in filter(lambda s: s != None, samples):
                # Generate a string that ensure no collisions even if a PID is recycled
                pid_stable = f"{sample['pid']} {sample['creation_epoch']}"
                if pid_stable not in samples_per_pid:
                    samples_per_pid[pid_stable] = []
                samples_per_pid[pid_stable].append({"timestamp": now, **sample})

            # Update the progressbar and break-loop condition
            bar.next(delta / 1e9)
            continue_sampling = (current_time - start_time) / 1e9 <= args.duration

            # Sleep until the next iteration (aiming for the same sub-second fraction for all iterations)
            wake_up_delay = (
                args.pace - (time.monotonic_ns() - start_time) / 1e9 % args.pace
            )
            time.sleep(wake_up_delay)

    return samples_per_pid


def get_sample(process_name, sample_duration=0.4):
    """Collect a smaple for the given process name."""
    processes = []
    for proc in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_info", "open_files"]
    ):
        processes.append(proc)

    # Filter by process names
    processes = filter(lambda p: p.info["name"] == process_name, processes)

    # Delay to get proper sampling (eg. CPU usage)
    time.sleep(sample_duration)

    # Fetch the values
    processes = map(lambda p: get_process_stats(p), processes)

    # Collect and return
    processes = list(processes)
    return processes if len(processes) else None


def get_process_stats(process):
    """Fetches the interesting process information. This may crash when trying to get information from a process the
    user hasn't created because of permission restrictions. Starting as root solves this problem. This is a deliberate
    decision instead of reporting bogus data (0 or None) silently."""
    with process.oneshot():
        try:
            stats = {
                "pid": process.pid,
                "name": process.name(),
                "cpu_percent": process.cpu_percent(),
                "mem_real": process.memory_info().rss,  # Reports the "Real memory" as System Monitor, unlike the "Private memory" as asked, because (it is broken on macOS)[https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_maps]
                "num_open_files": len(process.open_files()),
                "creation_epoch": process.create_time(),
            }
        except:
            stats = None
        return stats
