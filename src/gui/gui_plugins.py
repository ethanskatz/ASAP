import tkinter as tk
from tkinter import ttk
from typing import Literal

STEP_UNITS: dict[str, list[str]] = {
    "linear": ["cm", "mm", "um", "nm"],
    "angular": ["deg", "rad"],
}

SPEED_UNITS: dict[str, list[str]] = {
    "linear": ["cm/s", "mm/s", "um/s", "nm/s"],
    "angular": ["deg/s", "rad/s"],
}


class MotorControlWidget(ttk.Frame):
    def __init__(
        self,
        master,
        motor,
        text: str,
        motion_type: Literal["linear", "angular"],
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)

        self.label: ttk.Label = ttk.Label(self, text=text)
        self.label.grid(row=0, column=0, padx=20)

        if motion_type == "linear":
            self.up_button: ttk.Button = ttk.Button(self, text="↑")
            self.down_button: ttk.Button = ttk.Button(self, text="↓")

        elif motion_type == "angular":
            self.up_button = ttk.Button(self, text="↪")
            self.down_button = ttk.Button(self, text="↩")

        self.up_button.grid(row=0, column=1)
        self.down_button.grid(row=0, column=2)

        step_label: ttk.Label = ttk.Label(self, text="Step")
        step_label.grid(row=0, column=3)

        # Step Size Entry
        self.step_var = tk.StringVar(value="1.0")
        self.step_entry = ttk.Entry(self, textvariable=self.step_var, width=5)
        self.step_entry.grid(row=0, column=4)

        # Step Units Dropdown
        self.step_unit_var = tk.StringVar(value=STEP_UNITS[motion_type][0])
        self.step_unit_menu = ttk.OptionMenu(
            self,
            self.step_unit_var,
            STEP_UNITS[motion_type][0],
            *STEP_UNITS[motion_type],
        )
        self.step_unit_menu.grid(row=0, column=5, padx=2)

        speed_label: ttk.Label = ttk.Label(self, text="Speed")
        speed_label.grid(row=0, column=6)
        # Speed Entry
        self.speed_var = tk.StringVar(value="10.0")
        self.speed_entry = ttk.Entry(self, textvariable=self.speed_var, width=5)
        self.speed_entry.grid(row=0, column=7, padx=(10, 2))

        # Speed Units Dropdown
        self.speed_unit_var = tk.StringVar(value=SPEED_UNITS[motion_type][0])
        self.speed_unit_menu = ttk.OptionMenu(
            self,
            self.speed_unit_var,
            SPEED_UNITS[motion_type][0],
            *SPEED_UNITS[motion_type],
        )
        self.speed_unit_menu.grid(row=0, column=8, padx=2)

        self.up_button.config(command=self.on_up)
        self.down_button.config(command=self.on_down)

        # Optional: configure spacing behavior
        # self.grid_columnconfigure(9, weight=1)

    def on_up(self):
        params = self.get_motion_params()
        print("UP:", params)

    def on_down(self):
        params = self.get_motion_params()
        print("DOWN:", params)

    def get_motion_params(self):
        try:
            step = float(self.step_var.get())
        except ValueError:
            step = None

        try:
            speed = float(self.speed_var.get())
        except ValueError:
            speed = None

        return {
            "step": step,
            "step_unit": self.step_unit_var.get(),
            "speed": speed,
            "speed_unit": self.speed_unit_var.get(),
        }
