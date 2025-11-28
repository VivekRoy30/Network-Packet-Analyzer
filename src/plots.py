import os
import pandas as pd
import pickle
import matplotlib
matplotlib.use("MacOSX")
import matplotlib.pyplot as plt
import subprocess

print("Loaded plots.py")

from preprocess import preprocess

PLOT_DIR = os.path.abspath("../plots")
print("Saving plots to:", PLOT_DIR)

try:
    os.makedirs(PLOT_DIR, exist_ok=True)
    print("Plot directory created or already exists.")
except Exception as e:
    print("Failed to create plot directory:", e)

def load_model():
    with open("../models/iso_forest.pkl", "rb") as f:
        return pickle.load(f)

def load_data():
    df = pd.read_csv("../data/packets.csv")
    clean = preprocess(df)
    return df, clean

def plot_anomaly_scores(df, clean, model):
    scores = model.decision_function(clean)

    plt.figure(figsize=(10, 5))
    plt.hist(scores, bins=50)
    plt.title("Anomaly Score Distribution")
    plt.xlabel("Anomaly Score")
    plt.ylabel("Frequency")
    plt.grid(True)

    plt.savefig(f"{PLOT_DIR}/anomaly_score_distribution.png")
    subprocess.run(["open", f"{PLOT_DIR}/anomaly_score_distribution.png"])
    plt.show()

def plot_packet_length(df):
    plt.figure(figsize=(10, 5))
    plt.hist(df["Length"], bins=60)
    plt.title("Packet Length Distribution")
    plt.xlabel("Packet Length")
    plt.ylabel("Frequency")
    plt.grid(True)

    plt.savefig(f"{PLOT_DIR}/packet_length_distribution.png")
    subprocess.run(["open", f"{PLOT_DIR}/packet_length_distribution.png"])
    plt.show()

def plot_anomaly_timeline(df, clean, model):
    scores = model.decision_function(clean)

    plt.figure(figsize=(12, 5))
    plt.plot(scores)
    plt.title("Anomaly Timeline")
    plt.xlabel("Packet Index")
    plt.ylabel("Anomaly Score")
    plt.grid(True)

    plt.savefig(f"{PLOT_DIR}/anomaly_timeline.png")
    subprocess.run(["open", f"{PLOT_DIR}/anomaly_timeline.png"])
    plt.show()

def plot_flags_frequency(df):
    flag_counts = df["Info"].str.extractall(r"\[(.*?)\]")[0].value_counts()

    plt.figure(figsize=(8, 5))
    flag_counts.plot(kind="bar")
    plt.title("TCP Flag Frequency")
    plt.xlabel("Flag")
    plt.ylabel("Count")
    plt.grid(True)

    plt.savefig(f"{PLOT_DIR}/flags_frequency.png")
    subprocess.run(["open", f"{PLOT_DIR}/flags_frequency.png"])
    plt.show()

def plot_protocol_distribution(df):
    plt.figure(figsize=(8, 5))
    df["Protocol"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Protocol Distribution")
    plt.ylabel("")

    plt.savefig(f"{PLOT_DIR}/protocol_distribution.png")
    subprocess.run(["open", f"{PLOT_DIR}/protocol_distribution.png"])
    plt.show()

def generate_all_plots():
    print("Current working directory:", os.getcwd())
    df, clean = load_data()
    model = load_model()

    plot_anomaly_scores(df, clean, model)
    plot_packet_length(df)
    plot_anomaly_timeline(df, clean, model)
    plot_flags_frequency(df)
    plot_protocol_distribution(df)

    print("\nAll plots generated and saved to /plots folder.\n")

if __name__ == "__main__":
    generate_all_plots()