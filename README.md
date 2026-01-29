# 🏫 IU Smart Campus: AI Admin & Recommender System

A centralized administrative ecosystem for smart campus management. This system integrates **AI-driven event scheduling**, **skill-based volunteer matching**, and **real-time field safety monitoring** using computer vision.

---

## 🏗 System Architecture

---

## 🌟 Key Features

### 1. AI Conflict-Free Scheduler

* **Greedy Interval Scheduling:** Automatically generates a sports timetable that ensures no two matches overlap in the same venue.
* **Pure Recommender Engine:** Scores events based on student interests and historical popularity.

### 2. Live Field Monitoring (Vision HUD)

* **Real-Time Safety Alerts:** Integrated with a YOLO-based injury detection model.
* **Live Emergency HUD:** Immediate red-box alerts for campus security whenever a fall or injury is detected on the sports field via the `live_injury.json` feed.

### 3. Dynamic Participation Tracking

* **Live Attendance Joins:** Real-time synchronization with `attendance.csv`. As students check in, the dashboard reflects live crowd density.
* **Skill-Based Context:** Provides administrators with a view of volunteers matched by their specific expertise (e.g., First Aid, Tech Support) and performance ratings.

### 4. Minimalist Analytics

* **Attendance Heatmaps:** Visualizes student engagement patterns across various event IDs.
* **Resource Distribution:** Monitors the balance of cultural vs. sports events to ensure a diverse campus life.

---

## 📂 Project Structure

```text
D:/Projects/Smart_Campus_Dashboard/
├── app/
│   └── Admin_Dashboard.py      # Streamlit UI & Data Orchestration
├── models/
│   ├── recommender/
│   │   └── recommender_hybrid.py # Scheduling & Scoring Logic
│   └── sports/
│       └── injury_detection.py  # Computer Vision Logic (YOLO)
├── data/
│   ├── students.csv            # Student Profiles & Interests
│   ├── attendance.csv          # Real-time Check-in Logs
│   └── volunteers.csv          # Pool of Available Staff/Skills
├── outputs/
│   ├── upcoming_timetable.csv  # AI-Generated Schedule
│   └── live_injury.json        # Live Vision Alert Feed
└── README.md

```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* A virtual environment (`env/`)

### Installation & Setup

1. **Navigate to the project root:**
```bash
cd D:/Projects/Smart_Campus_Dashboard

```


2. **Install dependencies:**
```bash
pip install streamlit pandas matplotlib seaborn st-aggrid

```


3. **Launch the Admin Dashboard:**
```bash
python -m streamlit run app/Admin_Dashboard.py

```



---

## 🛠 Tech Stack

* **Frontend:** [Streamlit](https://www.google.com/search?q=https://streamlit.io/)
* **Data Processing:** [Pandas](https://www.google.com/search?q=https://pandas.pydata.org/) & [NumPy](https://www.google.com/search?q=https://numpy.org/)
* **Visualization:** [Seaborn](https://www.google.com/search?q=https://seaborn.pydata.org/) & [Matplotlib](https://www.google.com/search?q=https://matplotlib.org/)
* **UI Components:** [Streamlit AgGrid](https://www.google.com/search?q=https://pypi.org/project/streamlit-aggrid/)
* **AI Engine:** Greedy Interval Scheduling & YOLOv8 (Inference)

---

## 👨‍💻 Module 7 Contribution

This project fulfills the requirements for **Module 7: Advanced AI Integration** by demonstrating:

1. **AI Recommender System** with complex constraints (Scheduling).
2. **Live Vision Data Integration** (Injury alerts).
3. **Dynamic Resource Allocation** (Skill-based volunteer management).
