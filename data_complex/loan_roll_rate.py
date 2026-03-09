import pandas as pd

# ──────────────────────────────────────────────
# Read loan data
# ──────────────────────────────────────────────
df = pd.read_csv("data_complex/loan.csv", parse_dates=["SnapshotDate"])

# ──────────────────────────────────────────────
# DPD Bucket mapping
# ──────────────────────────────────────────────
def dpd_bucket(dpd):
    if dpd <= 30:
        return "Normal"
    elif dpd <= 60:
        return "Mild"
    elif dpd <= 90:
        return "Moderate"
    elif dpd <= 120:
        return "Severe"
    else:
        return "Red Zone"

df["DPD_Bucket"] = df["DayPastDue"].apply(dpd_bucket)

# ──────────────────────────────────────────────
# Bucket order for comparison (higher = worse)
# ──────────────────────────────────────────────
bucket_order = {
    "Normal": 0,
    "Mild": 1,
    "Moderate": 2,
    "Severe": 3,
    "Red Zone": 4,
}

df["_bucket_rank"] = df["DPD_Bucket"].map(bucket_order)

# ──────────────────────────────────────────────
# Sort and compute DPD_Status (vs previous month)
# ──────────────────────────────────────────────
df = df.sort_values(["CustomerID", "SnapshotDate"]).reset_index(drop=True)

df["_prev_rank"] = df.groupby("CustomerID")["_bucket_rank"].shift(1)

def dpd_status(row):
    if pd.isna(row["_prev_rank"]):
        return "New"          # first snapshot, no prior month
    elif row["_bucket_rank"] > row["_prev_rank"]:
        return "Worsen"       # bucket worsened
    elif row["_bucket_rank"] < row["_prev_rank"]:
        return "Improve"      # bucket improved
    else:
        return "NoChange"     # same bucket

df["DPD_Status"] = df.apply(dpd_status, axis=1)

# ──────────────────────────────────────────────
# Drop helper columns and save
# ──────────────────────────────────────────────
df = df.drop(columns=["_bucket_rank", "_prev_rank"])

df.to_csv("data_complex/load_roll_rate.csv", index=False)

print(df.to_string(index=False))
print(f"\nSaved -> data_complex/load_roll_rate.csv  ({len(df)} rows)")
