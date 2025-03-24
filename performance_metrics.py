# performance_metrics.py
# Visualizes performance metrics using Matplotlib.

import tkinter as tk
from ttkbootstrap import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PerformanceMetrics:
    def __init__(self, processes, parent):
        self.processes = processes
        self.parent = parent
        self.plot_metrics()

    def plot_metrics(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Waiting and Turnaround Times
        pids = [p.pid for p in self.processes]
        waiting_times = [p.waiting_time for p in self.processes]
        turnaround_times = [p.turnaround_time for p in self.processes]

        ax1.bar([i - 0.2 for i in range(len(pids))], waiting_times, 0.4, label="Waiting Time", color="#00D4FF")
        ax1.bar([i + 0.2 for i in range(len(pids))], turnaround_times, 0.4, label="Turnaround Time", color="#FF2E63")
        ax1.set_xticks(range(len(pids)))
        ax1.set_xticklabels(pids)
        ax1.set_title("Waiting and Turnaround Times")
        ax1.legend()

        # CPU Utilization and Throughput
        avg_wait, avg_turn, cpu_util, throughput = calculate_metrics(self.processes)
        ax2.bar(["CPU Utilization", "Throughput"], [cpu_util, throughput * 100], color=["#00D4FF", "#FF2E63"])
        ax2.set_title("CPU Utilization and Throughput")

        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
