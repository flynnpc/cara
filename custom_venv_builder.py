import os
import subprocess
import sys
from venv import EnvBuilder

# Copied from: https://runebook.dev/en/docs/python/library/venv/an-example-of-extending-envbuilder


class CustomVenvBuilder(EnvBuilder):
    """
    An EnvBuilder subclass that automatically installs a list of default packages.
    """

    def __init__(self, *args, packages_to_install=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the list of packages to install
        self.packages_to_install = (
            packages_to_install if packages_to_install is not None else []
        )
        self.verbose = True  # A little extra output is helpful

    # This function was copied from:
    # https://www.aicodesnippet.com/python/deployment-and-distribution/generating-requirementstxt-using-pip-freeze.html
    def generate_requirements_txt(self, pip_path, filename="requirements.txt"):
        try:
            result = subprocess.run(
                [pip_path, "freeze"], capture_output=True, text=True, check=True
            )
            with open(filename, "w") as f:
                f.write(result.stdout)
            print(f"Successfully created {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating requirements.txt: {e}")

    def post_setup(self, context):
        """
        Runs after the environment has been created. Used here to install packages.
        :param context: The context object, containing paths and environment info.
        """
        # --- Customization Logic Starts Here ---

        # 1. Get the path to the venv's pip executable
        # 'context.env_exe' is the venv's Python executable path
        # 'context.bin_path' is the directory for executables (bin/ or Scripts/)
        pip_path = os.path.join(context.bin_path, "pip")

        # Ensure 'pip' exists (it usually does unless `--without-pip` was passed)
        if not os.path.exists(pip_path):
            # On Windows, pip is often `pip.exe`
            pip_path = os.path.join(context.bin_path, "pip.exe")
            if not os.path.exists(pip_path):
                print(
                    f"Warning: pip executable not found at {context.bin_path}. Skipping package installation."
                )
                return

        # 2. Construct the installation command
        if self.packages_to_install:
            print(
                f"Installing default packages: {', '.join(self.packages_to_install)}..."
            )

            # Example command: ['/path/to/venv/bin/pip', 'install', 'requests', 'click']
            command = [pip_path, "install"] + self.packages_to_install

            # 3. Execute the command
            try:
                # Use subprocess.check_call for robust execution and error checking
                subprocess.check_call(command, stdout=sys.stdout, stderr=sys.stderr)
                print("Default packages installed successfully! ")
            except subprocess.CalledProcessError as e:
                print(f"ERROR: Failed to install packages: {e}")
            except FileNotFoundError:
                print(
                    "ERROR: Could not run pip. Is it correctly installed in the base Python?"
                )

            # create requirements.txt file
            self.generate_requirements_txt(pip_path=pip_path)
            print("requirements.txt created successfully.")
