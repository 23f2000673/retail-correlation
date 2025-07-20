# gen.py
import sqlite3
import json
import pandas as pd

# --- Step 1: Load SQL into an in-memory SQLite DB ---
# Use 'retail-data.sql' if you renamed the file, otherwise use the original name.
sql_file = "q-sql-correlation-github-pages.sql"
conn = sqlite3.connect(":memory:")
with open(sql_file) as f:
    conn.executescript(f.read())

# --- Step 2: Pull out the three columns using the correct table and column names ---
# The table is 'retail_data', not 'sales'.
# It's good practice to match the case of the columns defined in the SQL file.
df = pd.read_sql("SELECT Returns, Avg_Basket, Promo_Spend FROM retail_data", conn)

# --- Step 3: Compute all three Pearson correlations ---
# The dictionary keys are the "pair" names for the output.
# The values use the correct DataFrame column names (case-sensitive).
pairs = [
    ("Returns-Avg_Basket", "Returns", "Avg_Basket"),
    ("Returns-Promo_Spend", "Returns", "Promo_Spend"),
    ("Avg_Basket-Promo_Spend", "Avg_Basket", "Promo_Spend"),
]
corrs = {name: df[x].corr(df[y]) for name, x, y in pairs}

# --- Step 4: Pick the strongest correlation (by absolute value) ---
best = max(corrs.items(), key=lambda kv: abs(kv[1]))  # (name, value)

# --- Step 5: Dump to result.json, rounding to 2 decimal places as in the example ---
# The example shows two decimal places, so round(value, 2) is safer.
out = {"pair": best[0], "correlation": round(best[1], 2)}
with open("result.json", "w") as f:
    json.dump(out, f, indent=2)

print("Correlation calculations complete.")
print(f' - Returns-Avg_Basket: {corrs["Returns-Avg_Basket"]:.2f}')
print(f' - Returns-Promo_Spend: {corrs["Returns-Promo_Spend"]:.2f}')
print(f' - Avg_Basket-Promo_Spend: {corrs["Avg_Basket-Promo_Spend"]:.2f}')
print("-----------------------------------------")
print(f"Strongest correlation written to result.json: {out}")
