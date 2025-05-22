import os
import tkinter as tk
from PIL import Image, ImageTk

from chosen_user import ChosenUser
from game_ui import GameUI


class StorageMenu:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title(f"{ChosenUser.user.username}'s Storage Menu")
        self.window.geometry("923x1080")

        self.init_background()
        self.game_ui = GameUI(self.canvas)
        self.display_user_properties()
        self.add_close_button()

    # Initialize the background
    def init_background(self):
        bg_path = "assets/storage_background.jpg"
        if not os.path.exists(bg_path):
            raise FileNotFoundError(f"Background image '{bg_path}' not found.")

        img = Image.open(bg_path)
        self.bg_photo = ImageTk.PhotoImage(img)

        self.canvas = tk.Canvas(self.window, width=img.width, height=img.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

    # Displays the UI (or refreshes it)
    def display_user_properties(self):
        user = ChosenUser.user
        if not user:
            raise Exception("No user is chosen.")

        properties = [
            {"label": "Eggs", "value": str(user.eggs)},
            {"label": "Milk", "value": str(user.milk)},
            {"label": "Chicken Feed", "value": str(user.food_chicken)},
            {"label": "Cow Feed", "value": str(user.food_cow)}
        ]

        images = [
            "assets/eggs.png",
            "assets/milk.png",
            "assets/chicken_food.png",
            "assets/cow_food.png"
        ]

        x_start = 311
        y_start = 200
        y_offset = 80

        for i, prop in enumerate(properties):
            if (i == 1 or i) == 3 and user.cows == 0:
                continue
            self.game_ui.add_gui_rectangle_element(
                x=x_start, y=y_start + (i * y_offset), width=300, height=70,
                text=f"{prop['label']}: {prop['value']}",
                image_path=images[i],
                color_in="lightblue",
                color_out="blue"
            )

    # Adds the close button
    def add_close_button(self):
        self.game_ui.add_gui_rectangle_element(
            x=386, y=640, width=150, height=70,
            text="Close", image_path="",
            color_in="red",
            color_out="darkred",
            onclick=self.close_window
        )

    # Handles closing the window event
    def close_window(self, event=None):
        self.window.destroy()
