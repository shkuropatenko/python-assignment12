# wind_plotly.py
# Task 3: Interactive Visualizations with Plotly

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.data as pldata


HTML_PATH = Path("wind.html")


def strength_to_float(x: str) -> float:
  """
  Convert strength like '0-1' or '5-6' to midpoint float (e.g., 0.5, 5.5).
  Falls back to extracting the first number if no range is found.
  """
  if pd.isna(x):
      return float("nan")

  s = str(x).strip()

  # Try range pattern: number-number (supports decimals)
  m = re.search(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", s)
  if m:
    a = float(m.group(1))
    b = float(m.group(2))
    return (a + b) / 2.0

  # Otherwise extract first number in the string
  m2 = re.search(r"(\d+(?:\.\d+)?)", s)
  if m2:
    return float(m2.group(1))

  return float("nan")


def main() -> None:
  # Load dataset
  df = pldata.wind(return_type="pandas")

  # Print first and last 10 rows
  print(df.head(10).to_string(index=False))
  print("\n---\n")
  print(df.tail(10).to_string(index=False))

  # Clean: strength -> float
  df["strength"] = df["strength"].apply(strength_to_float)

  # Basic sanity check: drop rows where conversion failed
  df = df.dropna(subset=["strength", "frequency", "direction"])

  # Interactive scatter
  fig = px.scatter(
    df,
    x="strength",
    y="frequency",
    color="direction",
    title="Wind: Strength vs Frequency by Direction",
    labels={"strength": "Strength", "frequency": "Frequency", "direction": "Direction"},
    hover_data=df.columns,
  )

  # Save HTML
  fig.write_html(str(HTML_PATH), include_plotlyjs="cdn")

  # "Load" verification (simple check the file exists + non-empty)
  if not HTML_PATH.exists() or HTML_PATH.stat().st_size == 0:
    raise RuntimeError("wind.html was not created correctly.")

  # Optional: open in browser automatically (commented out to be safe in grading)
  # import webbrowser
  # webbrowser.open(HTML_PATH.resolve().as_uri())

  print(f"\nSaved interactive plot to: {HTML_PATH.resolve()}")


if __name__ == "__main__":
  main()
