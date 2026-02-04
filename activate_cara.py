#!/usr/bin/env python3
import os
import subprocess
import sys

# import venv


def determine_os():
    # Determine the OS of the current system
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "linux":
        return "linux"
    if sys.platform == "darwin":
        return "macos"

    return ""


# Determine if venv already exists
# if not:
# Just run a command based off of the OS to install a venv called venv.
# Then activate venv based on OS
# Install pandas
# Make requirements.txt
# else:
# activate venv


def main():
    # Check the existance of a cara directory. Setup environment if not present
    # or define the target directory for the virtual environment.
    # This creates a 'cara' directory relative to where the script is run
    base_dir = os.getcwd()
    cara_dir = os.path.join(base_dir, "cara")
    os.mkdir(cara_dir)

    os_platform = determine_os()

    cara_venv = os.path.join(cara_dir, "venv")
    if os.path.exists(cara_venv):
        print(f"Activating virtual environment: {cara_dir}")

        if os_platform == "":
            print("unknown operating system")
            return
        # fmt: off
        if os_platform == "windows":
            activate_venv_cmd = os.path.join(
                cara_venv,
                "Scripts",
                "activate.bat")
        else:
            activate_venv_cmd = ["source", os.path.join(
                cara_venv,
                "bin",
                "activate")]
        # fmt: on

        subprocess.run(activate_venv_cmd)

    # Create the virtual environment
    subprocess.run(["python3", "-m", "venv", cara_venv])

    # if not os.path.exists(python_bin):
    #     print(f"Error: Python executable not found at {python_bin}")
    #     sys.exit(1)


if __name__ == "__main__":
    main()
