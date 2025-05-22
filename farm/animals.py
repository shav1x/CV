import threading
import time
from chosen_user import ChosenUser


class Animal:
    def __init__(self, name, product_name, production_time):
        self.name = name
        self.product_name = product_name
        self.status = "hungry"
        self.next_product_time = None
        self.production_time = production_time
        self.thread = None

    # Feed the animal and start the production process.
    def feed(self):
        if self.status == "hungry":
            self.status = "satisfied"
            self.next_product_time = self.production_time
            self._start_timer()

    # Collect product and make the animal hungry again.
    def collect(self):
        if self.status == "collect":
            user = ChosenUser.user
            if self.product_name == "egg":
                user.eggs += 1
            elif self.product_name == "milk":
                user.milk += 1
            self.status = "hungry"
            user.write_into_db()

    # Start a timer for producing a product.
    def _start_timer(self):
        if self.thread and self.thread.is_alive():
            self.thread = None
        self.thread = threading.Thread(target=self._produce, daemon=True)
        self.thread.start()

    # Handle the production timer.
    def _produce(self):
        start_time = time.time()
        while self.status == "satisfied":
            time.sleep(1)
            elapsed_time = time.time() - start_time
            start_time = time.time()
            self.next_product_time -= elapsed_time

            if self.next_product_time <= 0:
                self.status = "collect"
                self.next_product_time = None
                self._update_collectable_product()
                break

            self._save_state()

        self._save_state()

    def _update_collectable_product(self):
        """Mark the product as ready to collect."""
        user = ChosenUser.user
        if self.product_name == "egg":
            user.eggs_to_collect += 1
        elif self.product_name == "milk":
            user.milk_to_collect += 1
        user.write_into_db()

    def _save_state(self):
        """Save the animal's state to the user data."""
        user = ChosenUser.user
        for animal in user.animals:
            if animal["name"] == self.name:
                animal["status"] = self.status
                animal["next_product_time"] = self.next_product_time
                animal["last_saved_time"] = time.time()
                user.write_into_db()
                break
        else:
            # If the animal isn't in the list, add it
            user.animals.append({
                "name": self.name,
                "status": self.status,
                "next_product_time": self.next_product_time,
                "last_saved_time": time.time(),
            })
            user.write_into_db()

class Chicken(Animal):
    counter = 0

    def __init__(self):
        Chicken.counter += 1
        super().__init__(name=f"Chicken{Chicken.counter}", product_name="egg", production_time=300)


class Cow(Animal):
    counter = 0

    def __init__(self):
        Cow.counter += 1
        super().__init__(name=f"Cow{Cow.counter}", product_name="milk", production_time=600)