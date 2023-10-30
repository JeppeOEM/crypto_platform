def timestamp_min_max(exchange):
    data_folder = f'data/{exchange}/'

    # Get a list of all files in the data folder
    file_list = os.listdir(data_folder)

    file_data_list = []

    for file_name in file_list:
        parts = file_name.split('_')

        file_data = {
            'lowest': int(parts[1]),
            'highest': int(parts[2])
        }

        file_data_list.append(file_data)

        file_data_list.sort(key=lambda x: x['lowest'])

    overlap = False
    overlap_start = None
    overlap_end = None

    for i in range(len(file_data_list) - 1):
        current_file_data = file_data_list[i]
        next_file_data = file_data_list[i + 1]

        # Check for overlap
        if current_file_data['highest'] >= next_file_data['lowest']:
            overlap = True
            overlap_start = max(
                current_file_data['lowest'], next_file_data['lowest'])
            overlap_end = min(
                current_file_data['highest'], next_file_data['highest'])

            # Calculate the duration of the overlap
            print("current file starting time:", )
            overlap_duration = overlap_end - overlap_start

            print(f"Overlap between {current_file_data['lowest']} and {current_file_data['highest']} "
                  f"and {next_file_data['lowest']} and {next_file_data['highest']}: Duration = {overlap_duration}"
                  f"overlap start", overlap_start, "overlap ends", overlap_end)

    if not overlap:
        print("No overlapping timestamps found")

    # Find the minimum and maximum values
    lowest_stamp = min(file_data['lowest'] for file_data in file_data_list)
    highest_stamp = max(file_data['highest'] for file_data in file_data_list)

    return lowest_stamp, highest_stamp

    # overlapping_entries = TimerangeModel.query.filter(
    #     TimerangeModel.timerange_start <= timerange.timerange_end,
    #     TimerangeModel.timerange_end >= timerange.timerange_start
    # ).all()

    # if overlapping_entries:
    #     overlapping_entries_data = []
    #     for entry in overlapping_entries:
    #         entry_data = {
    #             "id": entry.id,  # Replace with the actual attribute name in your model
    #             "timerange_start": entry.timerange_start,
    #             "timerange_end": entry.timerange_end,
    #             # Add other attributes as needed
    #         }
    #         overlapping_entries_data.append(entry_data)
    #     print(overlapping_entries_data)

