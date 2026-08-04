#!/usr/bin/env python3


import importlib
import importlib.metadata
import sys


PROGRAMS: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}

DECLARED: dict[str, str] = {
    "pandas": ">=2.0",
    "numpy": ">=1.24",
    "matplotlib": ">=3.7",
}

DATA_POINTS: int = 1000
RESULT_FILE: str = "matrix_analysis.png"


def package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def check_dependencies() -> list[str]:
    print("Checking dependencies:")
    missing: list[str] = []
    for name in PROGRAMS:
        try:
            importlib.import_module(name)
        except ImportError:
            print(f"[KO] {name} - Program not loaded")
            missing.append(name)
            continue
        print(f"[OK] {name} ({package_version(name)}) - {PROGRAMS[name]}")
    return missing


def show_loading_help(missing: list[str]) -> None:
    print("LOADING FAILED: some programs are missing")
    for name in missing:
        print(f"  Missing: {name}")
    print("Load them with pip:")
    print("  python -m venv matrix_env")
    print("  source matrix_env/bin/activate")
    print("  pip install -r requirements.txt")
    print("Load them with Poetry:")
    print("  poetry install")
    print("  poetry run python loading.py")


def compare_managers() -> None:
    print("pip vs Poetry:")
    print("  pip reads requirements.txt, a flat list of pinned"
          + " versions")
    print("  pip needs a virtual environment created by hand")
    print("  pip installs what is written, conflicts are yours to"
          + " solve")
    print("  Poetry reads pyproject.toml, a declaration of ranges")
    print("  Poetry resolves the ranges and freezes them in"
          + " poetry.lock")
    print("  Poetry creates and runs the environment for you")
    print("Declared range vs installed version:")
    for name in PROGRAMS:
        installed: str = package_version(name)
        print(f"  {name}: declared {DECLARED[name]},"
              + f" installed {installed}")


def analyze_matrix_data() -> None:
    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as pyplot
    import numpy
    import pandas

    print("Analyzing Matrix data...")
    print(f"Processing {DATA_POINTS} data points...")
    generator = numpy.random.default_rng(1999)
    frame = pandas.DataFrame({
        "signal": generator.normal(100.0, 15.0, DATA_POINTS),
        "latency": generator.exponential(5.0, DATA_POINTS),
        "sector": generator.integers(1, 5, DATA_POINTS),
    })
    threshold: float = float(frame["signal"].mean()
                             + 2.0 * frame["signal"].std())
    frame["anomaly"] = frame["signal"] > threshold

    print(f"  Signal mean: {round(float(frame['signal'].mean()), 2)}")
    print(f"  Signal max: {round(float(frame['signal'].max()), 2)}")
    print(f"  Latency mean: {round(float(frame['latency'].mean()), 2)}")
    print(f"  Anomalies found: {int(frame['anomaly'].sum())}")
    print("  Mean signal per sector:")
    means = frame.groupby("sector")["signal"].mean()
    for sector in means.index:
        value: float = round(float(means[sector]), 2)
        print(f"    Sector {int(sector)}: {value}")

    print("Generating visualization...")
    figure, axes = pyplot.subplots(1, 2, figsize=(11, 4))
    axes[0].hist(frame["signal"], bins=30, color="#0f9d58")
    axes[0].set_title("Signal distribution")
    axes[0].set_xlabel("signal")
    axes[0].set_ylabel("count")
    axes[1].bar(means.index, means.to_numpy(), color="#0f9d58")
    axes[1].set_title("Mean signal per sector")
    axes[1].set_xlabel("sector")
    figure.suptitle("Matrix data analysis")
    figure.tight_layout()
    figure.savefig(RESULT_FILE, dpi=120)
    pyplot.close(figure)

    print("Analysis complete!")
    print(f"Results saved to: {RESULT_FILE}")


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    missing: list[str] = check_dependencies()
    if len(missing) > 0:
        show_loading_help(missing)
        return
    compare_managers()
    try:
        analyze_matrix_data()
    except (ValueError, OSError) as error:
        print(f"LOADING FAILED: {error}")


if __name__ == "__main__":
    print(f"Interpreter: {sys.executable}")
    main()
