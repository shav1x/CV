import glob
import json
import os
import time


class User:

    users = []

    def __init__(self, username):
        self.username = username
        self.balance = 7.5
        self.chickens = 1
        self.cows = 0
        self.food_chicken = 0
        self.food_cow = 0
        self.eggs = 0
        self.milk = 0
        self.eggs_to_collect = 0
        self.milk_to_collect = 0
        self.animals = [{
            "name": "Chicken1",
            "status": "hungry",
            "next_product_time": None,
            "last_saved_time": None
        }]

        User.users.append(self)
        self._load_from_db()

    # Updates the user's JSON file
    def write_into_db(self):
        file_path = f"users/{self.username}.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    # Load the user from the JSON
    def _load_from_db(self):
        file_path = f"users/{self.username}.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                for key, value in data.items():
                    setattr(self, key, value)

                self._adjust_animal_timers()

    # Keeps the JSON's next_product_time updated
    def _adjust_animal_timers(self):
        current_time = time.time()
        for animal in self.animals:
            if animal["status"] == "satisfied" and animal["next_product_time"]:
                time_elapsed = current_time - animal["last_saved_time"]
                remaining_time = animal["next_product_time"] - time_elapsed
                if remaining_time <= 0:
                    animal["status"] = "hungry"
                    animal["next_product_time"] = None
                else:
                    animal["next_product_time"] = remaining_time

    # Convert the user to dictionary
    def to_dict(self):
        return {
            "username": self.username,
            "balance": self.balance,
            "chickens": self.chickens,
            "cows": self.cows,
            "food_chicken": self.food_chicken,
            "food_cow": self.food_cow,
            "eggs": self.eggs,
            "milk": self.milk,
            "eggs_to_collect": self.eggs_to_collect,
            "milk_to_collect": self.milk_to_collect,
            "animals": self.animals,
        }

    # Add new chicken to the JSON
    def add_chicken(self):
        self.animals.append({"name": f"Chicken{self.chickens}",
                             "status": "hungry",
                             "next_product_time": None,
                             "last_saved_time": None
                             })

    # Add new cow to the JSON
    def add_cow(self):
        self.animals.append({"name": f"Cow{self.cows}",
                             "status": "hungry",
                             "next_product_time": None,
                             "last_saved_time": None
                             })

    # Deletes the user's JSON
    @staticmethod
    def delete_user(username):
        file_path = f"users/{username}.json"
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            Exception("No user was found with that username.")

    # Appends all users to the JSON
    @staticmethod
    def append_all_users():
        user_files = glob.glob("users/*.json")
        for file_path in user_files:
            with open(file_path, "r") as f:
                data = json.load(f)
                user = User.__new__(User)
                for key, value in data.items():
                    setattr(user, key, value)
                User.users.append(user)