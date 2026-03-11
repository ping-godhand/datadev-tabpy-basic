import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_absolute_error

# ============================================================
# 1) Load Data
# ============================================================
df = pd.read_csv("data/03-Rice.csv")
print("=== Raw Data ===")
print(df)
print()

# Drop rows where Price is missing
df = df.dropna(subset=["Price"])
print("=== Clean Data (no missing Price) ===")
print(df)
print()

# Prepare X and y
X = df[["Item"]]          # feature  (number of items)
y = df["Price"]            # target   (price)

# ============================================================
# 2) Model 1 — Linear Regression  (y = ax + b)
# ============================================================
model1 = LinearRegression()
model1.fit(X, y)

a1 = model1.coef_[0]
b1 = model1.intercept_
print("=== Model 1: Linear (y = ax + b) ===")
print(f"  a = {a1:.2f}")
print(f"  b = {b1:.2f}")
print(f"  Formula: y = {a1:.2f}x + {b1:.2f}")
print()

y_pred1 = model1.predict(X)

# ============================================================
# 3) Model 2 — Quadratic Regression  (y = ax² + bx + c)
# ============================================================
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)   # creates columns [x, x²]

model2 = LinearRegression()
model2.fit(X_poly, y)

b2, a2 = model2.coef_          # coef order: [x, x²]
c2 = model2.intercept_
print("=== Model 2: Quadratic (y = ax^2 + bx + c) ===")
print(f"  a = {a2:.2f}")
print(f"  b = {b2:.2f}")
print(f"  c = {c2:.2f}")
print(f"  Formula: y = {a2:.2f}x^2 + {b2:.2f}x + {c2:.2f}")
print()

y_pred2 = model2.predict(X_poly)

# ============================================================
# 4) Compare Performance
# ============================================================
print("=== Compare Performance ===")
print(f"{'Metric':<20} {'Linear':>10} {'Quadratic':>10}")
print("-" * 42)
print(f"{'R2 Score':<20} {r2_score(y, y_pred1):>10.4f} {r2_score(y, y_pred2):>10.4f}")
print(f"{'MAE':<20} {mean_absolute_error(y, y_pred1):>10.4f} {mean_absolute_error(y, y_pred2):>10.4f}")
print()

# ============================================================
# 5) Predict Price for Item = 3
# ============================================================
new_item = np.array([[3]])
pred1 = model1.predict(new_item)[0]
pred2 = model2.predict(poly.transform(new_item))[0]

print("=== Predict: Item = 3 ===")
print(f"  Linear    -> Price = {pred1:.2f}")
print(f"  Quadratic -> Price = {pred2:.2f}")
