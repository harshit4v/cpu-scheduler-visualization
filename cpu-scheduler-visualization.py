# scheduler_visualization.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
import csv
from datetime import datetime
# Placeholder for imported scheduler algorithms and GUI (to be integrated later)
from scheduler_algorithms import *
from scheduler_gui import SchedulerGUI

class SchedulerVisualizer(SchedulerGUI):
    def __init__(self, root):
        super().__init__(root)
        # Add visualization buttons
        control_frame = self.root.winfo_children()[0].winfo_children()[2]  # Access control_frame
        buttons = [
            ("View Gantt Chart", self.view_gantt_chart, "View Gantt chart in a new window"),
            ("Start Animation", self.start_animation, "Start real-time animation in new window"),
            ("Stop Animation", self.stop_animation, "Stop real-time animation"),
            ("Compare All", self.compare_all, "Compare all algorithms' performance"),
            ("Export Results", self.export_results, "Export results to CSV")
        ]
        for text, cmd, tip in buttons:
            btn = ttk.Button(control_frame, text=text, command=cmd)
            btn.pack(side="left", padx=10)
            self.add_tooltip(btn, tip)
        
        self.canvas_widget = None
        self.anim_running = False
        self.anim = None
        self.gantt_window = None

    def view_gantt_chart(self):
        if not hasattr(self, 'timeline') or not self.timeline:
            messagebox.showwarning("Warning", "Run a simulation first!")
            return
        self.plot_gantt(self.current_processes, self.current_algo_name, self.timeline, animate=False)

    def start_animation(self):
        if not hasattr(self, 'timeline') or not self.timeline:
            messagebox.showwarning("Warning", "Run a simulation first!")
            return
        if self.anim_running:
            self.stop_animation()
        self.plot_gantt(self.current_processes, self.current_algo_name, self.timeline, animate=True)

    def stop_animation(self):
        if self.anim and self.anim_running:
            self.anim.event_source.stop()
            self.anim_running = False
            if self.gantt_window:
                self.gantt_window.destroy()
                self.gantt_window = None

    def compare_all(self):
        try:
            self.get_processes()
            quantum = int(self.quantum_var.get())
            algorithms = [
                fcfs_scheduler, sjf_non_preemptive, sjf_preemptive,
                lambda p: rr_scheduler(p, quantum), priority_non_preemptive, priority_preemptive
            ]
            results = {}
            for algo in algorithms:
                proc_copy = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in self.processes]
                proc_result, algo_name, _ = algo(proc_copy)
                avg_wait, _, cpu_util, throughput = calculate_metrics(proc_result)
                results[algo_name] = {'avg_wait': avg_wait, 'cpu_util': cpu_util, 'throughput': throughput}
            self.plot_comparison(results)
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def plot_gantt(self, processes, algo_name, timeline, animate=False):
        if self.gantt_window:
            self.gantt_window.destroy()
        
        self.gantt_window = tk.Toplevel(self.root)
        self.gantt_window.title(f"Gantt Chart - {algo_name}")
        self.gantt_window.geometry("1000x600")
        
        bg_color = "#2e2e2e" if self.current_theme == "equilux" else "#f0f8ff"
        text_color = "white" if self.current_theme == "equilux" else "#333333"
        fig, ax = plt.subplots(figsize=(14, 6), facecolor=bg_color)
        colors = plt.cm.Set3(np.linspace(0, 1, len(processes)))
        
        ax.set_ylim(0, 1.5)
        max_time = max(t[2] for t in timeline) + 1 if timeline else max(p.end_time for p in processes) + 1
        ax.set_xlim(0, max_time)
        ax.set_xlabel("Time (ms)", fontsize=16, color=text_color, fontweight='bold')
        ax.set_yticks([])
        ax.set_title(f"Gantt Chart - {algo_name}", fontsize=20, color=text_color, pad=30, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.5, color='gray')
        ax.set_facecolor("#3c3f41" if self.current_theme == "equilux" else "#e6f0ff")
        
        legend_elements = [plt.Line2D([0], [0], marker='s', color=colors[i], label=p.pid, 
                                     markersize=15, markerfacecolor=colors[i], markeredgecolor='black') 
                          for i, p in enumerate(processes)]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1.25), ncol=len(processes), 
                  frameon=True, fontsize=12, title="Processes", title_fontsize=14, 
                  facecolor=bg_color, edgecolor='white' if self.current_theme == "equilux" else 'black')

        if animate:
            self.anim_running = True
            
            def update(frame):
                ax.clear()
                ax.set_ylim(0, 1.5)
                ax.set_xlim(0, max_time)
                ax.set_xlabel("Time (ms)", fontsize=16, color=text_color, fontweight='bold')
                ax.set_yticks([])
                ax.set_title(f"Gantt Chart - {algo_name}", fontsize=20, color=text_color, pad=30, fontweight='bold')
                ax.grid(True, linestyle='--', alpha=0.5, color='gray')
                ax.set_facecolor("#3c3f41" if self.current_theme == "equilux" else "#e6f0ff")
                ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1.25), ncol=len(processes), 
                          frameon=True, fontsize=12, title="Processes", title_fontsize=14, 
                          facecolor=bg_color, edgecolor='white' if self.current_theme == "equilux" else 'black')
                
                for pid, start, end in timeline[:frame + 1]:
                    idx = [p.pid for p in processes].index(pid)
                    color = colors[idx]
                    ax.broken_barh([(start, end - start)], (0, 1), facecolors=color, edgecolors='black', linewidth=2, alpha=0.9)
                    ax.text(start + (end - start) / 2, 0.5, pid, ha='center', va='center', fontsize=14, color='white', fontweight='bold')

            self.anim = FuncAnimation(fig, update, frames=len(timeline), interval=500, repeat=False)
        else:
            for pid, start, end in timeline:
                idx = [p.pid for p in processes].index(pid)
                color = colors[idx]
                ax.broken_barh([(start, end - start)], (0, 1), facecolors=color, edgecolors='black', linewidth=2, alpha=0.9)
                ax.text(start + (end - start) / 2, 0.5, pid, ha='center', va='center', fontsize=14, color='white', fontweight='bold')

        plt.subplots_adjust(top=0.85)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.gantt_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_comparison(self, results):
        fig, ax = plt.subplots(figsize=(12, 6), facecolor="#f0f8ff")
        algos = list(results.keys())
        waits = [results[algo]['avg_wait'] for algo in algos]
        colors = plt.cm.Set3(np.linspace(0, 1, len(algos)))
        bars = ax.bar(algos, waits, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_ylabel("Average Waiting Time (ms)", fontsize=14, color="#333333")
        ax.set_title("Algorithm Performance Comparison", fontsize=16, color="#333333", pad=15)
        plt.xticks(rotation=45, ha="right", fontsize=12, color="#333333")
        plt.yticks(fontsize=12, color="#333333")
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', 
                    ha='center', va='bottom', fontsize=12, color='black', fontweight='bold')
        
        ax.grid(True, linestyle='--', alpha=0.3, color='gray')
        ax.set_facecolor("#f0f8ff")
        plt.tight_layout()
        plt.show()

    def export_results(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Run a simulation first!")
            return
        filename = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["PID", "Arrival", "Burst", "Priority", "Start", "End", "Waiting", "Turnaround"])
            for p in self.processes:
                writer.writerow([p.pid, p.arrival_time, p.burst_time, p.priority, p.start_time, p.end_time, p.waiting_time, p.turnaround_time])
        messagebox.showinfo("Success", f"Results exported to {filename}")

if __name__ == "__main__":
    root = ThemedTk(theme="radiance")
    app = SchedulerVisualizer(root)
    root.mainloop()
