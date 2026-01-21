import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os

# ---------- Setup ----------
print("Current working directory:", os.getcwd())
sns.set(style="whitegrid")  # consistent style for all plots

# ---------- Load Data ----------
recs = pd.read_csv("outputs/hybrid_sports_recommendations.csv")

# Parse participants lists stored as string
recs['actual_participants'] = recs['actual_participants'].apply(
    lambda x: ast.literal_eval(x) if pd.notna(x) else []
)

# Compute actual participant count
recs['actual_count'] = recs['actual_participants'].apply(len)

# ---------- 1️⃣ Top events by hybrid score ----------
plt.figure(figsize=(12,6))
sns.barplot(
    data=recs.sort_values('score', ascending=False),
    x='event_name',
    y='score',
    color="steelblue"
)
plt.xticks(rotation=45, ha='right')
plt.title("Top Recommended Events by Hybrid Score", fontsize=14)
plt.xlabel("Event Name", fontsize=12)
plt.ylabel("Hybrid Score", fontsize=12)
plt.tight_layout()
plt.show()

# ---------- 2️⃣ Predicted turnout vs actual participants ----------
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=recs,
    x='predicted_turnout',
    y='actual_count',
    hue='event_type',
    s=100,
    palette="Set2"
)
max_val = max(recs['predicted_turnout'].max(), recs['actual_count'].max())
plt.plot([0, max_val], [0, max_val], 'r--', label="Perfect Prediction")
plt.title("Predicted Turnout vs Actual Participants", fontsize=14)
plt.xlabel("Predicted Turnout", fontsize=12)
plt.ylabel("Actual Participants", fontsize=12)
plt.legend(title="Event Type")
plt.tight_layout()
plt.show()

# ---------- 3️⃣ Event type distribution ----------
plt.figure(figsize=(8,5))
sns.countplot(data=recs, x='event_type', color="mediumseagreen")
plt.title("Distribution of Recommended Event Types", fontsize=14)
plt.xlabel("Event Type", fontsize=12)
plt.ylabel("Number of Events", fontsize=12)
plt.tight_layout()
plt.show()

# ---------- 4️⃣ Injuries per event ----------
plt.figure(figsize=(12,6))
sns.barplot(
    data=recs.sort_values('injuries', ascending=False),
    x='event_name',
    y='injuries',
    color="tomato"
)
plt.xticks(rotation=45, ha='right')
plt.title("Number of Injuries per Event", fontsize=14)
plt.xlabel("Event Name", fontsize=12)
plt.ylabel("Injuries", fontsize=12)
plt.tight_layout()
plt.show()


# ---------- 5️⃣ Combined Event Dashboard ----------
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

# ---- a) Hybrid Score ----
sns.barplot(
    data=recs.sort_values('score', ascending=False),
    x='event_name',
    y='score',
    color="steelblue",
    ax=axes[0]
)
axes[0].set_title("Hybrid Score per Event", fontsize=14)
axes[0].set_xlabel("Event Name", fontsize=12)
axes[0].set_ylabel("Hybrid Score", fontsize=12)
axes[0].tick_params(axis='x', rotation=45)

# ---- b) Predicted vs Actual Turnout ----
max_val = max(recs['predicted_turnout'].max(), recs['actual_count'].max())
sns.scatterplot(
    data=recs,
    x='predicted_turnout',
    y='actual_count',
    hue='event_type',
    s=100,
    palette="Set2",
    ax=axes[1]
)
axes[1].plot([0, max_val], [0, max_val], 'r--', label="Perfect Prediction")
axes[1].set_title("Predicted vs Actual Participants", fontsize=14)
axes[1].set_xlabel("Predicted Turnout", fontsize=12)
axes[1].set_ylabel("Actual Participants", fontsize=12)
axes[1].legend(title="Event Type")

# ---- c) Injuries ----
sns.barplot(
    data=recs.sort_values('injuries', ascending=False),
    x='event_name',
    y='injuries',
    color="tomato",
    ax=axes[2]
)
axes[2].set_title("Number of Injuries per Event", fontsize=14)
axes[2].set_xlabel("Event Name", fontsize=12)
axes[2].set_ylabel("Injuries", fontsize=12)
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
