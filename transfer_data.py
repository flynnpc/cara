import os

# import pandas


def transfer_data():
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        print("It seems as though the data directory is missing. Maybe renamed?")
        return

    xls_files_to_transfer = []

    for dir_path, _, file_names in os.walk(data_dir):
        for file_name in file_names:
            if file_name.endswith(".xls"):
                file_path = os.path.join(dir_path, file_name)
                xls_files_to_transfer.append(file_path)
