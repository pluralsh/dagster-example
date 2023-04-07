from setuptools import find_packages, setup

setup(
    name="plural-etl",
    version="1!0+dev",
    author="nnandhakumar",
    author_email="nnandhakumar@toptal.org",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["test"]),
    install_requires=[
        "aiobotocore",
        "dagster",
        "dagster-aws",
        "dagster-dbt",
        "dagster-pandas",
        "dagster-pyspark",
        "dagster-slack",
        "dagster-postgres",
        "dagster-duckdb",
        "dagster-duckdb-pandas",
        "dagster-duckdb-pyspark",
        "dagster-snowflake",
        "dagster-snowflake-pandas",
        "dagster-snowflake-pyspark",
        "mock",
        # DataFrames were not written to Snowflake, causing errors
        "pyarrow>=4.0.0",
        "pyspark",
        "requests",
        "gcsfs",
        "fsspec",
        "s3fs"
    ],
    extras_require={
        "dev": ["dagit", "pytest"],
        "tests": [
            "mypy",
            "pylint",
            "pytest"
        ],
    },
)