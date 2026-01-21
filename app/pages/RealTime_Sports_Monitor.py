import streamlit as st
import cv2
import os
import json
import ast
import time
from models.sports.injury_detection import detect_injury_live

st.title("🏃 Real-Time Sports Injury Monitoring")

VIDEO_DIR = "data/sports_videos"
videos = [v for v in os.listdir(VIDEO_DIR) if v.endswith(".mp4")]
selected_video = st.selectbox("Select Sports Video", videos)
video_path = os.path.join(VIDEO_DIR, selected_video)

# --- Define the UI Section for Alerts BEFORE the Video ---
st.markdown("---")
st.subheader("📡 Live Injury Alerts")
alert_placeholder = st.empty()  # This is the "Live" box

def show_alert_box():
    alert_path = "outputs/live_injury.json"
    if os.path.exists(alert_path):
        try:
            with open(alert_path, "r") as f:
                alerts = json.load(f)
            
            with alert_placeholder.container():
                # Show newest alert at the top
                for alert in reversed(alerts):
                    st.warning(f"**Status:** 🚨 {alert.get('event')} | **Time:** {alert.get('timestamp')}")
        except:
            pass
    else:
        alert_placeholder.success("✅ Monitoring: Field Clear")

# Initial check
show_alert_box()

# --- THE CLEAR BUTTON SECTION (Always runs after/outside the loop) ---
alert_path = "outputs/live_injury.json"
if os.path.exists(alert_path):
    # We place the button outside the loop so it's clickable after monitoring
    if st.button("🗑️ Clear All Alerts"):
        try:
            os.remove(alert_path)
            st.success("All alerts cleared!")
            time.sleep(0.5)
            st.rerun()
        except PermissionError:
            st.error("Error: System busy. Try again in a second.")


# --- Video Monitoring Section ---
if st.button("▶ Start Live Monitoring"):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: fps = 30
    
    st_frame = st.empty() 
    fall_counter = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        processed_frame, fall_counter, is_injured = detect_injury_live(frame, fall_counter, fps)
        
        # 1. Update the Video Frame
        frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        st_frame.image(frame_rgb, channels="RGB", use_container_width=True)

        # 2. Update the Status Box LIVE while video plays
        show_alert_box()

    cap.release()



# import streamlit as st
# import cv2
# import os
# import json
# import ast
# import time
# from models.sports.injury_detection import detect_injury_live

# st.title("🏃 Real-Time Sports Injury Monitoring")

# VIDEO_DIR = "data/sports_videos"
# videos = [v for v in os.listdir(VIDEO_DIR) if v.endswith(".mp4")]
# selected_video = st.selectbox("Select Sports Video", videos)
# video_path = os.path.join(VIDEO_DIR, selected_video)

# if st.button("▶ Start Live Monitoring"):
#     cap = cv2.VideoCapture(video_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
    
#     # Placeholders for live updates
#     st_frame = st.empty()        # For the video
#     st_status = st.empty()       # FOR THE LIVE STATUS (The part you want updated)
    
#     fall_counter = 0
    
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret: break

#         processed_frame, fall_counter, is_injured = detect_injury_live(frame, fall_counter, fps)
        
#         # 1. Update the Video Frame
#         frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
#         st_frame.image(frame_rgb, channels="RGB", use_container_width=True)

#         # 2. UPDATE STATUS LIVE BY READING THE JSON IMMEDIATELY
#         if os.path.exists("outputs/live_injury.json"):
#             with open("outputs/live_injury.json", "r") as f:
#                 alert_data = json.load(f)
#                 st_status.warning(f"""
#                 **Live Status:** 🚨 {alert_data.get('event')}  
#                 **Detection Time:** {alert_data.get('timestamp')}
#                 """)
#         else:
#             st_status.success("✅ Monitoring: Field Clear")

#     cap.release()

# # 1. Define the UI Header
# st.markdown("---")
# st.subheader("📡 Live Injury Alerts")

# # 2. CREATE A PLACEHOLDER (This stays visible and active)
# alert_placeholder = st.empty() 

