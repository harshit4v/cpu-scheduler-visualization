# CPU Scheduler Visualizer (Tkinter GUI)

## Overview
This project provides a graphical user interface (GUI) for simulating and visualizing CPU scheduling algorithms using Tkinter. The application includes features such as Gantt chart visualization, real-time animations, and algorithm performance comparisons.

## Features
- **Graphical Process Input:** Users can enter process details dynamically.
- **Supported Scheduling Algorithms:**
  - First Come First Serve (FCFS)
  - Shortest Job First (SJF) - Non-Preemptive & Preemptive
  - Round Robin (RR) with customizable time quantum
  - Priority Scheduling - Non-Preemptive & Preemptive
- **Visualization Tools:**
  - Static Gantt Chart for schedule visualization.
  - Animated Gantt Chart for step-by-step execution.
  - Performance comparison across all algorithms.
- **Performance Metrics Display:**
  - Average Waiting Time
  - Average Turnaround Time
  - CPU Utilization
  - Throughput
- **Export Results:** Save scheduling results as a CSV file.
- **UI Customization:** Change themes for better visibility.

## Installation
### Prerequisites
- Python 3.x
- Required Python packages:
  ```sh
  pip install tkinter ttkthemes matplotlib pandas numpy mplcursors
  ```

## Usage
1. Run the application:
   ```sh
   python scheduler_visualizer.py
   ```
2. Enter process details (Process ID, Arrival Time, Burst Time, Priority).
3. Select a scheduling algorithm.
4. (Optional) Set the time quantum for Round Robin.
5. Click `Run Simulation` to execute the algorithm.
6. Use visualization tools:
   - `View Gantt Chart` for a static view.
   - `Start Animation` for real-time execution.
   - `Compare All` to analyze performance across algorithms.
7. Export results using `Export Results`.
8. Reset input fields if needed.
9. Change UI theme via the settings.

## File Structure
- `scheduler_visualizer.py` - Main GUI and visualization logic.
- `scheduler_algorithms.py` - CPU scheduling algorithm implementations.
- `config.py` - Configuration settings.

## Shortcuts
- `Ctrl + R`: Run simulation.
- `Ctrl + G`: Display Gantt chart.
- `Ctrl + A`: Start animation.
- `Ctrl + C`: Compare all algorithms.

## Notes
- Ensure valid inputs: Arrival time ≥ 0, Burst time > 0.
- Animated Gantt charts provide a stepwise execution overview.
- The comparison tool helps analyze scheduling efficiency.

