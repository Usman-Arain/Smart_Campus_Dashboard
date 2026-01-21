import streamlit as st
import pandas as pd
from datetime import datetime
import ast

st.set_page_config(page_title="Student Dashboard", layout="wide")

st.title("🎓 Student Dashboard")
st.caption("AI-Powered Campus Event Participation System")

# ------------------ LOAD DATA ------------------
recs = pd.read_csv("outputs/hybrid_sports_recommendations.csv")

# Convert lists if stored as strings
if 'actual_participants' in recs.columns:
    recs['actual_participants'] = recs['actual_participants'].apply(ast.literal_eval)

# Round score to 2 decimals
recs['score'] = recs['score'].round(2)

# Add dummy upcoming date if not exists
if 'event_date' not in recs.columns:
    recs['event_date'] = pd.date_range(
        start=datetime.today(), periods=len(recs), freq="3D"
    )

# Participation history stored in session
if "history" not in st.session_state:
    st.session_state["history"] = []

# ------------------ METRICS ------------------
col1, col2, col3 = st.columns(3)

col1.metric("🎯 Recommended Events", len(recs))
col2.metric("✅ Participated", len(st.session_state["history"]))
col3.metric("🪑 Seats Per Event", 50)

st.divider()

# ------------------ UPCOMING EVENTS ------------------
st.subheader("📅 Recommended Events For You")

# Sort by score (AI recommendation)
recs = recs.sort_values("score", ascending=False)

for _, row in recs.iterrows():
    # Calculate current participants & remaining seats
    current_participants = len(row['actual_participants']) if 'actual_participants' in row else 0
    remaining_seats = 50 - current_participants  # assuming capacity 50

    with st.expander(f"🎫 {row['event_name']} | ⭐ {row['score']}"):
        left, right = st.columns([3, 1])

        left.markdown(f"""
        **📌 Event Type:** {row['event_type']}  
        **📆 Event Date:** {row['event_date'].strftime('%d %b %Y')}  
        **🪑 Capacity:** 50 seats  
        👥 **Participants:** {current_participants} / 50  
        🪑 **Remaining Seats:** {remaining_seats}
        """)

        st.progress(current_participants / 50)

        if right.button("Participate", key=row['event_name']):
            voucher_id = f"VCH-{len(st.session_state['history'])+1001}"

            st.session_state["history"].append({
                "event_name": row['event_name'],
                "event_type": row['event_type'],
                "event_date": row['event_date'].strftime('%d %b %Y'),
                "voucher": voucher_id,
                "joined_on": datetime.now().strftime('%d %b %Y %H:%M')
            })

            st.success(f"🎉 Registered Successfully! Voucher: {voucher_id}")

st.divider()

# ------------------ PARTICIPATION HISTORY ------------------
st.subheader("🧾 Participation History")

if st.session_state["history"]:
    history_df = pd.DataFrame(st.session_state["history"])

    # Sort history by joined date
    history_df["joined_on_sort"] = pd.to_datetime(history_df["joined_on"])
    history_df = history_df.sort_values("joined_on_sort", ascending=False)
    history_df = history_df.drop(columns="joined_on_sort")

    st.dataframe(history_df, use_container_width=True)
else:
    st.info("No participation records found.")
