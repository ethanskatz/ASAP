"""_summary_"""

import tkinter as tk
from tkinter import ttk


class MotorCameraGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Motor + Camera GUI")
        self.geometry("1200x720")
        self.minsize(1000, 650)

        # App state
        self.selected_units = tk.StringVar(value="mm")
        self.step_size = tk.StringVar(value="1.0")
        self.last_click_text = tk.StringVar(value="Last click: none")
        self.last_key_text = tk.StringVar(value="Last key: none")
        self.status_text = tk.StringVar(value="Ready")
        self.coord_x_var = tk.StringVar(value="")
        self.coord_y_var = tk.StringVar(value="")

        # Placeholder camera dimensions
        self.camera_width = 640
        self.camera_height = 480

        self._build_layout()
        self._bind_keys()
        self._draw_camera_placeholder()

    # -------------------------
    # UI Layout
    # -------------------------
    def _build_layout(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        left_frame = ttk.Frame(self, padding=10)
        right_frame = ttk.Frame(self, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")

        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(6, weight=1)

        # -------------------------
        # Camera panel (placeholder)
        # -------------------------
        self.camera_canvas = tk.Canvas(
            left_frame,
            width=self.camera_width,
            height=self.camera_height,
            bg="black",
            highlightthickness=1,
            highlightbackground="#666",
        )
        self.camera_canvas.grid(row=0, column=0, sticky="nsew")
        self.camera_canvas.bind("<Button-1>", self.on_camera_click)

        info_frame = ttk.Frame(left_frame)
        info_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        info_frame.columnconfigure(0, weight=1)

        ttk.Label(info_frame, textvariable=self.last_click_text).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(info_frame, textvariable=self.status_text).grid(
            row=1, column=0, sticky="w"
        )

        # -------------------------
        # Controls panel
        # -------------------------
        ttk.Label(
            right_frame,
            text="Motion Control",
            font=("TkDefaultFont", 16, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))

        # Units section
        units_frame = ttk.LabelFrame(right_frame, text="Units", padding=10)
        units_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        units_frame.columnconfigure(1, weight=1)

        ttk.Label(units_frame, text="Select units:").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        ttk.Combobox(
            units_frame,
            textvariable=self.selected_units,
            values=["nm", "mm", "cm", "um"],
            state="readonly",
            width=10,
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(units_frame, text="Step size:").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=(8, 0)
        )
        ttk.Entry(units_frame, textvariable=self.step_size, width=12).grid(
            row=1, column=1, sticky="w", pady=(8, 0)
        )

        # Action buttons
        action_frame = ttk.LabelFrame(right_frame, text="Actions", padding=10)
        action_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        action_frame.columnconfigure((0, 1), weight=1)

        ttk.Button(action_frame, text="Home", command=self.on_home).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(action_frame, text="Stop", command=self.on_stop).grid(
            row=0, column=1, sticky="ew"
        )

        # D-pad
        dpad_frame = ttk.LabelFrame(right_frame, text="D-Pad", padding=12)
        dpad_frame.grid(row=3, column=0, sticky="n", pady=(0, 10))

        for r in range(3):
            dpad_frame.rowconfigure(r, weight=1)
        for c in range(3):
            dpad_frame.columnconfigure(c, weight=1)

        ttk.Button(
            dpad_frame,
            text="↑",
            width=6,
            command=lambda: self.on_direction("Up"),
        ).grid(row=0, column=1, padx=4, pady=4)
        ttk.Button(
            dpad_frame,
            text="←",
            width=6,
            command=lambda: self.on_direction("Left"),
        ).grid(row=1, column=0, padx=4, pady=4)
        ttk.Button(
            dpad_frame,
            text="→",
            width=6,
            command=lambda: self.on_direction("Right"),
        ).grid(row=1, column=2, padx=4, pady=4)
        ttk.Button(
            dpad_frame,
            text="↓",
            width=6,
            command=lambda: self.on_direction("Down"),
        ).grid(row=2, column=1, padx=4, pady=4)

        ttk.Label(right_frame, textvariable=self.last_key_text).grid(
            row=4, column=0, sticky="w"
        )

        # Coordinate output
        coords_frame = ttk.LabelFrame(
            right_frame, text="Coordinate Output", padding=10
        )
        coords_frame.grid(row=5, column=0, sticky="ew", pady=(10, 10))
        coords_frame.columnconfigure(1, weight=1)

        ttk.Label(coords_frame, text="X:").grid(row=0, column=0, sticky="w")
        ttk.Entry(
            coords_frame,
            textvariable=self.coord_x_var,
            state="readonly",
            width=15,
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(coords_frame, text="Y:").grid(
            row=1, column=0, sticky="w", pady=(6, 0)
        )
        ttk.Entry(
            coords_frame,
            textvariable=self.coord_y_var,
            state="readonly",
            width=15,
        ).grid(row=1, column=1, sticky="w", pady=(6, 0))

        # Command log / event log
        log_frame = ttk.LabelFrame(right_frame, text="Event Log", padding=8)
        log_frame.grid(row=6, column=0, sticky="nsew", pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, height=10, wrap="word")
        self.log_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            log_frame, orient="vertical", command=self.log_text.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

    # -------------------------
    # Placeholder camera view
    # -------------------------
    def _draw_camera_placeholder(self):
        self.camera_canvas.delete("all")
        self.camera_canvas.create_rectangle(
            0,
            0,
            self.camera_width,
            self.camera_height,
            fill="#111",
            outline="",
        )
        self.camera_canvas.create_text(
            self.camera_width // 2,
            self.camera_height // 2 - 20,
            text="CAMERA FEED PLACEHOLDER",
            fill="white",
            font=("TkDefaultFont", 18, "bold"),
        )
        self.camera_canvas.create_text(
            self.camera_width // 2,
            self.camera_height // 2 + 15,
            text="Click anywhere to get coordinates",
            fill="#cccccc",
            font=("TkDefaultFont", 11),
        )

    # -------------------------
    # Input handling
    # -------------------------
    def _bind_keys(self):
        self.bind("<Up>", lambda event: self.on_arrow_key("Up"))
        self.bind("<Down>", lambda event: self.on_arrow_key("Down"))
        self.bind("<Left>", lambda event: self.on_arrow_key("Left"))
        self.bind("<Right>", lambda event: self.on_arrow_key("Right"))
        self.bind("<Home>", lambda event: self.on_home())
        self.focus_force()

    def on_camera_click(self, event):
        x, y = event.x, event.y
        self.coord_x_var.set(str(x))
        self.coord_y_var.set(str(y))
        self.last_click_text.set(f"Last click: ({x}, {y})")
        self.status_text.set(f"Camera clicked at ({x}, {y})")
        self.log(f"Camera click -> x={x}, y={y}")

        # Draw click marker
        self._draw_camera_placeholder()
        r = 4
        self.camera_canvas.create_oval(
            x - r, y - r, x + r, y + r, outline="red", width=2
        )

    def on_arrow_key(self, key_name):
        self.last_key_text.set(f"Last key: {key_name}")
        self.status_text.set(f"Arrow key pressed: {key_name}")
        self.log(f"Arrow key pressed -> {key_name}")

    def on_direction(self, direction):
        self.last_key_text.set(f"Last key: {direction}")
        self.status_text.set(f"D-pad pressed: {direction}")
        self.log(
            f"D-pad -> direction={direction}, step={self.step_size.get()}, units={self.selected_units.get()}",
        )

    def on_home(self):
        self.last_key_text.set("Last key: Home")
        self.status_text.set("Home pressed")
        self.log("Home button pressed")

    def on_stop(self):
        self.status_text.set("Stop pressed")
        self.log("Stop button pressed")

    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")


if __name__ == "__main__":
    app = MotorCameraGUI()
    app.mainloop()
