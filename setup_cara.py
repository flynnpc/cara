#!/usr/bin/env python3
import os
import subprocess
import sys
import venv


def get_system_venv_path(dir):
    # Determine the path to the python executable within the new venv
    # Using this executable ensures we are installing into the venv
    if sys.platform == "win32":
        python_bin = os.path.join(dir, "Scripts")
    if sys.platform == "darwin" or sys.platform == "linux":
        python_bin = os.path.join(dir, "bin")

    return python_bin | ""


def build_venv(dir):
    # Create the virtual environment
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(dir)


def main():
    # Check the existance of a cara directory. Setup environment if not present
    # or define the target directory for the virtual environment.
    # This creates a 'cara' directory relative to where the script is run
    base_dir = os.getcwd()
    cara_dir = os.path.join(base_dir, "cara")

    if os.path.exists(cara_dir):
        print(f"Activating virtual environment: {cara_dir}")

    print(f"Creating virtual environment in: {cara_dir}")

    # Create the virtual environment
    venv.create(cara_dir)

    # Get the path to the python executable within the new venv
    python_bin = get_system_venv_path(cara_dir)

    if not os.path.exists(python_bin):
        print(f"Error: Python executable not found at {python_bin}")
        sys.exit(1)

    print("Activating venv and installing Pandas...")
    # Install pandas using the venv's python executable
    subprocess.check_call([python_bin, "-m", "pip", "install", "pandas"])

    print("Freezing requirements to requirements.txt...")
    # Define path for requirements.txt inside the cara directory
    req_path = os.path.join(cara_dir, "requirements.txt")

    # Run pip freeze and write the output to the file
    with open(req_path, "w") as f:
        subprocess.check_call([python_bin, "-m", "pip", "freeze"], stdout=f)

    print(f"Success! Requirements saved to {req_path}")


if __name__ == "__main__":
    main()
