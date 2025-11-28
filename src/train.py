import pandas as pd
from sklearn.ensemble import IsolationForest
import pickle
from preprocess import preprocess

# 1. Load raw CSV
df = pd.read_csv("../data/packets.csv")

# 2. Preprocess into numeric feature dataset
clean = preprocess(df)

# 3. Train Isolation Forest
model = IsolationForest(
    n_estimators=200,
    contamination=0.02, # approx 2% anomalies
    random_state=42
)

model.fit(clean)

# 4. Save the model
with open("../models/iso_forest.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved to ../models/iso_forest.pkl")
