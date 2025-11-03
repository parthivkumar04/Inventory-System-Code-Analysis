"""
A inventory management system to track stock, load/save data
and check for low stock items using a class structure.
"""


import json
from datetime import datetime


class InventorySystem:
    """Manages the stock, data loading and reporting for items."""

    def __init__(self):
        # stock_data is now an instance attribute not a global variable.
        self.stock_data = {}

    def add_item(self, item="default", qty=0, logs=None):
        """Adds a quantity to the stock for a given item."""
        if not isinstance(qty, (int, float)):
            print(f"Error: Quantity must be a number, got {type(qty)}")
            return

        if logs is None:
            logs = []
        if not item:
            return

        item_key = str(item)
        self.stock_data[item_key] = self.stock_data.get(item_key, 0) + qty

        logs.append(f"{datetime.now()}: Added {qty} of {item_key}")

    def remove_item(self, item, qty):
        """Removes a quantity from the stock for a given item."""
        try:
            self.stock_data[item] -= qty
            if self.stock_data[item] <= 0:
                del self.stock_data[item]
        except KeyError:
            pass

    def get_qty(self, item):
        """Returns the current quantity of an item."""
        return self.stock_data.get(item, 0)

    def load_data(self, file="inventory.json"):
        """Loads inventory data from a JSON file."""
        try:
            with open(file, "r", encoding='utf-8') as f:
                self.stock_data = json.loads(f.read())
        except FileNotFoundError:
            print("Warning: File not found.Starting with empty inventory.")
        except json.JSONDecodeError:
            # Braking up the string cuz of line limit
            print("Error: Could not decode JSON from ")
            print("Starting with empty inventory.")

    def save_data(self, file="inventory.json"):
        """Saves inventory data to a JSON file."""
        with open(file, "w", encoding='utf-8') as f:
            f.write(json.dumps(self.stock_data))

    def print_data(self):
        """Prints a report of all items and their quantities."""
        print("Items Report")
        for i in self.stock_data:
            print(i, "->", self.stock_data[i])

    def check_low_items(self, threshold=5):
        """Returns a list of items below the specified threshold."""
        result = []
        for i in self.stock_data:
            if self.stock_data[i] < threshold:
                result.append(i)
        return result


def main():
    """The main execution function."""
    # Initialize the system as a class instance
    inventory = InventorySystem()

    # Call methods on the instance
    inventory.add_item("apple", 10)
    inventory.add_item("banana", -2)
    inventory.add_item(123, "ten")
    inventory.remove_item("apple", 3)
    inventory.remove_item("orange", 1)
    print("Apple stock:", inventory.get_qty("apple"))
    print("Low items:", inventory.check_low_items())
    inventory.save_data()
    inventory.load_data()
    inventory.print_data()

    # eval("print('eval used')")  # removed


main()

