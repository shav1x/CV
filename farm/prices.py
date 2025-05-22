import threading
import random
import time
import json

class Prices:
    def __init__(self, json_file, limits=None):
        self.json_file = json_file
        self.lock = threading.Lock()
        self.limits = limits or {
            "eggs": {"min": 10.3, "max": 13.5},
            "milk": {"min": 13.2, "max": 17.8},
            "chicken_feed": {"min": 5.6, "max": 8.9},
            "cow_feed": {"min": 8.3, "max": 11.7}
        }

        self.prices = self._load_prices()
        self.start_price_adjustment()

    # Load the prices from the JSON file
    def _load_prices(self):
        with open(self.json_file, "r") as file:
            return json.load(file)

    # Saves the updated prices
    def _save_prices(self):
        with open(self.json_file, "w") as file:
            json.dump(self.prices, file, indent=4)

    # Randomly changes the prices and saves them into the JSON
    def start_price_adjustment(self):
        def adjust_prices():
            while True:
                with self.lock:
                    for item, price in self.prices.items():
                        if item == "chicken" or item == "cow":
                            continue
                        # Adjust the price randomly between 1% and 20% (increase or decrease)
                        percentage_change = random.uniform(0.01, 0.2)
                        if random.choice([True, False]):
                            new_price = round(price * (1 + percentage_change), 2)
                        else:
                            new_price = round(price * (1 - percentage_change), 2)

                        # Apply limits for each item
                        min_price, max_price = self._get_limits(item)
                        self.prices[item] = min(max(new_price, min_price), max_price)

                    # Save the updated prices back to JSON
                    self._save_prices()

                # Wait for a random interval between 15 seconds and 1 minute
                time.sleep(random.randint(15, 60))

        adjustment_thread = threading.Thread(target=adjust_prices, daemon=True)
        adjustment_thread.start()

    # Get the min and max price limits for an item. Defaults are used if not specified.
    def _get_limits(self, item):
        default_min = 5  # Set default minimum if no custom limit provided
        default_max = float('inf')  # No maximum limit by default
        return self.limits.get(item, {}).get("min", default_min), self.limits.get(item, {}).get("max", default_max)

    # Gets the price of a given item
    def get_price(self, item):
        with self.lock:
            return self.prices.get(item)

    # Sets the price for a given item
    def set_price(self, item, price):
        with self.lock:
            # Apply limits when setting the price manually
            min_price, max_price = self._get_limits(item)
            self.prices[item] = min(max(price, min_price), max_price)
            self._save_prices()

    # Gets all the prices
    def get_all_prices(self):
        with self.lock:
            return self.prices.copy()