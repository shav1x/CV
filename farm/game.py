import tkinter as tk
import os

import pygame
import random

from PIL import Image, ImageTk

from animal_menu import HenhouseMenu, CowpenMenu
from animals import Chicken, Cow
from chosen_user import ChosenUser
from game_ui import GameUI
from options import Options
from price_manager import PriceManager
from shop_menu import ShopMenu
from storage_menu import StorageMenu


class Game:

    MIN_DISTANCE = 50

    def __init__(self, user):
        pygame.mixer.init()

        self.user = user

        self.coins_text_id = None
        self.egg_text_id = None
        self.milk_text_id = None

        self.prices = PriceManager.get_instance().prices

        self.music_toggle = Options.game_music_toggle
        self.sound_toggle = Options.game_sound_toggle

        self.background_music_path = "assets/music.mp3"

        self.root = tk.Tk()
        self.root.title(f"{user.username}'s Farm")
        self.root.geometry("1920x1080")

        self.root.update_music_state = self.update_music_state
        self.root.update_sound_state = self.update_sound_state

        self.play_initial_sound() if self.music_toggle else None
        self.play_chicken_sound() if self.sound_toggle else None

        self.chicken_texture_left = self.load_chicken_texture(flip=False)
        self.chicken_texture_right = self.load_chicken_texture(flip=True)
        self.cow_texture_left = self.load_cow_texture(flip=False)
        self.cow_texture_right = self.load_cow_texture(flip=True)

        self.init_background()

        self.game_ui = GameUI(self.canvas)

        self.add_gui_elements()

        self.ready_chicken_icon = ImageTk.PhotoImage(
            Image.open("assets/egg.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.ready_cow_icon = ImageTk.PhotoImage(
            Image.open("assets/bucket.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.hungry_icon = ImageTk.PhotoImage(
            Image.open("assets/hungry.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.satisfied_icon = ImageTk.PhotoImage(
            Image.open("assets/wait.png").resize((20, 20), Image.Resampling.LANCZOS))

        self.chicken_movement_area = [
            (167, 257),  # Point 1
            (382, 257),  # Point 2
            (392, 187),  # Point 3
            (592, 207),  # Point 4
            (592, 282),  # Point 5
            (121, 277),  # Point 6
        ]

        self.cow_movement_area = [
            (500, 533),  # Point 1
            (749, 533),  # Point 2
            (795, 603),  # Point 3
            (464, 603),  # Point 4
        ]

        self.chicken_spawn_coordinates = self.chicken_movement_area.copy()
        self.chicken_spawn_coordinates[1] = (275, 271)
        self.chicken_spawn_coordinates[2] = (412, 187)
        self.chicken_spawn_coordinates[-2] = (532, 282)
        self.chicken_spawn_coordinates[-1] = (141, 277)
        self.chicken_spawn_coordinates.remove((167, 257))

        self.cow_spawn_coordinates = self.cow_movement_area.copy()

        self.chicken_positions = {}
        self.chicken_objects = {}
        self.chicken_targets = {}
        self.chicken_resting = {}

        self.cow_positions = {}
        self.cow_objects = {}
        self.cow_targets = {}
        self.cow_resting = {}

        self.chickens = []
        self.cows = []
        self.game_animals = []

        self.chicken_status_objects = {}
        self.chicken_timer_objects = {}

        self.cow_status_objects = {}
        self.cow_timer_objects = {}

        self.chicken_speed = 3
        self.cow_speed = 1.5

        self.restore_animals_from_save()
        self.spawn_animals()
        self.update_chicken_ui()
        self.update_cow_ui()
        self.render_animals()
        self.update_animals()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    # Updates the statuses of displayed animals, so they are correct/starts the timers for satisfied animals
    def restore_animals_from_save(self):
        user = ChosenUser.user
        for animal_data in user.animals:
            if "Chicken" in animal_data["name"]:
                animal = Chicken()
            elif "Cow" in animal_data["name"]:
                animal = Cow()
            else:
                continue

            animal.status = animal_data["status"]
            animal.next_product_time = animal_data["next_product_time"]
            if animal.status == "satisfied":
                animal._start_timer()
            self.game_animals.append(animal)

    # Play a sound at the start of the game
    def play_initial_sound(self):
        rooster_sound_path = "assets/rooster.wav"
        if not os.path.exists(rooster_sound_path):
            raise FileNotFoundError(f"Sound file '{rooster_sound_path}' not found.")

        rooster_sound = pygame.mixer.Sound(rooster_sound_path)
        rooster_sound.set_volume(1.0)
        rooster_sound.play()

        sound_duration = rooster_sound.get_length()
        self.root.after(int(sound_duration * 700), self.play_background_music)

    # Plays chicken sound at a random moment of time
    def play_chicken_sound(self):
        if not self.sound_toggle:
            return

        chicken_sound_path = "assets/chicken.wav"
        if not os.path.exists(chicken_sound_path):
            raise FileNotFoundError(f"Sound file '{chicken_sound_path}' not found.")

        chicken_sound = pygame.mixer.Sound(chicken_sound_path)
        chicken_sound.set_volume(1.0)
        chicken_sound.play()

        sound_duration = chicken_sound.get_length()
        self.chicken_sound_job = self.root.after(
            random.randint(10000, 30000), self.play_chicken_sound
        )

    # Plays cow sound at a random moment of time
    def play_cow_sound(self):
        if not self.sound_toggle:
            return

        cow_sound_path = "assets/moo.aiff"
        if not os.path.exists(cow_sound_path):
            raise FileNotFoundError(f"Sound file '{cow_sound_path}' not found.")

        cow_sound = pygame.mixer.Sound(cow_sound_path)
        cow_sound.set_volume(1.0)
        cow_sound.play()

        # Schedule the next cow sound to play after a random interval
        sound_duration = cow_sound.get_length()
        self.cow_sound_job = self.root.after(
            random.randint(20000, 60000), self.play_cow_sound
        )

    # Plays background music in a loop
    def play_background_music(self):
        if not self.music_toggle:
            pygame.mixer.music.stop()
            return

        if not os.path.exists(self.background_music_path):
            raise FileNotFoundError(f"Music file '{self.background_music_path}' not found.")

        pygame.mixer.music.load(self.background_music_path)
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1, fade_ms=2000)

    # Adds UI elements (buttons, etc.)
    def add_gui_elements(self):
        self.game_ui.add_gui_rectangle_element(
            x=85, y=730, width=200, height=70,
            text=f"Options  ", image_path="assets/options.png",
            color_in="#F5CC5B",
            color_out="peru",
            onclick=self.open_options
        )

        self.game_ui.add_gui_rectangle_element(
            x=1080, y=500, width=140, height=120,
            text=f"", image_path="assets/storage.png",
            color_in="lightblue",
            color_out="blue",
            onclick=self.open_storage
        )

        self.game_ui.add_gui_rectangle_element(
            x=1080, y=640, width=140, height=120,
            text=f"", image_path="assets/shop.png",
            color_in="lightblue",
            color_out="blue",
            onclick=self.open_shop
        )

        self.game_ui.add_gui_rectangle_element(
            x=745, y=325, width=100, height=80,
            text=f"", image_path="assets/chicken_icon.png",
            color_in="lightblue",
            color_out="blue",
            onclick=self.open_henhouse_menu
        )

        self.game_ui.add_gui_rectangle_element(
            x=315, y=500, width=100, height=80,
            text=f"", image_path="assets/cow_icon.png",
            color_in="lightblue",
            color_out="blue",
            onclick=self.open_cowpen_menu
        ) if ChosenUser.user.cows != 0 else None

        self.coins_text_id = self.game_ui.add_gui_rectangle_element(
            x=425, y=20, width=280, height=80,
            text=f"Money: ${ChosenUser.user.balance}", image_path="assets/coins.png",
            color_in="#F5CC5B",
            color_out="peru"
        )

        self.egg_text_id = self.game_ui.add_gui_rectangle_element(
            x=960, y=20, width=200, height=80,
            text=f"Eggs: {ChosenUser.user.eggs}  ", image_path="assets/eggs.png",
            color_in="#F5CC5B",
            color_out="peru"
        )

        self.milk_text_id = self.game_ui.add_gui_rectangle_element(
            x=1200, y=20, width=200, height=80,
            text=f"Milk: {ChosenUser.user.milk}    ", image_path="assets/milk.png",
            color_in="#F5CC5B",
            color_out="peru"
        )

    # What to do when the window is closef
    def on_close(self):
        if self.music_toggle:
            pygame.mixer.music.fadeout(2000)
        self.user.write_into_db()
        self.root.destroy()

    # Loads textures
    def load_chicken_texture(self, flip=False):
        chicken_texture_path = "assets/chicken.png"
        if not os.path.exists(chicken_texture_path):
            raise FileNotFoundError(f"Chicken texture '{chicken_texture_path}' not found.")

        img = Image.open(chicken_texture_path).convert("RGBA")
        if flip:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        return ImageTk.PhotoImage(img)

    # Loads textures
    def load_cow_texture(self, flip=False):
        cow_texture_path = "assets/cow.png"
        if not os.path.exists(cow_texture_path):
            raise FileNotFoundError(f"Cow texture '{cow_texture_path}' not found.")

        img = Image.open(cow_texture_path).convert("RGBA")
        if flip:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        return ImageTk.PhotoImage(img)

    # Spawns animals in the defined coordinates
    def spawn_animals(self):
        for _ in range(self.user.chickens):
            chicken = Chicken()
            self.chickens.append(chicken)
            x, y = self.chicken_spawn_coordinates[_]
            self.chicken_positions[chicken] = {"x": x, "y": y, "last_x": x}
            self.chicken_targets[chicken] = {"x": x, "y": y}
            self.chicken_resting[chicken] = False

        for _ in range(self.user.cows):
            cow = Cow()
            self.cows.append(cow)
            x, y = self.cow_spawn_coordinates[_]
            self.cow_positions[cow] = {"x": x, "y": y, "last_x": x}
            self.cow_targets[cow] = {"x": x, "y": y}
            self.cow_resting[cow] = False

        if self.cows and self.sound_toggle:
            self.play_cow_sound()

    # Checks the destination point of animal (whether it is in the restricted area or not)
    def is_point_in_polygon(self, x, y, polygon):
        n = len(polygon)
        inside = False
        px, py = x, y

        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n]

            if ((y1 > py) != (y2 > py)) and (px < (x2 - x1) * (py - y1) / (y2 - y1) + x1):
                inside = not inside

        return inside

    # Checks the minimum distance between animals, so they are not clustered
    def is_point_valid(self, x, y, positions, min_distance=MIN_DISTANCE):
        for pos in positions.values():
            other_x, other_y = pos["x"], pos["y"]
            distance = ((x - other_x) ** 2 + (y - other_y) ** 2) ** 0.5
            if distance < self.MIN_DISTANCE:
                return False
        return True

    # Play/stop music if the toggle was changed in options
    def update_music_state(self, music_state):
        self.music_toggle = music_state
        if self.music_toggle and not pygame.mixer.music.get_busy():
            self.play_initial_sound()
        elif not self.music_toggle:
            pygame.mixer.music.stop()

    # Play/stop sound if the toggle was changed in options
    def update_sound_state(self, sound_state):
        self.sound_toggle = sound_state
        if not self.sound_toggle:
            if hasattr(self, "chicken_sound_job") and self.chicken_sound_job is not None:
                try:
                    self.root.after_cancel(self.chicken_sound_job)
                except ValueError:
                    pass
                self.chicken_sound_job = None
            if hasattr(self, "cow_sound_job") and self.cow_sound_job is not None:
                try:
                    self.root.after_cancel(self.cow_sound_job)
                except ValueError:
                    pass
                self.cow_sound_job = None
        else:
            self.play_chicken_sound()
            self.play_cow_sound() if ChosenUser.user.cows != 0 else None

    # Define the next position of the chicken
    def get_random_point_with_min_distance_chicken(self, chicken_positions):
        while True:
            x_min = min(point[0] for point in self.chicken_movement_area)
            x_max = max(point[0] for point in self.chicken_movement_area)
            y_min = min(point[1] for point in self.chicken_movement_area)
            y_max = max(point[1] for point in self.chicken_movement_area)

            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)

            if self.is_point_in_polygon(x, y, self.chicken_movement_area) and \
                    self.is_point_valid(x, y, chicken_positions):
                return x, y

    # Define the next position of the cow
    def get_random_point_with_min_distance_cow(self, cow_positions):
        while True:
            x_min = min(point[0] for point in self.cow_movement_area)
            x_max = max(point[0] for point in self.cow_movement_area)
            y_min = min(point[1] for point in self.cow_movement_area)
            y_max = max(point[1] for point in self.cow_movement_area)

            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)

            if self.is_point_in_polygon(x, y, self.cow_movement_area) and \
                    self.is_point_valid(x, y, cow_positions, 220):
                return x, y

    # Updates the status UI of the chicken
    def update_chicken_ui(self):
        user_animals = [animal for animal in self.user.to_dict()["animals"] if "Chicken" in animal["name"]]

        for index, chicken in enumerate(self.chickens):
            if index < len(user_animals):
                chicken_data = user_animals[index]
                chicken.status = chicken_data["status"]
                chicken.next_product_time = chicken_data.get("next_product_time")
                chicken_data["next_product_time"] = chicken.next_product_time

        self.root.after(100, self.update_chicken_ui)

    # Updates the status UI of the cow
    def update_cow_ui(self):
        user_animals = [animal for animal in self.user.to_dict()["animals"] if "Cow" in animal["name"]]

        for index, cow in enumerate(self.cows):
            if index < len(user_animals):
                cow_data = user_animals[index]
                cow.status = cow_data["status"]
                cow.next_product_time = cow_data.get("next_product_time")

        self.root.after(100, self.update_cow_ui)

    # Displays the animals at the corresponding coordinates
    def render_animals(self):
        for chicken, pos in self.chicken_positions.items():
            x, y = pos["x"], pos["y"]
            if chicken not in self.chicken_objects:
                chicken_obj = self.canvas.create_image(x, y, anchor=tk.NW, image=self.chicken_texture_left)
                self.chicken_objects[chicken] = chicken_obj
            self.render_chicken_status_ui(chicken, x, y)

        for cow, pos in self.cow_positions.items():
            x, y = pos["x"], pos["y"]
            if cow not in self.cow_objects:
                cow_obj = self.canvas.create_image(x, y, anchor=tk.NW, image=self.cow_texture_left)
                self.cow_objects[cow] = cow_obj
            self.render_cow_status_ui(cow, x, y)

    # Keeps the chicken status up to date
    def render_chicken_status_ui(self, chicken, x, y):
        status = chicken.status
        image = None

        if status == "hungry":
            image = self.hungry_icon
        elif status == "collect":
            image = self.ready_chicken_icon
        elif status == "satisfied":
            image = self.satisfied_icon

        if chicken in self.chicken_status_objects:
            self.canvas.delete(self.chicken_status_objects[chicken])

        if chicken in self.chicken_timer_objects and status != "satisfied":
            self.canvas.delete(self.chicken_timer_objects[chicken])
            del self.chicken_timer_objects[chicken]

        if image:
            ui_obj = self.canvas.create_image(x + 27, y - 20, anchor=tk.CENTER, image=image)
            self.chicken_status_objects[chicken] = ui_obj

            if status == "satisfied" and chicken.next_product_time:
                timer_text = int(chicken.next_product_time)
                if chicken in self.chicken_timer_objects:
                    self.canvas.delete(self.chicken_timer_objects[chicken])
                text_obj = self.canvas.create_text(
                    x + 27, y - 40, text=f"{timer_text}s", fill="white", font=("Arial", 12, "bold")
                )
                self.chicken_timer_objects[chicken] = text_obj

    # Keeps the cow status up to date
    def render_cow_status_ui(self, cow, x, y):
        status = cow.status
        image = None

        if status == "hungry":
            image = self.hungry_icon
        elif status == "collect":
            image = self.ready_cow_icon
        elif status == "satisfied":
            image = self.satisfied_icon

        if cow in self.cow_status_objects:
            self.canvas.delete(self.cow_status_objects[cow])

        if cow in self.cow_timer_objects and status != "satisfied":
            self.canvas.delete(self.cow_timer_objects[cow])
            del self.cow_timer_objects[cow]

        if image:
            ui_obj = self.canvas.create_image(x + 118, y - 20, anchor=tk.CENTER, image=image)
            self.cow_status_objects[cow] = ui_obj

            if status == "satisfied" and cow.next_product_time:
                timer_text = int(cow.next_product_time)
                if cow in self.cow_timer_objects:
                    self.canvas.delete(self.cow_timer_objects[cow])
                text_obj = self.canvas.create_text(
                    x + 118, y - 40, text=f"{timer_text}s", fill="white", font=("Arial", 12, "bold")
                )
                self.cow_timer_objects[cow] = text_obj

    # Updates the position of animals on the screen every 100 ms
    def update_animals(self):
        for chicken, target in self.chicken_targets.items():
            if self.chicken_resting[chicken]:
                self.render_chicken_status_ui(chicken, target["x"], target["y"])
                continue

            current_x, current_y = self.chicken_positions[chicken]["x"], self.chicken_positions[chicken]["y"]
            target_x, target_y = target["x"], target["y"]

            if abs(current_x - target_x) < 5 and abs(current_y - target_y) < 5:
                self.chicken_resting[chicken] = True
                self.root.after(random.randint(2000, 5000), self.finish_resting_chicken, chicken)
                continue

            direction_x = target_x - current_x
            direction_y = target_y - current_y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

            step_x = (direction_x / distance) * self.chicken_speed if distance != 0 else 0
            step_y = (direction_y / distance) * self.chicken_speed if distance != 0 else 0

            new_x = current_x + step_x
            new_y = current_y + step_y
            self.chicken_positions[chicken]["x"] = new_x
            self.chicken_positions[chicken]["y"] = new_y
            self.canvas.coords(self.chicken_objects[chicken], new_x, new_y)

            self.render_chicken_status_ui(chicken, new_x, new_y)

            last_x = self.chicken_positions[chicken]["last_x"]
            if new_x > last_x:
                self.canvas.itemconfig(self.chicken_objects[chicken], image=self.chicken_texture_right)
            elif new_x < last_x:
                self.canvas.itemconfig(self.chicken_objects[chicken], image=self.chicken_texture_left)

            self.chicken_positions[chicken]["last_x"] = new_x

        for cow, target in self.cow_targets.items():
            if self.cow_resting[cow]:
                self.render_cow_status_ui(cow, target["x"], target["y"])
                continue

            current_x, current_y = self.cow_positions[cow]["x"], self.cow_positions[cow]["y"]
            target_x, target_y = target["x"], target["y"]

            if abs(current_x - target_x) < 5 and abs(current_y - target_y) < 5:
                self.cow_resting[cow] = True
                self.root.after(random.randint(5000, 10000), self.finish_resting_cow, cow)
                continue

            direction_x = target_x - current_x
            direction_y = target_y - current_y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

            step_x = (direction_x / distance) * self.cow_speed if distance != 0 else 0
            step_y = (direction_y / distance) * self.cow_speed if distance != 0 else 0

            new_x = current_x + step_x
            new_y = current_y + step_y
            self.cow_positions[cow]["x"] = new_x
            self.cow_positions[cow]["y"] = new_y
            self.canvas.coords(self.cow_objects[cow], new_x, new_y)

            self.render_cow_status_ui(cow, new_x, new_y)

            last_x = self.cow_positions[cow]["last_x"]
            if new_x > last_x:
                self.canvas.itemconfig(self.cow_objects[cow], image=self.cow_texture_right)
            elif new_x < last_x:
                self.canvas.itemconfig(self.cow_objects[cow], image=self.cow_texture_left)

            self.cow_positions[cow]["last_x"] = new_x

        self.root.after(100, self.update_animals)

    # Finish resting and choose a new target point (chicken)
    def finish_resting_chicken(self, chicken):
        if chicken in self.chicken_positions:
            current_positions = {
                other: {"x": self.chicken_positions[other]["x"], "y": self.chicken_positions[other]["y"]}
                for other in self.chicken_positions if other != chicken
            }
            new_target_x, new_target_y = self.get_random_point_with_min_distance_chicken(current_positions)
            self.chicken_targets[chicken] = {"x": new_target_x, "y": new_target_y}
            self.chicken_resting[chicken] = False

    # Finish resting and choose a new target point (cow)
    def finish_resting_cow(self, cow):
        if cow in self.cow_positions:
            current_positions = {
                other: {"x": self.cow_positions[other]["x"], "y": self.cow_positions[other]["y"]}
                for other in self.cow_positions if other != cow
            }
            new_target_x, new_target_y = self.get_random_point_with_min_distance_cow(current_positions)
            self.cow_targets[cow] = {"x": new_target_x, "y": new_target_y}
            self.cow_resting[cow] = False

    # Refreshes the user's UI to keep it updated
    def update_displayed_properties(self):
        self.canvas.itemconfig(self.coins_text_id, text=f"Coins: {ChosenUser.user.balance}")
        self.canvas.itemconfig(self.egg_text_id, text=f"Eggs: {ChosenUser.user.eggs}")
        self.canvas.itemconfig(self.milk_text_id, text=f"Milk: {ChosenUser.user.milk}")
        self.canvas.update_idletasks()

    # Called when a new animal was added
    def update_animals_callback(self):
        current_chickens = len(self.chicken_positions)
        current_cows = len(self.cow_positions)

        if ChosenUser.user.chickens > current_chickens:
            for _ in range(ChosenUser.user.chickens - current_chickens):
                chicken = Chicken()
                self.game_animals.append(chicken)
                x, y = self.get_random_point_with_min_distance_chicken(self.chicken_positions)
                self.chicken_positions[chicken] = {"x": x, "y": y, "last_x": x}
                self.chicken_targets[chicken] = {"x": x, "y": y}
                self.chicken_resting[chicken] = False
                chicken_obj = self.canvas.create_image(x, y, anchor=tk.NW, image=self.chicken_texture_left)
                self.chicken_objects[chicken] = chicken_obj

        if ChosenUser.user.cows > current_cows:
            for _ in range(ChosenUser.user.cows - current_cows):
                cow = Cow()
                self.game_animals.append(cow)
                x, y = self.get_random_point_with_min_distance_cow(self.cow_positions)
                self.cow_positions[cow] = {"x": x, "y": y, "last_x": x}
                self.cow_targets[cow] = {"x": x, "y": y}
                self.cow_resting[cow] = False
                cow_obj = self.canvas.create_image(x, y, anchor=tk.NW, image=self.cow_texture_left)
                self.cow_objects[cow] = cow_obj

            self.play_cow_sound() if self.sound_toggle else None

        if ChosenUser.user.cows == 1: self.add_gui_elements()

        self.render_animals()

    # Called when the statuses of animals were changed to satisfied and starts the timer (to collect)
    def update_animals_statuses_callback(self):
        user_animals = ChosenUser.user.to_dict()["animals"]
        for ind in range(len(user_animals)):
            if self.game_animals[ind].status != user_animals[ind]["status"]:
                if self.game_animals[ind].status == "hungry":
                    if (("Chicken" in self.game_animals[ind].name
                            and user_animals[ind]["status"] == "satisfied"
                            and user_animals[ind]["next_product_time"] == 180) or
                        ("Cow" in self.game_animals[ind].name
                            and user_animals[ind]["status"] == "satisfied"
                            and user_animals[ind]["next_product_time"] == 300)):
                        self.game_animals[ind].status = user_animals[ind]["status"]
                        self.game_animals[ind].next_product_time = user_animals[ind]["next_product_time"]
                        self.game_animals[ind]._start_timer()
                else:
                    self.game_animals[ind].status = user_animals[ind]["status"]

    # Called when the statuses of animals were changed to collect
    def update_animals_collect_callback(self):
        user_animals = ChosenUser.user.to_dict()["animals"]
        for ind in range(len(user_animals)):
            if self.game_animals[ind].status == "satisfied":
                if (("Chicken" in self.game_animals[ind].name or "Cow" in self.game_animals[ind].name)
                        and user_animals[ind]["status"] == "collect"):
                    self.game_animals[ind].status = user_animals[ind]["status"]

    # Initialize the background
    def init_background(self):
        bckgrnd_path = "assets/farm_background.png"
        if not os.path.exists(bckgrnd_path):
            raise FileNotFoundError(f"Background image '{bckgrnd_path}' not found.")

        self.bg_image = Image.open(bckgrnd_path)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root, width=self.bg_image.width, height=self.bg_image.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

    # Called when the option menu needs to be opened
    def open_options(self, event=None):
        Options(self.root, True)

    # Called when the storage menu needs to be opened
    def open_storage(self, event=None):
        StorageMenu(self.root)

    # Called when the shop menu needs to be opened
    def open_shop(self, event=None):
        ShopMenu(self.root, update_items_ui_callback=self.update_displayed_properties,
                 update_animals_ui_callback=self.update_animals_callback)

    # Called when the henhouse menu needs to be opened
    def open_henhouse_menu(self, event=None):
        HenhouseMenu(self.root, update_items_ui_callback=self.update_displayed_properties,
                     update_animals_ui_callback=self.update_animals_callback,
                     update_animals_statuses_callback=self.update_animals_statuses_callback,
                     update_animals_collect_callback=self.update_animals_collect_callback)

    # Called when the cowpen menu needs to be opened
    def open_cowpen_menu(self, event=None):
        CowpenMenu(self.root, update_items_ui_callback=self.update_displayed_properties,
                   update_animals_ui_callback=self.update_animals_callback,
                   update_animals_statuses_callback=self.update_animals_statuses_callback,
                   update_animals_collect_callback=self.update_animals_collect_callback
        )
