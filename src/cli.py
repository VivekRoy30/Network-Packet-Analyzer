import argparse
import pandas as pd
import pickle
from preprocess import preprocess

def load_model():
    with open("../models/iso_forest.pkl", "rb") as f:
        return pickle.load(f)

def analyze(file_path):
    # Load CSV
    df = pd.read_csv(file_path)
    clean = preprocess(df)

    # Load trained model
    model = load_model()

    # Predict anomalies
    preds = model.predict(clean)
    df["anomaly"] = preds  # -1 = anomaly, 1 = normal

    anomalies = df[df["anomaly"] == -1]

    print("\n===== Network Packet Analyzer =====")
    print(f"Total packets: {len(df)}")
    print(f"Anomalies detected: {len(anomalies)}")
    print(f"Anomaly percentage: {round((len(anomalies)/len(df))*100, 2)}%")

    print("\n===== Sample Anomalous Packets =====")
    print(anomalies.head(10))

    print("\nDone.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Packet Analyzer CLI")
    parser.add_argument("--file", required=True, help="Path to CSV packet file")
    args = parser.parse_args()

    analyze(args.file)