# # Function to render the alert UI inside the placeholder
# def update_alert_ui():
#     alert_path = "outputs/live_injury.json"
#     if os.path.exists(alert_path):
#         try:
#             with open(alert_path, "r") as f:
#                 event_data = json.load(f)
            
#             # We use 'with alert_placeholder.container()' to push content into the placeholder
#             with alert_placeholder.container():
#                 st.warning(f"""
#                 **Status:** 🚨 {event_data.get('event', 'Injury')}  
#                 **Time:** {event_data.get('timestamp', 'N/A')}  
#                 """)
#                 # Note: Buttons inside loops are tricky, usually best to clear 
#                 # alerts via the sidebar or after the video stops.
#         except:
#             pass
#     else:
#         alert_placeholder.info("✅ System Monitoring: No injuries detected")

# # 3. Initial call to show status before video starts
# update_alert_ui()

# # # ---- Live Alert Section ----
# # st.markdown("---")
# # st.subheader("📡 Live Injury Alerts")

# # alert_path = "outputs/live_injury.json"

# # if os.path.exists(alert_path):
# #     try:
# #         # Read data and close immediately
# #         with open(alert_path, "r") as f:
# #             event_data = json.load(f)
        
# #         st.warning(f"""
# #         **Status:** 🚨 {event_data.get('event', 'Injury')}  
# #         **Time:** {event_data.get('timestamp', 'N/A')}  
# #         """)
        
# #         if st.button("✅ Clear Alert"):
# #             # Ensure the file is not being targeted by another thread
# #             try:
# #                 os.remove(alert_path)
# #                 st.success("Alert cleared!")
# #                 time.sleep(0.5) # Give Windows a moment to catch up
# #                 st.rerun()
# #             except PermissionError:
# #                 st.error("Could not clear alert. The detection loop might still be writing to it.")
# #     except (json.JSONDecodeError, IOError):
# #         # If the file is being written to while we read it, it might be empty/invalid
# #         st.info("Refreshing alert data...")

# # import streamlit as st
# # import os
# # import cv2
# # import json
# # import time
# # from models.sports.injury_detection import detect_injury, detect_injury_live

# # st.title("🏃 Real-Time Sports Injury Monitoring")

# # VIDEO_DIR = "data/sports_videos"

# # videos = [v for v in os.listdir(VIDEO_DIR) if v.endswith(".mp4")]

# # selected_video = st.selectbox("Select Sports Video", videos)

# # video_path = os.path.join(VIDEO_DIR, selected_video)

# # print(video_path)

# # st.video(video_path)

# # if st.button("▶ Start Live Monitoring"):
# #     cap = cv2.VideoCapture(video_path)
# #     fps = cap.get(cv2.CAP_PROP_FPS)
# #     st_frame = st.empty() # Placeholder for the video frames
    
# #     fall_counter = 0
# #     injury_detected = False

# #     while cap.isOpened():
# #         ret, frame = cap.read()
# #         if not ret:
# #             break

# #         # Process frame
# #         frame, fall_counter, injury_detected = detect_injury_live(frame, fall_counter, fps)
        
# #         # Convert BGR (OpenCV) to RGB (Streamlit)
# #         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #         st_frame.image(frame_rgb, channels="RGB", use_container_width=True)

# #         if injury_detected:
# #             st.error("🚨 INJURY DETECTED AT THIS MOMENT!")
# #             # Save your JSON logic here
# #             break
            
# #     cap.release()





# # import streamlit as st
# # import time
# # import random

# # st.title("⚽ Real-Time Sports Injury Monitoring")

# # st.warning("🔴 Live CV stream simulation (YOLO integration point)")

# # video_placeholder = st.empty()
# # alert_placeholder = st.empty()

# # st.markdown("### Live Match Feed")

# # for i in range(20):
# #     video_placeholder.image(
# #         "https://via.placeholder.com/800x400.png?text=Live+Sports+Feed",
# #         caption="Live Camera Stream"
# #     )

# #     injury_detected = random.choice([0, 0, 0, 1])

# #     if injury_detected:
# #         alert_placeholder.error("🚨 Injury Detected! Medical Team Alerted")
# #         st.balloons()
# #         break

# #     time.sleep(0.5)
