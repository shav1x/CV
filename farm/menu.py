import os
import tkinter as tk

from PIL import Image, ImageTk

from chosen_user import ChosenUser
from game import Game
from game_ui import GameUI
from options import Options
from user_menu import UserMenu

class Menu:
    def __init__(self):
        self.music_toggle = True
        self.root = tk.Tk()
        self.root.title("Main menu")
        self.root.geometry("1920x1080")
        self.root.focus_force()
        self.init_background()
        self.game_ui = GameUI(self.canvas)
        self.create_menu_buttons()


    # Creates the menu buttons
    def create_menu_buttons(self):
        self.game_ui.add_gui_rectangle_element(
            x=230, y=25, width=150, height=80,
            text=f"Play!", image_path="",
            color_in="sienna",
            color_out="wheat",
            onclick=self.on_play_button_click
        )
        self.game_ui.add_gui_rectangle_element(
            x=900, y=25, width=150, height=80,
            text=f"Options", image_path="",
            color_in="sienna",
            color_out="wheat",
            onclick=self.options_menu
        )
        self.game_ui.add_gui_rectangle_element(
            x=410, y=25, width=200, height=80,
            text=f"Choose user", image_path="",
            color_in="sienna",
            color_out="wheat",
            onclick=self.users_menu
        )
        self.game_ui.add_gui_rectangle_element(
            x=1350, y=750, width=130, height=80,
            text=f"Exit", image_path="",
            color_in="sienna",
            color_out="wheat",
            onclick=self.close_menu
        )

    # What happens when the play button was clicked
    def on_play_button_click(self, event=None):
        self.root.destroy()
        Game(ChosenUser.user)

    # What happens when the user menu button was clicked
    def users_menu(self, event=None):
        UserMenu(self.root)

    # What happens when the close button was clicked
    def close_menu(self, event=None):
        self.root.destroy()

    # What happens when the option button was clicked
    def options_menu(self, event=None):
        Options(self.root)

    # Initialize the background
    def init_background(self):
        bckgrnd_path = "assets/menu_background.png"
        if not os.path.exists(bckgrnd_path):
            raise FileNotFoundError(f"Background image '{bckgrnd_path}' not found.")

        self.bg_image = Image.open(bckgrnd_path)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root, width=self.bg_image.width, height=self.bg_image.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

# To start the program
if __name__ == "__main__":
    ChosenUser()
    menu = Menu()
    menu.root.mainloop()
