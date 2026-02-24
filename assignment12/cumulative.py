# cumulative.py
# Task 2: Line Plot of Cumulative Revenue

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


DB_PATH = Path("db/lesson.db")

SQL = """
SELECT
  o.order_id,
  SUM(price * quantity) AS total_price
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p   ON l.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id;
"""


def load_orders(db_path: Path) -> pd.DataFrame:
  conn = sqlite3.connect(db_path)
  try:
    df = pd.read_sql_query(SQL, conn)
  finally:
    conn.close()

  if df.empty:
    raise ValueError("Query returned 0 rows. Check database and joins.")

  df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce")
  if df["total_price"].isna().any():
    raise ValueError("total_price contains NaN after numeric conversion.")

  return df


def plot_cumulative(df: pd.DataFrame) -> None:
  df["cumulative"] = df["total_price"].cumsum()

  ax = df.plot(
    kind="line",
    x="order_id",
    y="cumulative",
    legend=False,
    figsize=(10, 5),
    color="darkgreen"
  )

  ax.set_title("Cumulative Revenue by Order")
  ax.set_xlabel("Order ID")
  ax.set_ylabel("Cumulative Revenue")

  plt.tight_layout()
  plt.show()


def main() -> None:
  if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found: {DB_PATH.resolve()}")

  df = load_orders(DB_PATH)
  plot_cumulative(df)


if __name__ == "__main__":
  main()
