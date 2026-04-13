import tkinter as tk
from tkinter import ttk

from src.gui.gui_plugins import MotorControlWidget
from src.gui.gui_utils import SizeableButton


class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        self.title("ASAP Controller")
        self.geometry("1200x800")
        style = ttk.Style()
        style.theme_use("classic")

        self._build_layout()
        self._enable_bindings()

    def _build_layout(self) -> None:
        _ = self.rowconfigure(1, weight=1)
        _ = self.columnconfigure(0, weight=1, minsize=300)
        _ = self.columnconfigure(1, weight=2)

        self.menu_frame: ttk.Frame = ttk.Frame(
            self,
            border=2,
            relief="raised",
        )
        self.menu_frame.grid(row=0, column=0, columnspan=2, sticky="new")
        self.home_button: SizeableButton = SizeableButton(
            self.menu_frame,
            width=60,
            height=60,
        )
        self.home_button.grid(row=0, column=0, sticky="nsw")
        self.stop_button: SizeableButton = SizeableButton(
            self.menu_frame,
            height=60,
            width=60,
        )
        self.stop_button.grid(row=0, column=1, sticky="nsw")

        self.camera_frame: ttk.Frame = ttk.Frame(self, border=2, relief="raised")
        self.camera_frame.grid(row=1, column=0, sticky="nsew")
        # self.camera_frame.grid_propagate(flag=False)

        """self.camera_canvas: tk.Canvas = tk.Canvas(
            self.camera_frame,
            bg="black",
            highlightthickness=0,
        )
        self.camera_canvas.pack(anchor="n", fill="x")"""

        options_frame = ttk.Frame(self, border=2, relief="raised")
        options_frame.grid(row=1, column=1, sticky="nsew")
        options_frame.columnconfigure(0, weight=1)
        options_frame.rowconfigure(0, weight=1)
        options_frame.rowconfigure(4, weight=1)

        stage_frame = ttk.LabelFrame(options_frame, text="Stage")
        stage_frame.grid(row=1, column=0, pady=10)

        self.stage_x = MotorControlWidget(
            stage_frame,
            motor=None,
            text="X-Axis",
            motion_type="linear",
        )
        self.stage_x.grid(row=0, column=0)
        self.stage_y = MotorControlWidget(
            stage_frame,
            motor=None,
            text="Y-Axis",
            motion_type="linear",
        )
        self.stage_y.grid(row=1, column=0)
        self.stage_theta = MotorControlWidget(
            stage_frame,
            motor=None,
            text="Theta-Axis",
            motion_type="angular",
        )
        self.stage_theta.grid(row=2, column=0)

        frame_frame = ttk.LabelFrame(options_frame, text="Frame")
        frame_frame.grid(row=2, column=0, pady=10)

        self.stage_x = MotorControlWidget(
            frame_frame,
            motor=None,
            text="X-Axis",
            motion_type="linear",
        )
        self.stage_x.grid(row=0, column=0)
        self.stage_y = MotorControlWidget(
            frame_frame,
            motor=None,
            text="Y-Axis",
            motion_type="linear",
        )
        self.stage_y.grid(row=1, column=0)

        z_gantry_frame = ttk.LabelFrame(options_frame, text="Gantry, Z Axis")
        z_gantry_frame.grid(row=3, column=0, pady=10)

        self.stage_x = MotorControlWidget(
            z_gantry_frame,
            motor=None,
            text="Gantry",
            motion_type="linear",
        )
        self.stage_x.grid(row=0, column=0)
        self.stage_y = MotorControlWidget(
            z_gantry_frame,
            motor=None,
            text="Z-Axis",
            motion_type="linear",
        )
        self.stage_y.grid(row=1, column=0)

        # add play button to resume

    def _enable_bindings(self) -> None:
        self.camera_frame.bind("<Configure>", self._resize_camera)

    def _resize_camera(self, event):
        size = event.width
        """self.camera_canvas.delete("all")
        self.camera_canvas.create_rectangle(0, 0, size, size, fill="black")"""


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
