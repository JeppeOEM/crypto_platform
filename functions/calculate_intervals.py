def calculate_intervals(start_timestamp, end_timestamp, timeframe):
    print(start_timestamp, end_timestamp, timeframe, "FFS")
    interval_map = {
        "5m": 5 * 60,
        "15m": 15 * 60,
        "30m": 30 * 60,
        "1h": 60 * 60,
        "8h": 8 * 60 * 60,
        "1d": 24 * 60 * 60,
    }
    if timeframe not in interval_map:
        raise ValueError("Invalid interval parameter")
    interval_duration = interval_map[timeframe]
    time_difference = end_timestamp - start_timestamp
    print(time_difference, "HERE IS TIMEDIFF")
    print(interval_duration, "INTERVAL DURATION")
    interval_count = int(time_difference) // interval_duration
    print(interval_count)
    return interval_count