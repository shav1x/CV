import os
import tkinter as tk
from PIL import Image, ImageTk

from chosen_user import ChosenUser
from game_ui import GameUI
from price_manager import PriceManager


class ShopMenu:
    def __init__(self, parent, update_items_ui_callback=None, update_animals_ui_callback=None):
        self.prices = PriceManager.get_instance().prices
        self.window = tk.Toplevel(parent)
        self.update_items_ui_callback = update_items_ui_callback
        self.update_animals_ui_callback = update_animals_ui_callback
        self.window.title("Shop Menu")
        self.window.geometry("720x1080")

        self.selected_eggs = tk.IntVar(value=0)
        self.selected_milk = tk.IntVar(value=0)
        self.selected_chicken_feed = tk.IntVar(value=0)
        self.selected_cow_feed = tk.IntVar(value=0)

        self.init_background()
        self.game_ui = GameUI(self.canvas)
        self.display_user_properties()
        self.add_sliders_buttons()
        self.add_close_button()

        self.update_prices()

    # Initialize the background
    def init_background(self):
        bg_path = "assets/shop_background.png"
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

        current_prices = self.prices.get_all_prices()

        properties = [
            {"label": "Eggs", "value": str(user.eggs), "price": current_prices.get("eggs", "N/A")},
            {"label": "Milk", "value": str(user.milk), "price": current_prices.get("milk", "N/A")},
            {"label": "Chicken Feed", "value": "", "price": current_prices.get("chicken_feed", "N/A")},
            {"label": "Cow Feed", "value": "", "price": current_prices.get("cow_feed", "N/A")},
            {"label": "Chicken", "value": "", "price": current_prices.get("chicken", "N/A")},
            {"label": "Cow", "value": "", "price": current_prices.get("cow", "N/A")}
        ]

        images = [
            "assets/eggs.png",
            "assets/milk.png",
            "assets/chicken_food.png",
            "assets/cow_food.png",
            "assets/chicken.png",
            "assets/cow.png"
        ]

        x_start = 55
        y_start = 60
        y_offset = 140

        for i, prop in enumerate(properties):

            if (i == 1 or i == 3) and user.cows == 0:
                continue

            self.game_ui.add_gui_rectangle_element(
                x=x_start, y=y_start + (i * y_offset) - 45, width=250, height=50,
                text=f"Price: ${prop['price']:.2f}" if isinstance(prop['price'],
                                                                  (int, float)) else f"Price: {prop['price']}",
                image_path="",
                color_in="lightyellow",
                color_out="gold"
            )

            self.game_ui.add_gui_rectangle_element(
                x=x_start, y=y_start + (i * y_offset), width=250, height=70,
                text=f"{prop['label']}: {prop['value']}" if prop['value'] else f"{prop['label']}",
                image_path=images[i],
                color_in="lightblue",
                color_out="blue"
            )

        self.game_ui.add_gui_rectangle_element(
            x=340, y=15, width=180, height=50,
            text=f"${ChosenUser.user.balance}",
            image_path="assets/coins.png",
            color_in="lightyellow",
            color_out="gold"
        )

    # Adds sliders to choose the amount of items to buy or sell
    def add_sliders_buttons(self):
        egg_slider = tk.Scale(
            self.window,
            from_=0,
            to=ChosenUser.user.eggs,
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
        egg_slider.place(x=325, y=85)

        chicken_feed_slider = tk.Scale(
            self.window,
            from_=0,
            to=10,
            orient="horizontal",
            variable=self.selected_chicken_feed,
            length=200,
            bg="lightgrey",
            fg="blue",
            troughcolor="lightblue",
            activebackground="blue",
            highlightbackground="blue",
            highlightthickness=4
        )
        chicken_feed_slider.place(x=325, y=353)

        self.game_ui.add_gui_rectangle_element(
            x=550, y=70, width=120, height=50,
            text=f"Sell", image_path="",
            color_in="tomato",
            color_out="red",
            onclick=self.sell_eggs
        )

        self.game_ui.add_gui_rectangle_element(
            x=550, y=350, width=120, height=50,
            text=f"Buy", image_path="",
            color_in="lime",
            color_out="green",
            onclick=self.buy_chicken_feed
        )

        self.game_ui.add_gui_rectangle_element(
            x=550, y=630, width=120, height=50,
            text=f"Buy", image_path="",
            color_in="lime",
            color_out="green",
            onclick=self.buy_chicken
        )

        self.game_ui.add_gui_rectangle_element(
            x=550, y=770, width=120, height=50,
            text=f"Buy", image_path="",
            color_in="lime",
            color_out="green",
            onclick=self.buy_cow
        )

        if ChosenUser.user.cows != 0:
            milk_slider = tk.Scale(
                self.window,
                from_=0,
                to=ChosenUser.user.milk,
                orient="horizontal",
                variable=self.selected_milk,
                length=200,
                bg="lightgrey",
                fg="blue",
                troughcolor="lightblue",
                activebackground="blue",
                highlightbackground="blue",
                highlightthickness=4
            )
            milk_slider.place(x=325, y=213)

            cow_feed_slider = tk.Scale(
                self.window,
                from_=0,
                to=10,
                orient="horizontal",
                variable=self.selected_cow_feed,
                length=200,
                bg="lightgrey",
                fg="blue",
                troughcolor="lightblue",
                activebackground="blue",
                highlightbackground="blue",
                highlightthickness=4
            )
            cow_feed_slider.place(x=325, y=493)

            self.game_ui.add_gui_rectangle_element(
                x=550, y=210, width=120, height=50,
                text=f"Sell", image_path="",
                color_in="tomato",
                color_out="red",
                onclick=self.sell_milk
            )

            self.game_ui.add_gui_rectangle_element(
                x=550, y=490, width=120, height=50,
                text=f"Buy", image_path="",
                color_in="lime",
                color_out="green",
                onclick=self.buy_cow_feed
            )

    # Add the close button
    def add_close_button(self):
        self.game_ui.add_gui_rectangle_element(
            x=610, y=10, width=100, height=35,
            text="Close", image_path="",
            color_in="red",
            color_out="darkred",
            onclick=self.close_window
        )

    # Handles the selling eggs event
    def sell_eggs(self, event=None):
        ChosenUser.user.eggs -= self.selected_eggs.get()
        ChosenUser.user.balance = round(
            ChosenUser.user.balance + (self.prices.get_price("eggs") * self.selected_eggs.get()), 2)
        ChosenUser.user.write_into_db()
        self.selected_eggs.set(0)
        self.display_user_properties()
        self.add_sliders_buttons()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()

    # Handles the selling milk event
    def sell_milk(self, event=None):
        ChosenUser.user.milk -= self.selected_milk.get()
        ChosenUser.user.balance = round(
            ChosenUser.user.balance + (self.prices.get_price("milk") * self.selected_milk.get()), 2)
        ChosenUser.user.write_into_db()
        self.selected_milk.set(0)
        self.display_user_properties()
        self.add_sliders_buttons()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()

    # Handles the buying chicken feed event
    def buy_chicken_feed(self, event=None):
        if ChosenUser.user.balance < self.prices.get_price("chicken_feed") * self.selected_chicken_feed.get():
            self.selected_chicken_feed.set(0)
            return
        ChosenUser.user.balance = round(
            ChosenUser.user.balance - (self.prices.get_price("chicken_feed") * self.selected_chicken_feed.get()), 2)
        ChosenUser.user.food_chicken += self.selected_chicken_feed.get()
        ChosenUser.user.write_into_db()
        self.selected_chicken_feed.set(0)
        self.display_user_properties()
        self.add_sliders_buttons()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()

    # Handles the buying cow feed event
    def buy_cow_feed(self, event=None):
        if ChosenUser.user.balance < self.prices.get_price("cow_feed") * self.selected_cow_feed.get():
            self.selected_cow_feed.set(0)
            return
        ChosenUser.user.balance = round(
            ChosenUser.user.balance - (self.prices.get_price("cow_feed") * self.selected_cow_feed.get()), 2)
        ChosenUser.user.food_cow += self.selected_cow_feed.get()
        ChosenUser.user.write_into_db()
        self.selected_cow_feed.set(0)
        self.display_user_properties()
        self.add_sliders_buttons()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()

    # Handles the buying chicken event
    def buy_chicken(self, event=None):
        if ChosenUser.user.balance < self.prices.get_price("chicken"):
            return

        if ChosenUser.user.chickens > 3:
            chickens_label = tk.Label(
                self.window,
                text="Max number of chickens reached",
                font=("Arial", 14, "bold"),
                fg="darkgreen",
                bg="orange"
            )
            chickens_label.place(x=315, y=655)
            self.window.after(5000, lambda: chickens_label.destroy())
            return

        ChosenUser.user.balance = round(ChosenUser.user.balance - self.prices.get_price("chicken"), 2)
        ChosenUser.user.chickens += 1
        ChosenUser.user.add_chicken()
        ChosenUser.user.write_into_db()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()
        if self.update_animals_ui_callback:
            self.update_animals_ui_callback()

    # Handles the buying cow event
    def buy_cow(self, event=None):
        if ChosenUser.user.balance < self.prices.get_price("cow"):
            return

        if ChosenUser.user.cows > 3:
            cows_label = tk.Label(
                self.window,
                text="Max number of cows reached",
                font=("Arial", 14, "bold"),
                fg="darkgreen",
                bg="orange"
            )
            cows_label.place(x=322, y=795)
            self.window.after(5000, lambda: cows_label.destroy())
            return

        ChosenUser.user.balance = round(ChosenUser.user.balance - self.prices.get_price("cow"), 2)
        ChosenUser.user.cows += 1
        ChosenUser.user.add_cow()
        ChosenUser.user.write_into_db()
        if self.update_items_ui_callback:
            self.update_items_ui_callback()
        if self.update_animals_ui_callback:
            self.update_animals_ui_callback()

    # Updates the prices displayed on the UI every 2 seconds (to keep them up to date)
    def update_prices(self):
        try:
            self.display_user_properties()
            self.window.after(2000, self.update_prices)
        except Exception as e:
            print(f"Error updating prices: {e}")

    # Closing the window event
    def close_window(self, event=None):
        self.window.destroy()
