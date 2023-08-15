def linear_regression(x, y):
    """This function computes a simple linear regression. It is better to use NumPy or scikit-learn for
    a battle tested and performant implementation rather than this ad-hoc code.

    It has been tested on this single test bench, verified using a spreadsheet software:
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]
    slope, intercept = linear_regression(x, y)
    slope == 0.6
    intercept == 2.2
    """

    if (len(x) != len(y)) or len(x) == 1:
        return None, None

    # Calculate the means of x and y
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    # Calculate the slope and intercept of the line
    numerator = sum([(xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)])
    denominator = sum([(xi - mean_x) ** 2 for xi in x])

    slope = numerator / denominator
    intercept = mean_y - slope * mean_x

    return slope, intercept


def find_mem_leak(samples):
    """A process is considered to have a memory lead if the trend-line over the second half of the recording is rising."""

    # Select the samples of the second half of the recording
    mid_timestamp = (samples[0]["timestamp"] + samples[-1]["timestamp"]) / 2
    samples_filtered = list(filter(lambda s: s["timestamp"] >= mid_timestamp, samples))

    # Compute the regression
    x = [s["timestamp"] for s in samples_filtered]
    y = [s["mem_real"] for s in samples_filtered]
    slope, intercept = linear_regression(x, y)

    # Return the PID and process creation time of the process detected
    return (
        {
            "channel": "mem_real",
            "creation_epoch": samples[0]["creation_epoch"],
            "name": samples[0]["name"],
            "pid": samples[0]["pid"],
            "warning": "POSSIBLE_MEMORY_LEAK",
        }
        if slope != None and slope > 0
        else None
    )


def get_average(samples):
    """Compute the average of the given samples, for each metric channel."""

    if not len(samples):
        return None

    # Dictionnary to hold the computed statistics
    averages = {
        "creation_epoch": samples[0]["creation_epoch"],
        "name": samples[0]["name"],
        "pid": samples[0]["pid"],
    }

    # For each metric recorded, compute the average
    channels = ["cpu_percent", "mem_real", "num_open_files"]
    for channel in [key for key in samples[0].keys() if key in channels]:
        sum = 0
        for sample in samples:
            sum += sample[channel]
        averages[f"{channel}_avg"] = sum / len(samples)

    # Return the PID and process creation time of the process detected
    return averages
