import os

from custom_venv_builder import CustomVenvBuilder

PACKAGES_TO_INSTALL = [
    "black",
    "flake8",
    "isort",
    "numpy",
    "pandas",
    "openpyxl",
    "xlrd",
    "xlsxwriter",
]


def main():
    # Check the existance of a venv directory. If venv is not present, then
    # create venv and install packages.
    base_dir = os.getcwd()

    data_dir = os.path.join(base_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    cara_venv = os.path.join(base_dir, "venv")
    if not os.path.exists(cara_venv):
        # Create the virtual environment
        venv_builder = CustomVenvBuilder(
            with_pip=True, packages_to_install=PACKAGES_TO_INSTALL
        )
        venv_builder.create(cara_venv)

    print("Installation complete!")


if __name__ == "__main__":
    main()
