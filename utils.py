import os

import pandas as pd

STARTING_ROW_INDEX = 5
ENDING_KEYWORD = "SHUTDOWN"
NEEDED_COLUMNS_INDEXES = [0, 1, 8]
DF_COLUMN_HEADS = ["Filename", "Sample Type", "Calculated amount"]
FILTER_KEYWORD_COLUMN = DF_COLUMN_HEADS[1]
FILTER_KEYWORD = "Unknown Sample"


# Data comes from a machine output. The keyword should always be present.
def find_ending_index(df):
    return df.index.get_loc(ENDING_KEYWORD)


def set_df_headers(
    dfs_by_compound: list[dict[str, pd.DataFrame]],
) -> list[dict[str, pd.DataFrame]]:
    reindexed_dfs = []
    for df_by_compound in dfs_by_compound:
        df = list(df_by_compound.values())[0]
        compound_name = list(df_by_compound.keys())[0]
        df.columns = DF_COLUMN_HEADS
        df.set_index(DF_COLUMN_HEADS[0], inplace=True)
        reindexed_dfs.append({compound_name: df})


def extract_compound_rows(dataframes: dict[str, pd.DataFrame]):
    compound_rows = {}

    for dataframe in dataframes:
        compound_name: str = dataframe.keys()[0]
        df: pd.DataFrame = dataframe.values()[0]

        end_index = find_ending_index(df)

        rows = df[STARTING_ROW_INDEX:end_index]

        compound_rows[compound_name] = rows

    return compound_rows


def filter_by_compound(
    dataframes_by_compound: list[dict[str, pd.DataFrame]], compound_names: list[str]
) -> list[dict[str, pd.DataFrame]]:

    if compound_names:
        compound_filtered_df: list[dict[str, pd.DataFrame]] = []
        for df in dataframes_by_compound:
            if df.keys()[0].lower() in compound_names:
                compound_filtered_df.append(df)
        return compound_filtered_df

    return dataframes_by_compound


def get_xls_file_names(data_dir):
    # data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        print("It seems as though the data directory is missing. Maybe it was renamed?")
        return

    xls_files_to_transfer = []

    for dir_path, _, file_names in os.walk(data_dir):
        for file_name in file_names:
            if file_name.lower().endswith(".xls"):
                file_path = os.path.join(dir_path, file_name)
                xls_files_to_transfer.append(file_path)

    return xls_files_to_transfer


def convert_xls_to_dfs(file_paths: list[str]) -> list[dict[str, pd.DataFrame]]:
    excel_as_dfs = []

    for file_path in file_paths:
        compound_to_df = {}

        dfs_by_compound = pd.read_excel(
            file_path,
            header=None,
            sheet_name=None,
            usecols=NEEDED_COLUMNS_INDEXES,
        )

        for compound in dfs_by_compound:
            df = dfs_by_compound[compound]
            df.columns = DF_COLUMN_HEADS
            df.set_index(DF_COLUMN_HEADS[0], inplace=True)

            compound_to_df[compound] = df

        excel_as_dfs.append(compound_to_df)

    return excel_as_dfs


def trim_unused_rows(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    # Data comes from a machine output. The keyword should always be present.
    end_index = dataframe.index.get_loc(ENDING_KEYWORD)

    return dataframe[STARTING_ROW_INDEX:end_index]


def filter_by_unknown_samples(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.loc[dataframe[FILTER_KEYWORD_COLUMN] == FILTER_KEYWORD]


def drop_unused_columns_inplace(df, column_names):
    df.drop(columns=column_names, inplace=True)


def create_dfs(
    file_paths: list[str], compound_names: list[str]
) -> list[dict[str, pd.DataFrame]]:
    dfs_by_compound = convert_xls_to_dfs(file_paths)

    compound_dfs: list[dict[str, pd.DataFrame]] = filter_by_compound(
        dfs_by_compound, compound_names
    )

    extracted_data = []

    for compound_df in compound_dfs:
        compound_name = list(compound_df)[0]
        df = list(compound_df.values())[0]
        trimmed_df = trim_unused_rows(df)
        filtered_df = filter_by_unknown_samples(trimmed_df)

        drop_unused_columns_inplace(filtered_df, FILTER_KEYWORD_COLUMN)

        extracted_data.append({compound_name: filtered_df})

    return extracted_data


# def transfer_data(output_xlsx_path):
