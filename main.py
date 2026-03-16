import os

import pandas as pd

from src.input_validation import InputValidation as Valid
from utils import create_dfs, get_xls_file_names

DEFAULT_XLSX_FILE_NAME: str = "Compound Results.xlsx"
# Ask for requested compound name (sheet), if none is provided then get all compounds (sheets)
# From each XLS file, get the "Filename" and "Calculated amount" rows from corresponding sheet name.
# Rows start at header (4th line or where "Filename" and "Calculated amount" are located)
# Rows always end with a "Filename" entry of "SHUTDOWN"
# Check for inputed XLSX path.
# if append_data = Y
#   * Check for compound name in xlsx sheet (input).
#   * Add rows (series) to end of compound column. Most likely need openpyxl to read whole sheet. Pandas overwrites.
#     check for chart and other compatability if overwritten.
# if append_data = N
#   * create a new sheet with data compound columns.
# No xlsx means create a new xlsx file with data in single sheet.


def main():
    # Determine the output xlsx, if any.
    target_xlsx: str = input(
        """Enter the file path for any xlsx file you would like the data transferred into.
        Press enter if you would like to create a new xlsx file with the data."""
    )

    if Valid.check_if_output_xlsx_exists(target_xlsx):
        output_xlsx_path = target_xlsx
    else:
        output_xlsx_path = os.path.join(os.getcwd(), DEFAULT_XLSX_FILE_NAME)

    compound_input: list[str] = input(
        """Input the compound you would like to transfer. Seperate compound names with a comma (,)
        if you want to add multiple. Press enter if you want all compounds transferred."""
    )

    # Convert string to lowercase to make comparisons case insensitive.
    # Split at the comma and remove any remaining whitespace.
    compound_names: list[str] = (
        compound_input.lower().split(",").trim() if compound_input else []
    )

    # Get the file paths for all XLS files in the data directory
    data_files: list[str] = get_xls_file_names()

    only_one_xls: bool = Valid.check_only_one_xls(data_files)
    if not only_one_xls:
        return

    # Convert all of the XLS files in data directory to Pandas Data Frames (df)
    dfs_from_xls: list[dict[str, pd.DataFrame]] = create_dfs(data_files, compound_names)


if __name__ == "__main__":
    main()
