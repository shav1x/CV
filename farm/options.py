import os
import sys
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

from game_ui import GameUI

class Options:

    game_music_toggle = True
    game_sound_toggle = True

    def __init__(self, parent, game=False):
        self.window = tk.Toplevel(parent)
        self.window.title("Options")
        self.window.geometry("1413x942")
        self.init_background()
        self.game_ui = GameUI(self.canvas)
        self.music_toggle_state = tk.BooleanVar()
        self.music_toggle_state.set(self.game_music_toggle)
        self.sound_toggle_state = tk.BooleanVar()
        self.sound_toggle_state.set(self.game_sound_toggle)
        self.create_checkbutton(570, 370)
        if game:
            self.game_ui.add_gui_rectangle_element(
                x=645, y=660, width=110, height=80,
                text=f"Close", image_path="",
                color_in="sienna",
                color_out="wheat",
                onclick=self.close_options
            )
            self.game_ui.add_gui_rectangle_element(
                x=580, y=560, width=250, height=80,
                text=f"Exit the game", image_path="",
                color_in="sienna",
                color_out="wheat",
                onclick=self.exit_the_game
            )
        else:
            self.game_ui.add_gui_rectangle_element(
                x=645, y=680, width=110, height=80,
                text=f"Close", image_path="",
                color_in="sienna",
                color_out="wheat",
                onclick=self.close_options
            )
        self.window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.window.destroy()
        )

    # Initialize the background
    def init_background(self):
        bckgrnd_path = "assets/options_background.jpg"
        if not os.path.exists(bckgrnd_path):
            raise FileNotFoundError(f"Background image '{bckgrnd_path}' not found.")

        bg_image = Image.open(bckgrnd_path)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.window, width=bg_image.width, height=bg_image.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

    # Creates the checkbuttons (to toggle the music/sound)
    def create_checkbutton(self, x, y):
        custom_font = font.Font(family="Galvji", size=40, weight="bold")

        self.checkbox = tk.Checkbutton(
            self.window,
            text="Game music",
            variable=self.music_toggle_state,
            onvalue=True,
            offvalue=False,
            command=self.on_toggle_music,
            bg="sienna",
            fg="wheat",
            activebackground="yellow",
            activeforeground="blue",
            font=custom_font,
        )

        self.canvas.create_window(x, y, anchor=tk.NW, window=self.checkbox)

        self.checkbox2 = tk.Checkbutton(
            self.window,
            text="Game sound",
            variable=self.sound_toggle_state,
            onvalue=True,
            offvalue=False,
            command=self.on_toggle_sound,
            bg="sienna",
            fg="wheat",
            activebackground="yellow",
            activeforeground="blue",
            font=custom_font,
        )

        self.canvas.create_window(x - 2, y + 75, anchor=tk.NW, window=self.checkbox2)

    # What happens when the music checkbutton is pressed
    def on_toggle_music(self):
        Options.game_music_toggle = self.music_toggle_state.get()
        if hasattr(self.window.master, "update_music_state"):
            self.window.master.update_music_state(Options.game_music_toggle)

    # What happens when the sound checkbutton is pressed
    def on_toggle_sound(self):
        Options.game_sound_toggle = self.sound_toggle_state.get()
        if hasattr(self.window.master, "update_sound_state"):
            self.window.master.update_sound_state(Options.game_sound_toggle)

    # What happens when the close button was clicked
    def close_options(self, event=None):
        self.window.destroy()

    # What happens when the exit button was clicked
    def exit_the_game(self, event=None):
        sys.exit(0)
