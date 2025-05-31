# 🚁 Drone Fleet Optimization
An intelligent delivery system using autonomous drones to perform optimized routing under constraints like limited battery, payload weight, no-fly zones, and time windows.

---

## 📌 Project Overview

This project was developed for the course *TBL331: Software Development Lab II*  
**Kocaeli University – Information Systems Engineering – Spring 2025**

### Goal:
To design and implement an adaptive algorithm that dynamically assigns delivery routes to a fleet of drones operating under environmental and operational constraints.

---

## ⚙️ Tech Stack

- **Language**: Python 3.10+
- **Libraries**: 
  - `matplotlib` – for route visualization  
  - `shapely` – for no-fly zone geometric intersection detection  
  - `heapq` – for A* priority queue  
  - `random`, `copy`, `datetime`

---

## 📁 Folder Structure

```
drone-fleet-opt/
│
├── main.py                   # Entry point of the system
├── requirements.txt          # Required Python packages
├── README.md                 # You're reading it
│
├── src/
│   ├── models/               # Drone, Delivery, NoFlyZone classes
│   ├── algorithms/           # A*, CSP, Genetic algorithm
│   └── utils/                # Graph, data generator, visualizer
│
├── data/                     # Optional: JSON test datasets
├── tests/                    # Unit test files
└── visualization/            # Output delivery maps
```

---

## 🚀 How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Execute:
```bash
python main.py
```

3. The program will:
- Generate a random fleet of drones, deliveries, and no-fly zones  
- Build a graph of possible paths  
- Run a genetic algorithm with A* and CSP integrated  
- Display an optimized route map avoiding active no-fly zones  

---

## 📊 Algorithms Used

- **A\***: Finds the shortest path between a drone and delivery using cost = distance + weight penalty  
- **CSP**: Ensures no-fly zone avoidance, time window compliance, and capacity constraints  
- **Genetic Algorithm**: Optimizes drone-to-delivery assignments over generations

---

## 🛑 No-Fly Zone Detection

- All no-fly zones are modeled as polygons  
- If a drone's route intersects any active zone, it is marked as invalid using `shapely.geometry.LineString.intersects`

---

## 🖼️ Sample Output

![Map](visualization/sample_map.png)

---

## 📚 Academic Notes

- Developed for: **TBL331 - Project II**  
- Submission Deadline: June 2, 2025  
- Presentation: June 16–27, 2025

---

## ✅ Author

**Name:** [Your Name]  
**Student ID:** [Your ID]  
**Email:** [Your Email]  
**Course Instructor:** Öğr. Gör. [Instructor Name]