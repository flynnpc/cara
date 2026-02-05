import os
import subprocess
import sys
from venv import EnvBuilder

# Copied from: https://runebook.dev/en/docs/python/library/venv/an-example-of-extending-envbuilder # noqa: E501


class CustomVenvBuilder(EnvBuilder):
    """
    An EnvBuilder subclass that automatically installs a list of default packages. # noqa: E501
    """

    def __init__(self, *args, packages_to_install=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the list of packages to install
        self.packages_to_install = (
            packages_to_install if packages_to_install is not None else []
        )
        self.verbose = True  # A little extra output is helpful

    def post_setup(self, context):
        """
        Runs after the environment has been created. Used here to install packages. # noqa: E501
        :param context: The context object, containing paths and environment info.
        """
        # --- Customization Logic Starts Here ---

        # 1. Get the path to the venv's pip executable
        # 'context.env_exe' is the venv's Python executable path
        # 'context.bin_path' is the directory for executables (bin/ or Scripts/) # noqa: E501
        pip_path = os.path.join(context.bin_path, "pip")

        # Ensure 'pip' exists (it usually does unless `--without-pip` was passed) # noqa: E501
        if not os.path.exists(pip_path):
            # On Windows, pip is often `pip.exe`
            pip_path = os.path.join(context.bin_path, "pip.exe")
            if not os.path.exists(pip_path):
                print(
                    f"Warning: pip executable not found at {context.bin_path}. Skipping package installation."  # noqa: E501
                )
                return

        # 2. Construct the installation command
        if self.packages_to_install:
            print(
                f"Installing default packages: {', '.join(self.packages_to_install)}..."  # noqa: E501
            )

            # Example command: ['/path/to/venv/bin/pip', 'install', 'requests', 'click'] # noqa: E501
            command = [pip_path, "install"] + self.packages_to_install

            # 3. Execute the command
            try:
                # Use subprocess.check_call for robust execution and error checking # noqa: E501
                subprocess.check_call(
                    command, stdout=sys.stdout, stderr=sys.stderr
                )  # noqa: E501
                print("Default packages installed successfully! ")

                # create requirements.txt file # noqa: E501
                req_command = [pip_path, "freeze", ">", "requirements.txt"]

                subprocess.check_call(
                    req_command, stdout=sys.stdout, stderr=sys.stderr
                )  # noqa: E501
                print("requirements.txt created successfully.")
            except subprocess.CalledProcessError as e:
                print(f"ERROR: Failed to install packages: {e}")
            except FileNotFoundError:
                print(
                    "ERROR: Could not run pip. Is it correctly installed in the base Python?"  # noqa: E501
                )
