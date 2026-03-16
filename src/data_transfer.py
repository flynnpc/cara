# Check if data folder has only one file
# Prompt user and stop program if there are multiple files in folder

# Always transfer to a new sheet with transfer date as name.
# Name format mm-dd-yyyy_hh:mm:ss
# If name exists add (1)
# Format for new sheets
# Rows are file names
# Columns are compound names
# Values are corresponding file names and compounds
from datetime import datetime
from src.input_validation import InputValidation as Valid
import pandas as pd

# Make all CONSTANTS easily accessable. This is a repeat!!!
DF_IMPORT_COLUMN_HEADS = [
    "Filename",
    "Sample Type",
]  # "Calculated Amount" is left off list but imported
DF_COMPOUND_COLUMN = DF_IMPORT_COLUMN_HEADS[1]
DATE_FORMAT = "%m-%d-%Y_%H:%M:%S"

def rename_columns_to_compound_name(dataframes: list[dict[str, pd.DataFrame]]) -> list[dict[str, pd.DataFrame]]:
    output_dfs = []
    for dataframe in dataframes:
        compound_name = list(dataframe.keys())[0]
        df = list(dataframe.values())[0]
        df.rename(columns={DF_COMPOUND_COLUMN: compound_name})

        output_dfs.append({compound_name: df})

    return output_dfs

def join_dfs(dataframes: list[dict[str, pd.DataFrame]]) -> pd.DataFrame:
    joined_df: pd.DataFrame = None

    indexed_dfs = enumerate(dataframes)
    for index, dataframe in indexed_dfs:
        df = list(dataframe.values())[0]
        if index == 0:
            joined_df = df
        else:
            joined_df.join(df, how="outer")

    return joined_df




def create_excel_writer(output_xlsx_path:str, dataframe:pd.DataFrame):
    transfer_date = datetime.today().strftime(DATE_FORMAT)
    with pd.ExcelWriter(output_xlsx_path) as writer:
        dataframe.to_excel(writer, sheet_name=transfer_date)

def save_to_xlsx(output_xlsx_path:str, dataframes: list[dict[str, pd.DataFrame]]):