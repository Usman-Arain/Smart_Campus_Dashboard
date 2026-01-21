from ultralytics import YOLO
import cv2
import time
import json
import os
from datetime import datetime

model = YOLO("yolov8n.pt")

# Track if we are already alerted for the current fall
is_currently_alerted = False 

def detect_injury_live(frame, fall_counter, fps):
    global is_currently_alerted
    results = model(frame, classes=[0], verbose=False)
    found_down = False
    limit = 1.5 * fps 

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            ratio = w / h if h > 0 else 0

            if ratio > 1.1:
                found_down = True
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "Fall Detected", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    if found_down:
        fall_counter += 1
    else:
        fall_counter = max(0, fall_counter - 2)
        if fall_counter == 0:
            is_currently_alerted = False

    # Trigger alert logic
    if fall_counter >= limit and not is_currently_alerted:
        is_currently_alerted = True 
        
        alert_file = "outputs/live_injury.json"
        os.makedirs("outputs", exist_ok=True)
        
        # 1. Create the new alert entry
        new_event = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "event": "POTENTIAL_INJURY",
            "status": "Critical"
        }

        # 2. LOAD EXISTING ALERTS (Appending logic)
        alerts = []
        if os.path.exists(alert_file):
            try:
                with open(alert_file, "r") as f:
                    alerts = json.load(f)
                    if not isinstance(alerts, list): # Ensure it's a list
                        alerts = []
            except (json.JSONDecodeError, IOError):
                alerts = []

        # 3. Add new event and Save
        alerts.append(new_event)
        with open(alert_file, "w") as f:
            json.dump(alerts, f, indent=4)
            
        return frame, fall_counter, True 

    return frame, fall_counter, False


# def detect_injury_live(frame, fall_counter, fps):
#     results = model(frame, classes=[0], verbose=False)
#     found_down = False
    
#     # 3 seconds threshold
#     limit = 3 * fps

#     for r in results:
#         for box in r.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             w, h = x2 - x1, y2 - y1
#             aspect_ratio = w / h if h > 0 else 0
            
#             # Print to console for debugging
#             print(f"Ratio: {aspect_ratio:.2f} | W: {w} H: {h}")

#             color = (0, 255, 0) # Green
#             label = "Player"

#             # Detection Logic
#             if aspect_ratio > 1.2: 
#                 found_down = True
#                 color = (0, 0, 255) # Red
#                 label = "FALL DETECTED"

#             cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#             cv2.putText(frame, label, (x1, y1 - 10), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#     if found_down:
#         fall_counter += 1
#     else:
#         fall_counter = max(0, fall_counter - 1)

#     injury_triggered = fall_counter >= limit

#     if injury_triggered:
#         # ONLY write the file if it doesn't already exist
#         # This prevents the file-lock error you are seeing
#         alert_file = "outputs/live_injury.json"
#         if not os.path.exists(alert_file):
#             event = {
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 "event": "POTENTIAL_INJURY",
#                 "status": "Critical"
#             }
#             os.makedirs("outputs", exist_ok=True)
#             with open(alert_file, "w") as f:
#                 json.dump(event, f)

#     return frame, fall_counter, injury_triggered



# from ultralytics import YOLO
# import cv2
# import numpy as np
# import time
# import json
# from datetime import datetime

# # Load YOLOv8 model (person detection)
# model = YOLO("yolov8n.pt")

# INJURY_THRESHOLD_TIME = 3  # seconds lying on ground

# def detect_injury_live(frame, fall_counter, fps):
#     results = model(frame, classes=[0], verbose=False)
#     found_down = False
    
#     # REQUIRED_FRAMES for 3 seconds
#     limit = 3 * fps

#     for r in results:
#         for box in r.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             w, h = x2 - x1, y2 - y1
#             aspect_ratio = w / h if h > 0 else 0
            
#             # --- DEBUG PRINT (Check your Terminal) ---
#             print(f"Detected Person - Width: {w}, Height: {h}, Ratio: {aspect_ratio:.2f}")

#             # Draw default box (Green)
#             color = (0, 255, 0) 
#             label = "Person"

#             if aspect_ratio > 1.2:
#                 found_down = True
#                 color = (0, 0, 255) # Red for potential fall
#                 label = "Check Player!"

