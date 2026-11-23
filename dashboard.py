import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


BG = "#08111f"
PANEL = "#111d30"
PANEL2 = "#14233a"
TEXT = "#f2f6fb"
MUTED = "#8fa4bf"
CYAN = "#25aef5"
GREEN = "#18d36b"
PINK = "#ff6680"
PURPLE = "#9b7cff"


class Dashboard:
    def __init__(self, root, app):
        self.root = root
        self.app = app

        root.configure(bg=BG)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TButton",
            font=("Segoe UI", 12, "bold"),
            padding=(14, 9),
            background="#172944",
            foreground=TEXT,
            borderwidth=0
        )
        style.map("TButton", background=[("active", "#213858")])

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", padx=24, pady=(18, 10))

        tk.Label(header, text="rPPG",
                 font=("Segoe UI", 31, "bold"),
                 fg=CYAN, bg=BG).pack(side="left")

        tk.Label(header, text="VITAL SIGNS MONITOR",
                 font=("Segoe UI", 26, "bold"),
                 fg=TEXT, bg=BG).pack(side="left", padx=10)

        tk.Label(header, text="Accuracy-focused signal processing",
                 font=("Segoe UI", 10),
                 fg=MUTED, bg=BG).pack(side="left", padx=8, pady=(12, 0))

        self.live_label = tk.Label(
            header, text="● READY",
            font=("Segoe UI", 12, "bold"),
            fg=MUTED, bg=BG
        )
        self.live_label.pack(side="right", padx=10)

        ttk.Button(header, text="▶ Start Monitoring",
                   command=app.start).pack(side="right", padx=5)
        ttk.Button(header, text="■ Stop",
                   command=app.stop).pack(side="right", padx=5)

        settings = tk.Frame(root, bg=PANEL, highlightthickness=1,
                            highlightbackground="#315070")
        settings.pack(fill="x", padx=24, pady=(0, 16))

        tk.Label(settings, text="SIGNAL SETTINGS",
                 font=("Segoe UI", 12, "bold"),
                 fg=MUTED, bg=PANEL).pack(side="left", padx=16, pady=11)

        for text in ["Low Hz   0.70", "High Hz   3.00", "Window   12 s",
                     "Method   POS"]:
            tk.Label(settings, text=text,
                     font=("Segoe UI", 10, "bold"),
                     fg=TEXT, bg=PANEL2,
                     padx=14, pady=7).pack(side="left", padx=4, pady=5)

        tk.Label(settings, text="Natural-color camera • No visual color filter",
                 font=("Segoe UI", 10),
                 fg=GREEN, bg=PANEL).pack(side="right", padx=16)

        body = tk.Frame(root, bg=BG)
        body.pack(fill="both", expand=True, padx=24)

        camera_panel = tk.Frame(body, bg=PANEL,
                                highlightthickness=1,
                                highlightbackground="#315070")
        camera_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        cam_head = tk.Frame(camera_panel, bg=PANEL)
        cam_head.pack(fill="x", padx=14, pady=(10, 4))

        tk.Label(cam_head, text="LIVE CAMERA",
                 font=("Segoe UI", 12, "bold"),
                 fg=TEXT, bg=PANEL).pack(side="left")

        self.cam_status = tk.Label(cam_head, text="Camera inactive",
                                   font=("Segoe UI", 10, "bold"),
                                   fg=MUTED, bg=PANEL)
        self.cam_status.pack(side="right")

        self.camera = tk.Label(camera_panel, bg="#020711")
        self.camera.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        side = tk.Frame(body, bg=BG, width=340)
        side.pack(side="right", fill="y")
        side.pack_propagate(False)

        self.hr_card = self.card(side, "HEART RATE", "—", "BPM", PINK)
        self.hrv_card = self.card(side, "HEART RATE VARIABILITY", "—", "ms · RMSSD", PURPLE)
        self.conf_card = self.card(side, "ESTIMATION CONFIDENCE", "—", "%", CYAN)
        self.stress_card = self.card(side, "STRESS INDICATOR", "Waiting", "", GREEN)

        details = tk.Frame(side, bg=PANEL, highlightthickness=1,
                           highlightbackground="#315070")
        details.pack(fill="x", pady=6)

        tk.Label(details, text="ESTIMATOR DETAILS",
                 font=("Segoe UI", 12, "bold"),
                 fg=TEXT, bg=PANEL).pack(anchor="w", padx=16, pady=(12, 7))

        self.details = tk.Label(
            details,
            text="FFT HR: — BPM\nPeak HR: — BPM\n\nWaiting for a clean pulse signal...",
            justify="left",
            font=("Consolas", 10, "bold"),
            fg=MUTED, bg=PANEL
        )
        self.details.pack(anchor="w", padx=16, pady=(0, 14))

        ttk.Button(side, text="Save Session",
                   command=app.save_session).pack(fill="x", pady=(8, 0))

        trends = tk.Frame(root, bg=BG)
        trends.pack(fill="both", expand=True, padx=24, pady=(15, 18))

        tk.Label(trends, text="LIVE VITAL TRENDS",
                 font=("Segoe UI", 12, "bold"),
                 fg=TEXT, bg=BG).pack(anchor="w", pady=(0, 7))

        charts = tk.Frame(trends, bg=BG)
        charts.pack(fill="both", expand=True)

        self.fig_hr = Figure(figsize=(6, 2.1), dpi=100)
        self.ax_hr = self.fig_hr.add_subplot(111)
        self.setup_axis(self.ax_hr, "Heart Rate", "BPM")
        self.canvas_hr = FigureCanvasTkAgg(self.fig_hr, charts)
        self.canvas_hr.get_tk_widget().pack(side="left", fill="both",
                                            expand=True, padx=(0, 7))

        self.fig_hrv = Figure(figsize=(6, 2.1), dpi=100)
        self.ax_hrv = self.fig_hrv.add_subplot(111)
        self.setup_axis(self.ax_hrv, "HRV (RMSSD)", "ms")
        self.canvas_hrv = FigureCanvasTkAgg(self.fig_hrv, charts)
        self.canvas_hrv.get_tk_widget().pack(side="left", fill="both",
                                             expand=True, padx=(7, 0))

    def card(self, parent, title, value, unit, accent):
        outer = tk.Frame(parent, bg=PANEL, highlightthickness=1,
                         highlightbackground="#315070")
        outer.pack(fill="x", pady=4)

        bar = tk.Frame(outer, bg=accent, width=5)
        bar.pack(side="left", fill="y")

        content = tk.Frame(outer, bg=PANEL)
        content.pack(fill="both", expand=True, padx=14, pady=7)

        tk.Label(content, text=title,
                 font=("Segoe UI", 10, "bold"),
                 fg=MUTED, bg=PANEL).pack(anchor="w")

        row = tk.Frame(content, bg=PANEL)
        row.pack(anchor="w", pady=(4, 0))

        value_font = ("Segoe UI", 27, "bold") if title == "STRESS INDICATOR" else ("Segoe UI", 31, "bold")
        value_label = tk.Label(row, text=value,
                               font=value_font,
                               fg=TEXT, bg=PANEL)
        value_label.pack(side="left")

        unit_label = tk.Label(row, text=("  " + unit if unit else ""),
                              font=("Segoe UI", 10, "bold"),
                              fg=MUTED, bg=PANEL)
        unit_label.pack(side="left", pady=(10, 0))

        return value_label

    def setup_axis(self, ax, title, ylabel):
        ax.set_facecolor(PANEL)
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold",
                     color=TEXT, pad=8)
        ax.set_ylabel(ylabel, color=MUTED, fontsize=8)
        ax.tick_params(colors=MUTED, labelsize=7)
        for spine in ax.spines.values():
            spine.set_color("#263955")
        ax.grid(True, alpha=0.15)

    def update_camera(self, bgr_frame):
        # IMPORTANT: BGR -> RGB exactly once for PIL.
        # This keeps the preview natural instead of blue.
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)

        w = max(500, self.camera.winfo_width() - 24)
        h = max(300, self.camera.winfo_height() - 24)
        image.thumbnail((w, h), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(image)
        self.camera.configure(image=photo, text="")
        self.camera.image = photo

    def update_data(self, bpm, hrv, confidence, stress,
                    times, values, hr_history, hrv_history, fft_bpm=0.0, peak_bpm=0.0):
        self.hr_card.configure(text=f"{bpm:.1f}" if bpm > 0 else "—")
        self.hrv_card.configure(text=f"{hrv:.1f}" if hrv > 0 else "—")
        self.conf_card.configure(text=f"{confidence * 100:.0f}" if bpm > 0 else "—")
        self.stress_card.configure(text=stress)

        if bpm > 0:
            self.details.configure(
                text=f"FFT HR:  {fft_bpm:.1f} BPM\n"
                     f"Peak HR: {peak_bpm:.1f} BPM\n\n"
                     f"Signal quality: {confidence*100:.0f}%"
            )

        # HR trend.
        self.ax_hr.clear()
        self.setup_axis(self.ax_hr, "Heart Rate", "BPM")
        if hr_history:
            n = min(len(hr_history), 60)
            y = np.asarray(hr_history[-n:])
            x = np.arange(-n + 1, 1)
            self.ax_hr.plot(x, y, linewidth=2.8)
            self.ax_hr.set_ylim(
                max(35, float(np.min(y)) - 10),
                min(180, float(np.max(y)) + 10)
            )
        self.canvas_hr.draw_idle()

        # HRV trend.
        self.ax_hrv.clear()
        self.setup_axis(self.ax_hrv, "HRV (RMSSD)", "ms")
        if hrv_history:
            n = min(len(hrv_history), 60)
            y = np.asarray(hrv_history[-n:])
            x = np.arange(-n + 1, 1)
            self.ax_hrv.plot(x, y, linewidth=2.8)
            ymax = max(100, float(np.max(y)) * 1.15)
            self.ax_hrv.set_ylim(0, ymax)
        self.canvas_hrv.draw_idle()

    def set_live(self, live):
        if live:
            self.live_label.configure(text="● LIVE", fg=GREEN)
            self.cam_status.configure(text="Camera active", fg=GREEN)
        else:
            self.live_label.configure(text="● READY", fg=MUTED)
            self.cam_status.configure(text="Camera inactive", fg=MUTED)
