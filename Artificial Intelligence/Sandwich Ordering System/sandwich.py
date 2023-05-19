# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import string

import re


class Menu:
    def __init__(self):
        self.menu_items = {
            "Samuel's Spicy Italian": (["Salami", "Pepperoni", "Cheddar Cheese", "Red Peppers", "Onions"],
                                       "White",
                                       "Chipotle"),
            "Club Tuna": (["Tuna Salad", "American Cheese", "Cucumber"],
                          "Whole Wheat",
                          "Mayo"),
            "Beach House": (["Turkey", "Provolone Cheese", "Avocado", "Cucumber"],
                            "Rye",
                            "Dijon Mustard"),
            "Cuban": (["Bacon", "Ham", "Swiss Cheese", "Pickles"],
                      "Whole Wheat",
                      "Dijon Mustard")
        }
        self.bread_types = {"Bread Options": ["Whole Wheat", "White", "Rye"]}
        self.spreads = {"Spread Options": ["Mayo", "Dijon Mustard", "Chipotle"]}
        self.options = {"Options": ["Toasted", "Salted", "Extra Cheese"]}
        self.exceptions = {"Exceptions": ["Onions", "Cucumber", "Avocado", "Ham"]}

    def get_menu_items(self):
        return self.menu_items.keys()

    def get_bread_types(self):
        return self.bread_types["Bread Options"]

    def get_usual_ingredients(self, name):
        return self.menu_items[name][0]

    def get_spread_options(self):
        return self.spreads["Spread Options"]

    def get_options(self):
        return self.options["Options"]

    def get_default_breads(self, name):
        return self.menu_items[name][1]

    def get_default_spreads(self, name):
        return self.menu_items[name][2]

    def get_exceptions(self):
        return self.exceptions["Exceptions"]

    def create_menu_helper(self, items):
        print()
        for key, value in items:
            print(key + ": ", end="")
            for v in value:
                print(v + ", ", end="")

    def create_menu(self):
        print("Menu")
        print("---------------------")
        print("Sandwiches: ")
        for name, (usual_ingredients, bread, spread) in self.menu_items.items():
            print(name + "- ", end="")
            print("Ingredients: ", end="")
            for items in usual_ingredients:
                print(items + ", ", end="")
            print("Default Bread: " + bread + ",", end=" ")
            print("Default Spread: " + spread, end=" ")
            print()
        Menu().create_menu_helper(self.bread_types.items())
        Menu().create_menu_helper(self.spreads.items())
        Menu().create_menu_helper(self.options.items())
        Menu().create_menu_helper(self.exceptions.items())
        print()


