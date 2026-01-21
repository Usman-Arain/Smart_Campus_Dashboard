import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os

print("Current working directory:", os.getcwd())

# Load recommendations CSV
recs = pd.read_csv("outputs/hybrid_sports_recommendations.csv")

# Optional: parse participants & volunteers lists if stored as string
recs['actual_participants'] = recs['actual_participants'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
recs['assigned_volunteers'] = recs['assigned_volunteers'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
recs['actual_count'] = recs['actual_participants'].apply(len)
recs['volunteer_count'] = recs['assigned_volunteers'].apply(len)

# ---------- Dashboard ----------
fig, axes = plt.subplots(4, 1, figsize=(14, 22))

# 1️⃣ Hybrid Score
sns.barplot(
    data=recs.sort_values('score', ascending=False),
    x='event_name',
    y='score',
    color="steelblue",
    ax=axes[0]
)
axes[0].set_title("Hybrid Score per Event", fontsize=16)
axes[0].set_xlabel("")
axes[0].set_ylabel("Hybrid Score", fontsize=12)
axes[0].tick_params(axis='x', rotation=45)

# 2️⃣ Predicted vs Actual Participants
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
axes[1].set_title("Predicted vs Actual Participants", fontsize=16)
axes[1].set_xlabel("Predicted Turnout")
axes[1].set_ylabel("Actual Participants")
axes[1].legend(title="Event Type")

# 3️⃣ Injuries
sns.barplot(
    data=recs.sort_values('injuries', ascending=False),
    x='event_name',
    y='injuries',
    color="tomato",
    ax=axes[2]
)
axes[2].set_title("Number of Injuries per Event", fontsize=16)
axes[2].set_xlabel("")
axes[2].set_ylabel("Injuries")
axes[2].tick_params(axis='x', rotation=45)

# 4️⃣ Volunteers Assigned
sns.barplot(
    data=recs.sort_values('volunteer_count', ascending=False),
    x='event_name',
    y='volunteer_count',
    color="mediumseagreen",
    ax=axes[3]
)
axes[3].set_title("Volunteers Assigned per Event", fontsize=16)
axes[3].set_xlabel("")
axes[3].set_ylabel("Number of Volunteers")
axes[3].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
