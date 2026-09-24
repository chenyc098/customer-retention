# Customer Shopping Behaviour Analysis

An end-to-end analytics project using **Python, PostgreSQL, and Power BI** to prepare customer shopping data, explore purchasing patterns, and support merchandising and customer-engagement questions.

## Workflow

```mermaid
flowchart LR
    A[Shopping CSV] --> B[Python cleaning and features]
    B --> C[PostgreSQL customer table]
    C --> D[Ten SQL business questions]
    C --> E[Power BI dashboard]
```

## Business questions

- How does purchase value vary by customer group and shipping method?
- Which products receive the strongest ratings or are most frequently discounted?
- How do subscribers and non-subscribers differ in observed spending?
- What customer segments emerge from previous-purchase counts?
- Which products lead each category by observed purchase count?

## Methods

Python standardizes column names, fills missing ratings using category medians, creates age quartiles, and maps purchase-frequency labels to approximate day counts. SQL uses aggregation, subqueries, CASE expressions, CTEs, and window functions. The Power BI file presents the analysis visually.

**Interpretation:** this is shopping behaviour and segmentation analysis of a snapshot. It does not measure churn, cohort retention, or the causal effect of discounts/subscriptions. The original repository URL is retained for existing links.

## Files

| File | Purpose |
| --- | --- |
| [customer_retention.py](customer_retention.py) | Data preparation and PostgreSQL loading |
| [customer_retention.sql](customer_retention.sql) | Ten analytical questions |
| [Customer Behavior Dashboard.pbix](Customer%20Behavior%20Dashboard.pbix) | Downloadable Power BI report |
| [requirements-customer-retention.txt](requirements-customer-retention.txt) | Python dependencies |

## Verified findings

![Customer shopping summary](assets/shopping-summary.svg)

Calculated from the supplied `customer_shopping_behavior.csv` using the repository's Python preparation function:

- **3,900 records and 3,900 unique customer IDs**, with **$233,081** in recorded purchase value and **$59.76** mean purchase amount.
- **Clothing accounts for $104,264 (44.7%)** of recorded purchase value, the largest category in this sample.
- **1,053 subscribers (27.0%)** average **$59.49** per recorded purchase, versus **$59.87** for 2,847 non-subscribers. This sample does not show higher mean purchase value among subscribers.
- **37 missing review ratings** were filled using category medians; no ratings remained missing after preparation.

The image is a Python summary of the CSV, not a screenshot of the Power BI report. These descriptive findings do not establish causality or represent lifetime customer value.

## Data provenance

The original CSV was supplied locally. Its publisher, download URL, license, and whether it is synthetic have not been verified, so results describe this sample only. The raw file is not redistributed. To reproduce, place the original file beside the script or supply `--csv`.

SHA-256: `d1f0b8e906cde9d909361ea28f08b0f33e74659ed4a42cd1d747fd9db2ffa701`.

The PBIX is available above and requires Power BI Desktop; GitHub cannot render it directly.

## Analytical assumptions

- Segment labels are rules, not predictions: **New** = 0–1 previous purchases, **Returning** = 2–10, **Loyal** = more than 10, and **Unknown** = missing or invalid values.
- Age-group labels refer to sample quartiles, not fixed demographic age ranges. Repeated quartile boundaries can prevent `qcut` from forming four groups.
- Discount percentages retain decimal precision. Product-ranking ties use product name for consistent ordering.
- A category with no valid ratings retains missing ratings; unfamiliar purchase-frequency labels remain missing.
- Verify one row per customer before interpreting row counts as customer counts. The current script replaces the destination table each run.

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


## Validation

SQL percentage and segmentation corrections were checked using synthetic boundary cases. The Python preparation function was also run against the supplied 3,900-row CSV and the descriptive results above were recalculated. A live PostgreSQL/Power BI integration run was not performed. The synthetic SQL checks used SQLite for the shared percentage and CASE expressions, not PostgreSQL.