class CustomerInteraction:
    def greet_customer(self):
        print("Welcome to Sam's Sandwich Shop!")

    def parse_input_helper(self, order, items, delimiter=" "):
        possible_items = {}
        for item in items:
            split_item = item.split(delimiter)
            for word in split_item:
                if word == "Toasted":
                    if re.search("toasted|toasty|toast", order.lower()):
                        if item in possible_items:
                            possible_items[item] += 1
                        else:
                            possible_items[item] = 1
                elif word == "Salted":
                    if re.search("salted|salty|salt", order.lower()):
                        if item in possible_items:
                            possible_items[item] += 1
                        else:
                            possible_items[item] = 1
                else:
                    if re.search(word.lower(), order.lower()):
                        if item in possible_items:
                            possible_items[item] += 1
                        else:
                            possible_items[item] = 1
        max_value = max(possible_items.values(), default=0)
        probable_items = [key for key, val in possible_items.items() if val == max_value]
        # probable_item = ""
        # if len(probable_items) == 1:
        #    probable_item = probable_items[0]
        return probable_items

    def handle_exception(self, items, default="default"):
        print()
        print("Your order is missing something required to make a sandwich or have chosen an invalid item! Here are a "
              "list of valid choices you must choose\nfrom to finish your order: ")
        print(list(items))
        print()
        if "White" in list(items):
            order = input("Press enter to choose the default bread option for this sandwich or type in your choice "
                          "from the above choices?\n")
        elif "Chipotle" in list(items):
            order = input("Press enter to choose the default spread option for this sandwich or type in your choice "
                          "from the above choices?\n")
        else:
            order = input("Type in the name of a valid sandwich from the above choices:\n")
        if order == "":
            if default != "default":
                return [default]
            else:
                return []
        else:
            return self.parse_input_helper(order, items)

    def parse_input(self, order):
        filtered_order = []
        stop_words = ['please', 'thanks', 'thank', 'you', 'with', 'the', 'i', 'want', 'the', 'sandwich']
        for word in order.lower().split():
            if word.lower() not in stop_words:
                filtered_order.append(word)
        probable_menu_item = self.parse_input_helper(order, Menu().get_menu_items())
        while len(probable_menu_item) != 1:
            probable_menu_item = self.handle_exception(Menu().get_menu_items())
        menu_item = probable_menu_item[0]
        probable_bread_type = self.parse_input_helper(order, Menu().get_bread_types())
        while len(probable_bread_type) != 1:
            probable_bread_type = self.handle_exception(Menu().get_bread_types(), Menu().get_default_breads(menu_item))
        bread_item = probable_bread_type[0]
        probable_spread_options = self.parse_input_helper(order, Menu().get_spread_options())
        while len(probable_spread_options) == 0:
            probable_spread_options = self.handle_exception(Menu().get_spread_options(),
                                                            Menu().get_default_spreads(menu_item))
        probable_options = self.parse_input_helper(order, Menu().get_options(), ",")
        exceptions = re.search("hold|minus|no|without", order.lower())
        exceptions_list = []
        received_exceptions = Menu().get_exceptions()
        received_exceptions_lower = [x.lower() for x in received_exceptions]
        usual_ingredients = Menu().get_usual_ingredients(menu_item)
        usual_ingredients_lower = [x.lower() for x in usual_ingredients]
        if exceptions:
            index = filtered_order.index(exceptions.group(0))
            for i in range(index + 1, len(filtered_order)):
                for elem in range(len(received_exceptions_lower)):
                    if filtered_order[i] == received_exceptions_lower[elem]:
                        for item in range(len(usual_ingredients_lower)):
                            if filtered_order[i] == usual_ingredients_lower[item]:
                                exceptions_list.append(usual_ingredients_lower[item])
        print()
        print("Your Final Order Details:")
        print("Name:", menu_item)
        print("Usual Ingredients:", Menu().get_usual_ingredients(menu_item))
        print("Bread:", bread_item)
        print("Spreads:", probable_spread_options)
        print("Options:", probable_options)
        print("Exceptions:", exceptions_list)


def main():
    yes_equivalents = ["yes", "yep", "yup", "yeah", "y"]
    no_equivalents = ["nope", "no", "nah", "n"]
    CustomerInteraction().greet_customer()
    order = input("What do you want to eat?\n")
    if re.search("options|menu|choices", order.lower()):
        print()
        Menu().create_menu()
        print()
        order_decision = input("What would you like to eat?\n")
        CustomerInteraction().parse_input(order_decision)
    else:
        CustomerInteraction().parse_input(order)
    print()
    correct = input("Is the above final order correct?\n")
    if correct.lower() in yes_equivalents:
        print()
        print("Thank you for your order. We'll get to making it right away!")
    while correct.lower() in no_equivalents:
        print()
        print("Let's re-do your order.")
        new_order_decision = input("What do you want to eat?\n")
        if re.search("options|menu|choices", new_order_decision.lower()):
            print()
            Menu().create_menu()
            print()
            order_decision_new = input("What would you like to eat?\n")
            CustomerInteraction().parse_input(order_decision_new)
            print()
            correct = input("Is the above final order correct?\n")
            if correct.lower() in yes_equivalents:
                print()
                print("Thank you for your order. We'll get to making it right away!")
        else:
            print()
            CustomerInteraction().parse_input(new_order_decision)
            correct = input("Is the above final order correct?\n")
            if correct.lower() in yes_equivalents:
                print()
                print("Thank you for your order. We'll get to making it right away!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
