# cpu_scheduler_visualization.py
# Handles the visualization of the Gantt chart with live animation for the CPU Scheduler Simulator.

import tkinter as tk
from ttkbootstrap import Window, Frame, Label, Button, Scrollbar

class SchedulerVisualizer:
    def __init__(self):
        self.root = Window(themename="darkly")
        self.root.title("Gantt Chart - CPU Scheduler Simulator")
        self.root.geometry("1000x500")
        self.is_playing = False
        self.current_index = 0
        self.animation_speed = 500
        self.after_ids = []  # Track scheduled after tasks

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Cancel all scheduled tasks
        for after_id in self.after_ids:
            self.root.after_cancel(after_id)
        self.root.destroy()

    def display_gantt_chart(self, algo_name, processes, timeline):
        frame = Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text=f"Gantt Chart - Algorithm: {algo_name}", font=("Segoe UI", 16, "bold"), bootstyle="primary").pack(anchor="w", pady=10)

        # Legend
        legend_frame = Frame(frame)
        legend_frame.pack(fill="x", pady=10)
        Label(legend_frame, text="Legend:", font=("Segoe UI", 12, "bold")).pack(side="left")
        self.colors = ["#00D4FF", "#FF2E63", "#AB47BC", "#FFCA28", "#66BB6A"]
        self.process_colors = {}
        color_index = 0
        for p in processes:
            if p.pid not in self.process_colors:
                self.process_colors[p.pid] = self.colors[color_index % len(self.colors)]
                color_index += 1
                Label(legend_frame, text=p.pid, background=self.process_colors[p.pid], relief="solid", width=5).pack(side="left", padx=5)
                Label(legend_frame, text=f" {p.pid} ").pack(side="left")

        # Canvas for Gantt chart
        canvas_frame = Frame(frame)
        canvas_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(canvas_frame, height=150, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, pady=10)

        scrollbar = Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview, bootstyle="round")
        scrollbar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=scrollbar.set)

        # Control buttons
        control_frame = Frame(frame)
        control_frame.pack(fill="x", pady=10)
        self.play_pause_btn = Button(control_frame, text="Play", command=self.toggle_animation, bootstyle="primary")
        self.play_pause_btn.pack(side="left", padx=10)

        # Initialize animation data
        self.timeline = timeline
        self.total_time = max(end for _, _, end in timeline) if timeline else 1
        canvas_width = max(1000, self.total_time * 50)
        self.canvas.configure(scrollregion=(0, 0, canvas_width, 150))
        self.unit_width = canvas_width / self.total_time
        self.y_top = 40
        self.y_bottom = 100

        # Draw time markers
        for t in range(self.total_time + 1):
            x = t * self.unit_width
            self.canvas.create_line(x, self.y_bottom, x, self.y_bottom + 10)
            self.canvas.create_text(x, self.y_bottom + 25, text=str(t), anchor="n", font=("Segoe UI", 8))

        # Start animation
        if self.timeline:
            self.is_playing = True
            self.play_pause_btn.config(text="Pause")
            self.animate_gantt()

    def toggle_animation(self):
        self.is_playing = not self.is_playing
        self.play_pause_btn.config(text="Pause" if self.is_playing else "Play")
        if self.is_playing:
            self.animate_gantt()

    def animate_gantt(self):
        if not self.is_playing or self.current_index >= len(self.timeline):
            self.is_playing = False
            self.play_pause_btn.config(text="Play")
            self.current_index = 0
            return

        # Check if the window still exists
        if not self.root.winfo_exists():
            return

        pid, start, end = self.timeline[self.current_index]
        x_start = start * self.unit_width
        x_end = end * self.unit_width
        block = self.canvas.create_rectangle(x_start, self.y_top, x_start, self.y_bottom, fill=self.process_colors.get(pid.split()[0], "#00D4FF"))
        text = self.canvas.create_text((x_start + x_end) / 2, (self.y_top + self.y_bottom) / 2, text=pid, font=("Segoe UI", 10))

        steps = 20
        step_size = (x_end - x_start) / steps
        def grow(step=0):
            if not self.root.winfo_exists():  # Stop if window is closed
                return
            if step >= steps or not self.is_playing:
                self.canvas.coords(block, x_start, self.y_top, x_end, self.y_bottom)
                self.current_index += 1
                after_id = self.root.after(500, self.animate_gantt)
                self.after_ids.append(after_id)
                return
            new_x_end = x_start + step_size * (step + 1)
            self.canvas.coords(block, x_start, self.y_top, new_x_end, self.y_bottom)
            self.canvas.coords(text, (x_start + new_x_end) / 2, (self.y_top + self.y_bottom) / 2)
            after_id = self.root.after(50, grow, step + 1)
            self.after_ids.append(after_id)

        after_id = self.root.after(0, grow)
        self.after_ids.append(after_id)
