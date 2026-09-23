# Customer retention analysis

This project prepares customer shopping data, loads it into PostgreSQL, explores it with SQL, and presents the results in Power BI.

## Files

- `customer_retention.py`: cleans the CSV and loads the `customer` table.
- `customer_retention.sql`: analysis queries for the `customer` table.
- `Customer Behavior Dashboard.pbix`: Power BI report.
- `requirements-customer-retention.txt`: Python dependencies.

The input CSV is not included. Place your downloaded `customer_shopping_behavior.csv` beside the Python script, or pass its location with `--csv`.

## Run

1. Create a PostgreSQL database named `customer_behavior` on `localhost:5432`.
2. Install the Python dependencies in your selected interpreter:

   ```powershell
   python -m pip install -r requirements-customer-retention.txt
   ```

3. Load the data:

   ```powershell
   python customer_retention.py
   ```

   The script asks for the local `postgres` user's password. You can also pass `--csv`, `--database-url`, or `--table`. Each run replaces the destination table.
4. Open `customer_retention.sql` in pgAdmin's Query Tool, connect to `customer_behavior`, and run the queries.
5. Open the `.pbix` file in Power BI Desktop. If prompted to update the data source, point it to your PostgreSQL server and the `customer_behavior` database, then enter your own database credentials.

The Python and SQL files do not store a database password.
