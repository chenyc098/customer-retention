"""Clean customer shopping data and load it into PostgreSQL.

In PyCharm, put customer_shopping_behavior.csv beside this file and run it.
The default database is customer_behavior on localhost, as in the original script.
"""

import argparse
import getpass
import os
from pathlib import Path


FREQUENCY_DAYS = {
    "Fortnightly": 14,
    "Weekly": 7,
    "Monthly": 30,
    "Quarterly": 90,
    "Bi-Weekly": 14,
    "Annually": 365,
    "Every 3 Months": 90,
}
AGE_GROUPS = ["Young Adult", "Adult", "Middle-aged", "Senior"]
REQUIRED_COLUMNS = {
    "age",
    "category",
    "review_rating",
    "frequency_of_purchases",
    "promo_code_used",
}


def prepare_data(csv_path, pd):
    """Read and clean the shopping CSV."""
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

    df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")
    df["review_rating"] = df["review_rating"].fillna(
        df.groupby("category")["review_rating"].transform("median")
    )

    ages = pd.to_numeric(df["age"], errors="coerce")
    if ages.notna().sum() < 4:
        raise ValueError("CSV needs at least four rows with valid ages for age groups.")
    df["age_group"] = pd.qcut(ages, q=4, labels=AGE_GROUPS)
    df["purchase_frequency_days"] = df["frequency_of_purchases"].map(FREQUENCY_DAYS)
    df = df.drop(columns="promo_code_used")
    return df


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).resolve().with_name("customer_shopping_behavior.csv"),
        help="Input CSV path (default: beside this script)",
    )
    parser.add_argument(
        "--database-url",
        default=os.environ.get("CUSTOMER_RETENTION_DATABASE_URL"),
        help="Override the local customer_behavior database with a SQLAlchemy PostgreSQL URL",
    )
    parser.add_argument("--table", default="customer", help="PostgreSQL table name")
    args = parser.parse_args()

    if not args.csv.is_file():
        parser.error(
            f"CSV file not found: {args.csv}. Put customer_shopping_behavior.csv "
            "beside this script or pass --csv with its full path."
        )

    try:
        import pandas as pd
    except ImportError:
        parser.error("pandas is missing. Install packages from requirements-customer-retention.txt in the PyCharm interpreter.")

    try:
        df = prepare_data(args.csv, pd)
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        parser.error(f"Could not prepare CSV: {exc}")

    print(f"Prepared {len(df)} rows and {len(df.columns)} columns from {args.csv}.")
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.engine import URL
    except ImportError:
        parser.error("SQLAlchemy is missing. Install packages from requirements-customer-retention.txt in the PyCharm interpreter.")

    database_url = args.database_url
    if not database_url:
        database_url = URL.create(
            "postgresql+psycopg2",
            username="postgres",
            password=getpass.getpass("PostgreSQL password for postgres: "),
            host="localhost",
            port=5432,
            database="customer_behavior",
        )
    try:
        engine = create_engine(database_url)
        with engine.begin() as connection:
            df.to_sql(args.table, connection, if_exists="replace", index=False)
        engine.dispose()
    except Exception as exc:
        parser.error(f"PostgreSQL load failed: {exc}")
    print(f"Loaded data into PostgreSQL table '{args.table}'.")


if __name__ == "__main__":
    main()
