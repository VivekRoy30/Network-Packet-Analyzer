import argparse
import pandas as pd
import pickle
from preprocess import preprocess

def load_model():
    with open("models/iso_forest.pkl", "rb") as f:
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

    # Colors
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    print(f"\n{CYAN}===== Network Packet Analyzer ====={RESET}")

    print(f"{YELLOW}Total packets:{RESET} {len(df)}")

    if len(anomalies) > 0:
        print(f"{RED}Anomalies detected:{RESET} {len(anomalies)}")
    else:
        print(f"{GREEN}Anomalies detected: 0{RESET}")

    anom_percent = round((len(anomalies)/len(df))*100, 2)
    color = RED if anom_percent > 0 else GREEN
    print(f"{color}Anomaly percentage:{RESET} {anom_percent}%")

    print(f"\n{CYAN}===== Sample Anomalous Packets ====={RESET}")
    print(anomalies.head(10))

    print(f"\n{GREEN}Done.{RESET}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Packet Analyzer CLI")
    parser.add_argument("--file", required=True, help="Path to CSV packet file")
    args = parser.parse_args()

    analyze(args.file)
