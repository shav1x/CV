import os
import tkinter as tk

from PIL import Image, ImageTk

from chosen_user import ChosenUser
from game_ui import GameUI


class HenhouseMenu:
    def __init__(self, parent, update_items_ui_callback=None, update_animals_ui_callback=None, update_animals_statuses_callback=None, update_animals_collect_callback=None):
        self.window = tk.Toplevel(parent)
        self.update_items_ui_callback = update_items_ui_callback
        self.update_animals_ui_callback = update_animals_ui_callback
        self.update_animals_statuses_callback = update_animals_statuses_callback
        self.update_user_collect_callback = update_animals_collect_callback
        self.window.title("Chicken Management Menu")
        self.window.geometry("720x1080")

        self.selected_eggs = tk.IntVar(value=1)
        self.selected_chickens = tk.IntVar(value=0)

        self.init_background()
        self.game_ui = GameUI(self.canvas)
        self.display_user_properties()
        self.add_sliders_buttons()
        self.add_close_button()
        self.refresh()

    # Initialize the background
    def init_background(self):
        bg_path = "assets/henhouse_background.png"
        if not os.path.exists(bg_path):
            raise FileNotFoundError(f"Background image '{bg_path}' not found.")

        img = Image.open(bg_path)
        self.bg_photo = ImageTk.PhotoImage(img)

        self.canvas = tk.Canvas(self.window, width=img.width, height=img.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.refresh()

    # Show the ui or refresh it (to keep the ui up to date)
    def display_user_properties(self):
        user = ChosenUser.user
        if not user:
            raise Exception("No user is chosen.")

        properties = [
            {"label": "Eggs to collect", "value": str(user.eggs_to_collect)},
            {"label": "Feed chickens     ", "value": None}
        ]

        images = [
            "assets/eggs.png",
            "assets/chicken.png",
        ]

        x_start = 155
        y_start = 200
        y_offset = 230

        self.game_ui.add_gui_rectangle_element(
            x=x_start, y=385, width=290, height=50,
            text=f"You have: {ChosenUser.user.food_chicken}",
            image_path="assets/chicken_food.png",
            color_in="lightyellow",
            color_out="gold"
        )

        for i, prop in enumerate(properties):
            self.game_ui.add_gui_rectangle_element(
                x=x_start, y=y_start + (i * y_offset), width=290, height=70,
                text=f"{prop['label']}: {prop['value']}" if prop['value'] else f"{prop['label']}",
                image_path=images[i],
                color_in="lightblue",
                color_out="blue"
            )

    # Add sliders to buy/sell something
    def add_sliders_buttons(self):
        egg_slider = tk.Scale(
            self.window,
            from_=1,
            to=4,
            orient="horizontal",
            variable=self.selected_eggs,
            length=200,
            bg="lightgrey",
            fg="blue",
            troughcolor="lightblue",
            activebackground="blue",
            highlightbackground="blue",
            highlightthickness=3
        )
        egg_slider.place(x=200, y=285)

        chicken_slider = tk.Scale(
            self.window,
            from_=0,
            to=sum(1 for animal in ChosenUser.user.animals if "Chicken" in animal["name"] and animal["status"] == "hungry"),
            orient="horizontal",
            variable=self.selected_chickens,
            length=200,
            bg="lightgrey",
            fg="blue",
            troughcolor="lightblue",
            activebackground="blue",
            highlightbackground="blue",
            highlightthickness=4
        )
        chicken_slider.place(x=200, y=515)

        self.game_ui.add_gui_rectangle_element(
            x=490, y=237, width=140, height=60,
            text=f"Collect", image_path="",
            color_in="lime",
            color_out="green",
            onclick=self.collect_eggs
        )

        self.game_ui.add_gui_rectangle_element(
            x=490, y=467, width=140, height=60,
            text=f"Feed", image_path="",
            color_in="lime",
            color_out="green",
            onclick=self.feed_chickens
        )

    # Adds a close button
    def add_close_button(self):
        self.game_ui.add_gui_rectangle_element(
            x=305, y=680, width=110, height=50,
            text="Close",
            image_path="",
            color_in="tomato",
            color_out="red",
            onclick=self.close_window
        )

    # A method which applies the changes in the case of collecting eggs
    def collect_eggs(self, event=None):
        if self.selected_eggs.get() == 0:
            return
        collected = 0
        user_animals = ChosenUser.user.to_dict()["animals"]
        for i in range(len(user_animals)):
            if "Chicken" in user_animals[i]["name"] and user_animals[i]["status"] == "collect":
                collected += 1
                user_animals[i]["status"] = "hungry"
            if collected == self.selected_eggs.get():
                break

        ChosenUser.user.eggs += collected
        ChosenUser.user.eggs_to_collect -= collected
        ChosenUser.user.write_into_db()
        self.selected_eggs.set(0)
        self.refresh()
        if self.update_animals_statuses_callback:
            self.update_animals_statuses_callback()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()
        if self.update_animals_ui_callback:
            self.update_animals_ui_callback()

    # A method which applies the changes in the case of feeding the chickens
    def feed_chickens(self, event=None):
        if ChosenUser.user.food_chicken < self.selected_chickens.get():
            return
        fed = 0
        user_animals = ChosenUser.user.to_dict()["animals"]
        for i in range(len(user_animals)):
            if "Chicken" in user_animals[i]["name"] and user_animals[i]["status"] == "hungry":
                fed += 1
                user_animals[i]["status"] = "satisfied"
                user_animals[i]["next_product_time"] = 180
            if fed == self.selected_chickens.get():
                break
        if fed != self.selected_chickens.get():
            return
        ChosenUser.user.food_chicken -= fed
        ChosenUser.user.write_into_db()
        self.selected_chickens.set(0)
        self.refresh()
        if self.update_animals_statuses_callback:
            self.update_animals_statuses_callback()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()
        if self.update_animals_ui_callback:
            self.update_animals_ui_callback()

    # Refreshes the UI every 1 second
    def refresh(self):
        try:
            self.add_sliders_buttons()
            self.display_user_properties()
            self.window.after(1000, self.refresh)
        except Exception as e:
            print(f"Error updating henhouse menu: {e}")

    # The event of closing the window
    def close_window(self, event=None):
        self.window.destroy()

class CowpenMenu:
    def __init__(self, parent, update_items_ui_callback=None, update_animals_ui_callback=None, update_animals_statuses_callback=None, update_animals_collect_callback=None):
        self.window = tk.Toplevel(parent)
        self.update_items_ui_callback = update_items_ui_callback
        self.update_animals_ui_callback = update_animals_ui_callback
        self.update_animals_statuses_callback = update_animals_statuses_callback
        self.update_user_collect_callback = update_animals_collect_callback
        self.window.title("Cow Management Menu")
        self.window.geometry("720x1080")

        self.selected_milk = tk.IntVar(value=1)
        self.selected_cows = tk.IntVar(value=0)

        self.init_background()
        self.game_ui = GameUI(self.canvas)
        self.display_user_properties()
        self.add_sliders_buttons()
        self.add_close_button()
        self.refresh()

    def init_background(self):
        bg_path = "assets/cowpen_background.png"
        if not os.path.exists(bg_path):
            raise FileNotFoundError(f"Background image '{bg_path}' not found.")

        img = Image.open(bg_path)
        self.bg_photo = ImageTk.PhotoImage(img)

        self.canvas = tk.Canvas(self.window, width=img.width, height=img.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.refresh()

    # Displays the UI or refreshes it
    def display_user_properties(self):
        user = ChosenUser.user
        if not user:
            raise Exception("No user is chosen.")

        properties = [
            {"label": "Milk to collect", "value": str(user.milk_to_collect)},
            {"label": "Feed cows      ", "value": None}
        ]

        images = [
            "assets/milk.png",
            "assets/cow.png",
        ]

        x_start = 155
        y_start = 200
        y_offset = 230

        self.game_ui.add_gui_rectangle_element(
            x=x_start, y=385, width=290, height=50,
            text=f"You have: {ChosenUser.user.food_cow}",
            image_path="assets/cow_food.png",
            color_in="lightyellow",
            color_out="gold"
        )

        for i, prop in enumerate(properties):
            self.game_ui.add_gui_rectangle_element(
                x=x_start, y=y_start + (i * y_offset), width=290, height=70,
                text=f"{prop['label']}: {prop['value']}" if prop['value'] else f"{prop['label']}",
                image_path=images[i],
                color_in="lightblue",
                color_out="blue"
            )

    # Adds sliders to choose the amount of buying/selling
    def add_sliders_buttons(self):
        milk_slider = tk.Scale(
            self.window,
            from_=1,
            to=4,
            orient="horizontal",
            variable=self.selected_milk,
            length=200,
            bg="lightgrey",
            fg="blue",
            troughcolor="lightblue",
            activebackground="blue",
            highlightbackground="blue",
            highlightthickness=3
        )
        milk_slider.place(x=200, y=285)

        cow_slider = tk.Scale(
            self.window,
            from_=0,
            to=sum(1 for animal in ChosenUser.user.animals if "Cow" in animal["name"] and animal["status"] == "hungry"),
            orient="horizontal",
            variable=self.selected_cows,
            length=200,
            bg="lightgrey",
            fg="blue",
            troughcolor="lightblue",
            activebackground="blue",
            highlightbackground="blue",
            highlightthickness=4
        )
        cow_slider.place(x=200, y=515)

        self.game_ui.add_gui_rectangle_element(
            x=490, y=237, width=140, height=60,
            text=f"Collect", image_path="",
            color_in="lime",
            color_out="green",
            onclick=self.collect_milk
        )

        self.game_ui.add_gui_rectangle_element(
            x=490, y=467, width=140, height=60,
            text=f"Feed", image_path="",
            color_in="lime",
            color_out="green",
            onclick=self.feed_cows
        )

    def add_close_button(self):
        self.game_ui.add_gui_rectangle_element(
            x=305, y=680, width=110, height=50,
            text="Close",
            image_path="",
            color_in="tomato",
            color_out="red",
            onclick=self.close_window
        )

    # A method which applies the changes in the case of collecting the milk
    def collect_milk(self, event=None):
        if self.selected_milk.get() == 0:
            return
        collected = 0
        user_animals = ChosenUser.user.to_dict()["animals"]
        for i in range(len(user_animals)):
            if "Cow" in user_animals[i]["name"] and user_animals[i]["status"] == "collect":
                collected += 1
                user_animals[i]["status"] = "hungry"
            if collected == self.selected_milk.get():
                break

        ChosenUser.user.milk += collected
        ChosenUser.user.milk_to_collect -= collected
        ChosenUser.user.write_into_db()
        self.selected_milk.set(0)
        self.refresh()
        if self.update_animals_statuses_callback:
            self.update_animals_statuses_callback()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()
        if self.update_animals_ui_callback:
            self.update_animals_ui_callback()

    # A method which applies the changes in the case of feeding the cows
    def feed_cows(self, event=None):
        if ChosenUser.user.food_cow < self.selected_cows.get():
            return
        fed = 0
        user_animals = ChosenUser.user.to_dict()["animals"]
        for i in range(len(user_animals)):
            if "Cow" in user_animals[i]["name"] and user_animals[i]["status"] == "hungry":
                fed += 1
                user_animals[i]["status"] = "satisfied"
                user_animals[i]["next_product_time"] = 300
            if fed == self.selected_cows.get():
                break
        if fed != self.selected_cows.get():
            return
        ChosenUser.user.food_cow -= fed
        ChosenUser.user.write_into_db()
        self.selected_cows.set(0)
        self.refresh()
        if self.update_animals_statuses_callback:
            self.update_animals_statuses_callback()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()
        if self.update_animals_ui_callback:
            self.update_animals_ui_callback()

    # Refreshes the UI
    def refresh(self):
        try:
            self.add_sliders_buttons()
            self.display_user_properties()
            self.window.after(1000, self.refresh)
        except Exception as e:
            print(f"Error updating cowpen menu: {e}")

    # Event to close the window
    def close_window(self, event=None):
        self.window.destroy()
