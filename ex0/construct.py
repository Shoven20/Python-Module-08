#!/usr/bin/env python3


import os
import site
import sys


def in_virtual_environment() -> bool:
    return sys.prefix != sys.base_prefix


def environment_name() -> str:
    declared: str = os.environ.get("VIRTUAL_ENV", "")
    if declared != "":
        return os.path.basename(declared)
    return os.path.basename(sys.prefix)


def site_packages_of(prefix: str) -> str:
    if os.name == "nt":
        return os.path.join(prefix, "Lib", "site-packages")
    version: str = f"python{sys.version_info.major}"
    version = version + f".{sys.version_info.minor}"
    return os.path.join(prefix, "lib", version, "site-packages")


def global_packages_path() -> str:
    if not in_virtual_environment():
        installed: list[str] = site.getsitepackages()
        if len(installed) > 0:
            return installed[len(installed) - 1]
    return site_packages_of(sys.base_prefix)


def show_plugged_in() -> None:
    print("MATRIX STATUS: You're still plugged in")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows")
    print("Then run this program again.")


def show_construct() -> None:
    print("MATRIX STATUS: Welcome to the construct")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {environment_name()}")
    print(f"Environment Path: {sys.prefix}")
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print("Package installation path:")
    print(site_packages_of(sys.prefix))


def show_package_locations() -> None:
    print("Package locations:")
    print(f"Global environment: {global_packages_path()}")
    if in_virtual_environment():
        print(f"Virtual environment: {site_packages_of(sys.prefix)}")
    else:
        print("Virtual environment: none, packages go global")
    print(f"User packages: {site.getusersitepackages()}")


if __name__ == "__main__":
    if in_virtual_environment():
        show_construct()
    else:
        show_plugged_in()
    print()
    show_package_locations()
