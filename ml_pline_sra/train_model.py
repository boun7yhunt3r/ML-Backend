import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

# Generate synthetic dataset
np.random.seed(42)
n_samples = 100
data = {
    "event_id": [f"evt_{i:03d}" for i in range(n_samples)],
    "request_size": np.random.randint(100, 2000, n_samples),
    "response_time": np.random.randint(50, 1000, n_samples),
}
df = pd.DataFrame(data)
# Simulate risky events: high request_size or response_time increases risk
df["is_risky"] = ((df["request_size"] > 1000) | (df["response_time"] > 500)).astype(int)

# Save dataset
df.to_csv("data/security_logs.csv", index=False)

# Preprocess data
X = df[["request_size", "response_time"]]
y = df["is_risky"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = LogisticRegression(random_state=42)
model.fit(X_scaled, y)

# Save model and scaler
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("Model and scaler saved successfully.")