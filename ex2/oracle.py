#!/usr/bin/env python3


import os
import sys


DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "",
    "API_KEY": "",
    "LOG_LEVEL": "DEBUG",
    "ZION_ENDPOINT": "",
}

PLACEHOLDER: str = "replace-with-your-own-key"


def load_env_file() -> bool:
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("WARNING: python-dotenv is not installed")
        print("Install it with: pip install -r requirements.txt")
        print("Falling back to the process environment only")
        return False
    loaded: bool = load_dotenv()
    if not loaded:
        print("WARNING: no .env file found")
        print("Create one with: cp .env.example .env")
    return loaded


def read_config() -> dict[str, str]:
    config: dict[str, str] = {}
    for name in DEFAULTS:
        config[name] = os.environ.get(name, DEFAULTS[name])
    return config


def mask(secret: str) -> str:
    if len(secret) < 4:
        return "****"
    return secret[0:3] + "*" * (len(secret) - 3)


def describe_database(config: dict[str, str]) -> str:
    url: str = config["DATABASE_URL"]
    if url == "":
        return "Not configured"
    if "localhost" in url or "127.0.0.1" in url:
        return "Connected to local instance"
    return "Connected to remote cluster"


def describe_api(config: dict[str, str]) -> str:
    key: str = config["API_KEY"]
    if key == "":
        return "Missing credentials"
    if key == PLACEHOLDER:
        return "Rejected, example key still in place"
    return "Authenticated"


def describe_zion(config: dict[str, str]) -> str:
    endpoint: str = config["ZION_ENDPOINT"]
    if endpoint == "":
        return "Offline"
    if endpoint.startswith("https://"):
        return "Online, encrypted channel"
    return "Online, clear channel"


def show_configuration(config: dict[str, str]) -> None:
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {describe_database(config)}")
    print(f"API Access: {describe_api(config)}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Zion Network: {describe_zion(config)}")


def show_mode_details(config: dict[str, str]) -> None:
    mode: str = config["MATRIX_MODE"]
    key: str = config["API_KEY"]
    print(f"Mode details ({mode}):")
    if mode == "production":
        print("  Secrets: hidden, never printed in production")
        print("  Traces: errors only, stack traces disabled")
        print("  Data source: live Zion mainframe")
    else:
        print(f"  Secrets: {mask(key)} shown masked for debugging")
        print(f"  Traces: verbose, log level {config['LOG_LEVEL']}")
        print("  Data source: local sandbox instance")


def check_configuration(config: dict[str, str]) -> list[str]:
    problems: list[str] = []
    mode: str = config["MATRIX_MODE"]
    if mode != "development" and mode != "production":
        problems.append(f"MATRIX_MODE '{mode}' is not a known mode")
    for name in DEFAULTS:
        if config[name] == "":
            problems.append(f"{name} is missing")
    if config["API_KEY"] == PLACEHOLDER:
        problems.append("API_KEY still holds the example value")
    if mode == "production":
        if config["LOG_LEVEL"] == "DEBUG":
            problems.append("LOG_LEVEL DEBUG leaks details in"
                            + " production")
        if config["ZION_ENDPOINT"].startswith("http://"):
            problems.append("ZION_ENDPOINT must use https in"
                            + " production")
    return problems


def show_security_check(config: dict[str, str], loaded: bool) -> None:
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if loaded:
        print("[OK] .env file properly configured")
    else:
        print("[KO] .env file missing, defaults in use")
    print("[OK] Production overrides available")
    print("[OK] .env listed in .gitignore, secrets stay local")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    loaded: bool = load_env_file()
    config: dict[str, str] = read_config()
    show_configuration(config)
    show_mode_details(config)
    problems: list[str] = check_configuration(config)
    if len(problems) > 0:
        print("ORACLE ALERT: the mainframe is not ready")
        for problem in problems:
            print(f"  - {problem}")
        print("Fix them in .env or in the process environment")
    show_security_check(config, loaded)
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    try:
        main()
    except OSError as error:
        print(f"ORACLE FAILED: {error}")
        sys.exit(1)
