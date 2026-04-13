from tkinter import Misc, ttk

MENU_BAR_SIZE = 40


class SizeableButton(ttk.Frame):
    """_summary_.

    :param ttk: _description_
    """

    def __init__(
        self,
        master: Misc | None,
        *,
        height: float,
        text: str = "",
        width: float,
        **kwargs: ...,
    ) -> None:
        """_summary_.

        :param master: _description_
        :param height: _description_
        :param width: _description_
        :param text: _description_, defaults to ""
        """
        super().__init__(
            master=master,
            height=height,
            width=width,
            **kwargs,
        )
        _ = self.pack_propagate(flag=False)
        self.button: ttk.Button = ttk.Button(self, text=text)
        self.button.pack(fill="both", expand=True)
