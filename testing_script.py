import os

# import utils.extract_compound_rows
# import utils.filter_by_compound
from utils import create_dfs, get_xls_file_names

STARTING_ROW_INDEX = 5
ENDING_KEYWORD = "SHUTDOWN"


# Data comes from a machine output. The keyword should always be present.
def find_ending_index(df):
    return df.index.get_loc(ENDING_KEYWORD)


def main():
    cwd = os.getcwd()
    data_dir = os.path.join(cwd, "data")

    filenames = get_xls_file_names(data_dir)

    data = create_dfs(filenames, [])

    # end_index = find_ending_index(data[0]["Leucine"])

    df_1 = list(data[0].values())[0]

    print(df_1.index)

    # filtered_data = utils.filter_by_compound.filter_by_compound(data, [])
    # print(filtered_data)

    # df_keys = filtered_data.keys()
    # df = filtered_data[df_keys[0]]

    # print(df)


if __name__ == "__main__":
    main()
