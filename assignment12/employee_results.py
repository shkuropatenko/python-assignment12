# employee_results.py
# Task 1: Plotting with Pandas

from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = Path("db/lesson.db")

SQL = """
SELECT
  last_name,
  SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o     ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id = l.order_id
JOIN products p   ON l.product_id = p.product_id
GROUP BY e.employee_id;
"""


def load_employee_results(db_path: Path) -> pd.DataFrame:
  conn = sqlite3.connect(db_path)
  try:
    df = pd.read_sql_query(SQL, conn)
  finally:
    conn.close()

  if df.empty:
    raise ValueError("Query returned 0 rows. Check database contents and joins.")

  df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
  if df["revenue"].isna().any():
    raise ValueError("Revenue contains NaN after numeric conversion. Check query/data types.")

  return df.sort_values("revenue", ascending=False).reset_index(drop=True)


def plot_employee_revenue(employee_results: pd.DataFrame) -> None:
  ax = employee_results.plot(
    kind="bar",
    x="last_name",
    y="revenue",
    legend=False,
    color="steelblue",
    figsize=(10, 5),
  )

  ax.set_title("Revenue by Employee")
  ax.set_xlabel("Employee Last Name")
  ax.set_ylabel("Revenue")

  plt.xticks(rotation=45, ha="right")
  plt.tight_layout()
  plt.show()


def main() -> None:
  if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found: {DB_PATH.resolve()}")

  employee_results = load_employee_results(DB_PATH)
  plot_employee_revenue(employee_results)


if __name__ == "__main__":
  main()
