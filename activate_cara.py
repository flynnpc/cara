#!/usr/bin/env python3
import os
import subprocess
import sys

from custom_venv_builder import CustomVenvBuilder

PACKAGES_TO_INSTALL = ["black", "flake8", "isort", "numpy", "pandas"]


def determine_os():
    # Determine the OS of the current system
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "linux":
        return "linux"
    if sys.platform == "darwin":
        return "macos"
    else:
        return ""


def activate_venv(venv_dir):
    os_platform = determine_os()

    print(f"Activating virtual environment: {venv_dir}")

    if os_platform == "":
        print("unknown operating system")
        return
    # fmt: off
    if os_platform == "windows":
        activate_venv_cmd = os.path.join(
            venv_dir,
            "Scripts",
            "activate.bat")
    else:
        activate_venv_cmd = ["source", os.path.join(
            venv_dir,
            "bin",
            "activate")]
    # fmt: on

    subprocess.run(activate_venv_cmd)
    return


def main():
    # Check the existance of a cara directory. Setup environment if not present
    # or define the target directory for the virtual environment.
    # This creates a 'cara' directory relative to where the script is run
    base_dir = os.getcwd()
    cara_dir = os.path.join(base_dir, "cara")
    os.mkdir(cara_dir)

    cara_venv = os.path.join(cara_dir, "venv")
    if os.path.exists(cara_dir):
        activate_venv(cara_venv)

    # Create the virtual environment
    venv_builder = CustomVenvBuilder(
        with_pip=True, packages_to_install=PACKAGES_TO_INSTALL
    )
    venv_builder.create(cara_venv)
    activate_venv(cara_venv)


if __name__ == "__main__":
    main()
