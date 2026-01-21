import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import json
import os
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# ---------- Page Config ----------
st.set_page_config(
    page_title="IU Smart Campus Admin",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 IU Smart Campus Admin Dashboard")
st.markdown("### Minimal Analytics for Students, Events, and Sports")

# ---------- Load Data ----------
students = pd.read_csv("data/students.csv")
logs = pd.read_csv("data/participation_logs.csv")
events = pd.read_csv("outputs/hybrid_sports_recommendations.csv")
attendance = pd.read_csv("data/attendance.csv")

# Convert string lists to actual lists
events['actual_participants'] = events['actual_participants'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
events['assigned_volunteers'] = events['assigned_volunteers'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
events['current_participants'] = events['actual_participants'].apply(len)
events['remaining_seats'] = 50 - events['current_participants']  # assuming 50 capacity per event
events['score'] = events['score'].round(2)

# ---------- Sidebar ----------
st.sidebar.header("Navigation")
module = st.sidebar.radio(
    "Select Module",
    ["Overview", "Students", "Events", "Sports"]
)

# ---------- OVERVIEW ----------
if module == "Overview":
    # --- NEW: LIVE EMERGENCY ALERTS SECTION ---
    st.subheader("🚨 Live Field Alerts")
    alert_path = "outputs/live_injury.json"

    if os.path.exists(alert_path):
        try:
            with open(alert_path, "r") as f:
                live_alerts = json.load(f)
            
            if live_alerts:
                # Display the most recent alert in a big red box
                latest = live_alerts[-1]
                st.error(f"**URGENT:** {latest['event']} detected at {latest['timestamp']}!")
                
                # Show all active alerts in an expander
                with st.expander("View Alert History / Manage Alerts"):
                    for i, alert in enumerate(reversed(live_alerts)):
                        col_a, col_b = st.columns([4, 1])
                        col_a.write(f"⚠️ **{alert['event']}** - Received at: {alert['timestamp']}")
                        if col_b.button("Done", key=f"clear_{i}"):
                            # Remove the specific alert and update file
                            live_alerts.remove(alert)
                            with open(alert_path, "w") as f:
                                json.dump(live_alerts, f)
                            st.rerun()
            else:
                st.success("✅ All clear. No active injuries on field.")
        except Exception as e:
            st.info("System initializing or alert file being updated...")
    else:
        st.success("✅ Field Monitoring: No active incidents.")

    st.markdown("---")
    st.subheader("📊 Quick Stats Overview")

    # ---------- Metrics ----------
    # (Keep your metrics calculations same as before)
    # Update total_injuries to include both CSV data and Live alerts
    live_count = 0
    if os.path.exists(alert_path):
        with open(alert_path, "r") as f:
            live_count = len(json.load(f))
    
    total_injuries = events['injuries'].sum() + live_count

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(students))
    col2.metric("Total Upcoming Events", len(events))
    col3.metric("Total Sports Events", len(events[events['event_type'] == 'Sports']))

    col4, col5, col6 = st.columns(3)
    col4.metric("Total Volunteers Assigned", events['assigned_volunteers'].apply(len).sum())
    col5.metric("Total Injuries (All Time)", int(total_injuries), delta=f"+{live_count} Live" if live_count > 0 else None)
    col6.metric("Avg. Attendance per Event", f"{events['current_participants'].mean():.1f}")

    st.markdown("---")

    # ---------- Event Attendance Overview ----------
    st.markdown("### Event Attendance Overview")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(
        data=events.sort_values('current_participants', ascending=False),
        x='event_name',
        y='current_participants',
        palette="Blues_d",
        ax=ax
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_ylabel("Current Participants")
    ax.set_xlabel("Event Name")
    plt.tight_layout()
    st.pyplot(fig)

    # ---------- Event Type Distribution ----------
    st.markdown("### Event Type Distribution")
    fig2, ax2 = plt.subplots(figsize=(6,4))
    sns.countplot(data=events, x='event_type', palette="Set2", ax=ax2)
    ax2.set_ylabel("Number of Events")
    ax2.set_xlabel("Event Type")
    plt.tight_layout()
    st.pyplot(fig2)

    # ---------- Participation Heatmap ----------
    st.markdown("### Student Participation Heatmap")
    if 'student_id' in logs.columns and 'event_id' in logs.columns:
        participation_matrix = logs.pivot_table(index='student_id', columns='event_id', aggfunc='size', fill_value=0)
        fig3, ax3 = plt.subplots(figsize=(12,6))
        sns.heatmap(participation_matrix, cmap="YlGnBu", cbar_kws={'label': 'Participation Count'}, ax=ax3)
        ax3.set_xlabel("Event ID")
        ax3.set_ylabel("Student ID")
        plt.tight_layout()
        st.pyplot(fig3)
    else:
        st.info("No participation logs available to generate heatmap")

# ---------- STUDENTS ----------
elif module == "Students":
    st.header("👨‍🎓 Students & Participation Records")

    st.subheader("📋 All Students")
    students_sorted = students.sort_values("name")

    # Configure AgGrid
    gb = GridOptionsBuilder.from_dataframe(students_sorted)
    gb.configure_selection(selection_mode="single", use_checkbox=False)
    gb.configure_pagination(enabled=True)
    gb.configure_grid_options(domLayout='normal')
    grid_options = gb.build()

    grid_response = AgGrid(
        students_sorted,
        gridOptions=grid_options,
        height=300,
        width='100%',
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True
    )

    selected = grid_response.get('selected_rows')  # this is a list of dicts

    if selected is None or (isinstance(selected, (list, pd.DataFrame)) and len(selected) == 0):
        st.warning("🔹 Click a row to view student details")
    else:
        # Convert the first selected dict to a DataFrame row
        student = pd.DataFrame(selected).iloc[0]
        student_id = student['student_id']

        # Show student details
        st.subheader("📄 Student Details")
        st.json(student.to_dict())

        # Participation history
        st.subheader("📅 Participation History")
        student_logs = logs[logs['student_id'] == student_id]

        if 'date' in student_logs.columns:
            student_logs['date'] = pd.to_datetime(student_logs['date'])
            student_logs = student_logs.sort_values('date', ascending=False)

        if student_logs.empty:
            st.warning("No participation found")
        else:
            st.dataframe(student_logs, use_container_width=True)

# ---------- EVENTS ----------
elif module == "Events":
    st.header("🎯 Events Management")
    
    # 1️⃣ Sort events by score
    events_sorted = events.sort_values('score', ascending=False)

    # 2️⃣ Configure AgGrid for Event Selection
    gb = GridOptionsBuilder.from_dataframe(events_sorted[['event_id', 'event_name', 'event_type', 'score', 'current_participants', 'remaining_seats']])
    gb.configure_selection(selection_mode="single", use_checkbox=False)
    gb.configure_pagination(enabled=True)
    grid_options = gb.build()

    st.subheader("📋 Select an Event")
    grid_response = AgGrid(
        events_sorted,
        gridOptions=grid_options,
        height=300,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True,
        theme='streamlit'
    )

    selected_event = grid_response.get('selected_rows')

    # 3️⃣ Robust Selection Check
    if selected_event is None or (isinstance(selected_event, (list, pd.DataFrame)) and len(selected_event) == 0):
        st.info("💡 Select an event from the table above to view volunteers and participants.")
    else:
        # Normalize selected data to a Series
        if isinstance(selected_event, pd.DataFrame):
            event_row = selected_event.iloc[0]
        else:
            event_row = pd.DataFrame(selected_event).iloc[0]
        
        selected_event_id = event_row['event_id']
        st.divider()
        st.subheader(f"🔍 Details for: {event_row['event_name']}")

        # 4️⃣ Display Volunteers & Participants in Two Columns
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🤝 Volunteers")
            # Filter logs or attendance for volunteers assigned to this event
            # Assuming 'logs' or 'attendance' has a 'role' column or similar
            # If you have a separate volunteers dataframe, filter it here
            event_volunteers = logs[(logs['event_id'] == selected_event_id) & (logs['role'] == 'Volunteer')]
            
            if event_volunteers.empty:
                st.write("No volunteers assigned yet.")
            else:
                # Merge with students to get names
                vol_details = event_volunteers.merge(students[['student_id', 'name']], on='student_id')
                st.dataframe(vol_details[['name', 'student_id']], use_container_width=True)

        with col2:
            st.markdown("### 👥 Participants")
            # Filter attendance for students who joined this event
            event_participants = attendance[attendance['event_id'] == selected_event_id]
            
            if event_participants.empty:
                st.write("No participants registered yet.")
            else:
                # Merge with students to get names
                part_details = event_participants.merge(students[['student_id', 'name']], on='student_id')
                st.dataframe(part_details[['name', 'student_id']], use_container_width=True)

# ---------- SPORTS ----------
elif module == "Sports":
    st.subheader("⛹️ Sports Event Management")
    
    # Load the hybrid output
    df_recs = pd.read_csv("outputs/hybrid_sports_recommendations.csv")
    
    # Show the AI-powered assignments
    for index, row in df_recs.iterrows():
        with st.expander(f"Event: {row['event_name']}"):
            col1, col2 = st.columns(2)
            col1.write(f"**Predicted Turnout:** {row['predicted_turnout']}")
            col1.write(f"**Live Injuries:** {row['injuries']}")
            col2.write(f"**AI-Assigned Volunteers:**")
            col2.write(row['assigned_volunteers'])