#             # Draw on frame
#             cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#             cv2.putText(frame, f"{label} {aspect_ratio:.1f}", (x1, y1 - 10), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#     if found_down:
#         fall_counter += 1
#     else:
#         fall_counter = max(0, fall_counter - 1)

#     injury_triggered = fall_counter >= limit
#     return frame, fall_counter, injury_triggered

    
# def detect_injury(video_path):
# cap = cv2.VideoCapture(video_path)
#     fps = cap.get(cv2.CAP_PROP_FPS) # Get actual video FPS
#     if fps == 0: fps = 30 # Fallback
    
#     fall_frames_counter = 0 
#     # 3 seconds * FPS = total frames needed to confirm injury
#     REQUIRED_FRAMES = INJURY_THRESHOLD_TIME * fps
#     injury_detected = False

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret: break

#         results = model(frame, classes=[0], verbose=False)
        
#         found_person_down_this_frame = False
        
#         for r in results:
#             for box in r.boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 h = y2 - y1
#                 w = x2 - x1
                
#                 aspect_ratio = w / h if h > 0 else 0
                
#                 # Lowered aspect ratio to 1.2 for better sensitivity 
#                 # (A person lying down isn't always perfectly flat to the camera)
#                 if aspect_ratio > 1.2: 
#                     found_person_down_this_frame = True
#                     break # We found one, that's enough for this frame

#         if found_person_down_this_frame:
#             fall_frames_counter += 1
#         else:
#             # Don't reset to 0 immediately (handles flickering/occlusion)
#             fall_frames_counter = max(0, fall_frames_counter - 5)

#         if fall_frames_counter >= REQUIRED_FRAMES:
#             injury_detected = True
#             break

#     cap.release()

#     if injury_detected:
#         event = {
#             "timestamp": datetime.now().isoformat(),
#             "video": video_path,
#             "event": "POTENTIAL_INJURY"
#         }
#         with open("outputs/live_injury.json", "w") as f:
#             json.dump(event, f)

#         return True

#     return False





# # import cv2
# # import pandas as pd
# # from ultralytics import YOLO
# # import os

# # # ---------- Load sports video dataset ----------
# # sports_videos = pd.read_csv("data/raw/sports_videos.csv")  # contains columns: event_id, video_path
# # # sports_videos = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/sports_videos.csv'))

# # # ---------- Load a pretrained YOLO model ----------
# # # Using a generic pose model for detecting falls/injuries
# # model = YOLO("yolov8n-pose.pt")  # ultralytics small pose model

# # # ---------- Injury Detection ----------
# # def detect_injuries(video_path):
# #     """
# #     Detect injuries in sports videos using YOLO pose model.
# #     Returns number of suspected injuries.
# #     """
# #     if not os.path.exists(video_path):
# #         return 0
    
# #     results = model.predict(source=video_path, stream=False)
    
# #     # Count frames with potential injury/fall
# #     injury_count = 0
# #     for r in results:
# #         # r.keypoints shape: [num_people, 17, 3] (x, y, confidence)
# #         if r.keypoints is not None:
# #             for person in r.keypoints:
# #                 # Simple heuristic: if head is very low (y > threshold), count as fall
# #                 head_y = person[0][1]  # nose keypoint y
# #                 if head_y > 400:  # adjust threshold based on video size
# #                     injury_count += 1
# #     return injury_count

# # # ---------- Participation Tracker ----------
# # def update_participation_logs(event_id):
# #     """
# #     Update attendance based on video and detect injuries.
# #     """
# #     video_row = sports_videos[sports_videos['event_id'] == event_id]
# #     if video_row.empty:
# #         return 0, []
    
# #     video_path = video_row.iloc[0]['video_path']
    
# #     injuries = detect_injuries(video_path)
    
# #     # For simplicity, assume all players in video are counted as participated
# #     # Here we simulate by marking student IDs 1-10 as participants
# #     participants = list(range(1, 11))
    
# #     return injuries, participants

# # # ---------- Test run ----------
# # if __name__ == "__main__":
# #     for eid in sports_videos['event_id'].tolist():
# #         injuries, participants = update_participation_logs(eid)
# #         print(f"Event {eid} -> Injuries: {injuries}, Participants: {participants}")

