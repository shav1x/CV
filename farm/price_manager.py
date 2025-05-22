from prices import Prices

class PriceManager:
    _instance = None

    # Creates the instance of the prices
    def __new__(cls, json_file="prices.json"):
        if cls._instance is None:
            cls._instance = super(PriceManager, cls).__new__(cls)
            cls._instance.prices = Prices(json_file)
        return cls._instance

    # To get current prices
    @staticmethod
    def get_instance():
        if not PriceManager._instance:
            raise Exception("PriceManager must be initialized first!")
        return PriceManager._instance

# Initialize the PriceManager once
PriceManager()  # This will load prices from "prices.json"