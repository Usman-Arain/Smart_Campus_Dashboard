import pandas as pd
import numpy as np
import os

# Load datasets
students = pd.read_csv("data/students.csv")
events = pd.read_csv("data/events.csv")
attendance = pd.read_csv("data/attendance.csv")

def get_conflict_free_schedule(df):
    """
    Sort by end time and remove overlaps.
    Handles dynamic time generation if columns are missing.
    """
    if df.empty:
        return df

    # If times are missing, generate them dynamically based on length of df
    if 'start_time' not in df.columns:
        # Create a list of start/end times that won't exceed the dataframe length
        # This creates slots: 09:00-10:00, 10:00-11:00, etc.
        generated_starts = [f"{9 + i:02d}:00" for i in range(len(df))]
        generated_ends = [f"{10 + i:02d}:00" for i in range(len(df))]
        
        df = df.copy() # Avoid SettingWithCopyWarning
        df['start_time'] = generated_starts
        df['end_time'] = generated_ends

    # Greedy Algorithm: Sort by end_time to maximize non-conflicting events
    df = df.sort_values(by='end_time')
    scheduled_events = []
    last_end_time = "00:00"

    for _, row in df.iterrows():
        if row['start_time'] >= last_end_time:
            scheduled_events.append(row)
            last_end_time = row['end_time']
            
    return pd.DataFrame(scheduled_events)

def recommend_upcoming_events(student_id, top_n=5):
    # 1. Content-Based Score (Interest Match)
    student = students[students['student_id'] == student_id].iloc[0]
    events['score'] = events['event_type'].apply(lambda x: 1.0 if x == student['interests'] else 0.5)

    # 2. Collaborative Filtering (Attendance Similarity)
    # (Optional: Add your matrix-dot logic here if needed)

    # 3. Filter only Upcoming/Non-attended
    attended = attendance[attendance['student_id'] == student_id]['event_id'].tolist()
    upcoming = events[~events['event_id'].isin(attended)].copy()

    # 4. Apply Scheduling Algorithm (Constraint: No overlapping sports)
    sports_events = upcoming[upcoming['event_type'] == 'Sports']
    other_events = upcoming[upcoming['event_type'] != 'Sports']
    
    # Auto-create timetable for sports
    timetable = get_conflict_free_schedule(sports_events)
    
    # Combine back
    final_recommendations = pd.concat([timetable, other_events.head(top_n-len(timetable))])
    return final_recommendations.sort_values(by='score', ascending=False)

def generate_final_output():
    """Generates the single source of truth for the dashboard."""
    # Generate for a sample view
    output = recommend_upcoming_events(student_id=1)
    
    # Remove any injury-related columns to keep it PURE
    cols_to_keep = ['event_id', 'event_name', 'event_type', 'start_time', 'end_time', 'score']
    output = output[[c for c in cols_to_keep if c in output.columns]]
    
    os.makedirs("outputs", exist_ok=True)
    output.to_csv("outputs/upcoming_timetable.csv", index=False)
    return output

if __name__ == "__main__":
    generate_final_output()