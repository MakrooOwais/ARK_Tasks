import pandas as pd

menu = """Please select an option!!
'g': Get a drink.
'REFILL': Restock.
's': Print the menu.
'q': Quit!"""


class VendingMachine:
    drinks_dictioinary = {
    "Code": ["PEPS", "MDEW", "DPEP", "COKE", "GATO", "DCOK", "MINM", "TROP"],
    "Name": [
        "Pepsi",
        "Mountain Dew",
        "Doctor Pepper",
        "Coke",
        "Gatorade",
        "Diet Coke",
        "Minute Maid",
        "Tropicana",
    ],
    "Cost": [30, 30, 50, 20, 20, 30, 25, 30],
    "Stock": [0, 0, 0, 0, 0, 0, 0, 0],
}
    def __init__(self) -> None:
        self.drinks = pd.DataFrame(VendingMachine.drinks_dictioinary)
        self.refill()
        self.max_name_length = 13

    def refill(self, new_stock: int = 50) -> None:
        self.drinks.Stock = new_stock
        print("Refill Successful!!")

    def change_stock(self, code: str, new_stock: int) -> None:
        self.drinks.loc[self.drinks["Code"] == code, "Stock"] = new_stock
        while new_stock == 0:
            print(
                f"Stock of {self.drinks.loc[self.drinks['Code'] == code, 'Name'].values[0]} is EXHAUSTED!!"
            )
            break

    def get_cost(self, code: str) -> int:
        return self.drinks.loc[self.drinks["Code"] == code, 'Cost'].values[0]

    def get_stock(self, code: str) -> int:
        return self.drinks.loc[self.drinks["Code"] == code, 'Stock'].values[0]

    def __str__(self) -> str:
        return_string: str = (
            "Code".ljust(6, " ")
            + "Name".ljust(self.max_name_length + 3, " ")
            + "Cost".ljust(5, " ")
            + "\n"
        )
        for _, drink in self.drinks.iterrows():
            while drink["Stock"]:
                return_string = (
                    return_string
                    + drink["Code"].ljust(6, " ")
                    + drink["Name"].ljust(self.max_name_length + 3, " ")
                    + str(drink["Cost"]).ljust(5, " ")
                    + "\n"
                )
                break

        return return_string

    def get_drink(self):
        while (
            code := input("Enter the code (NOT case sensitive.): ").upper()
        ) not in VendingMachine.drinks_dictioinary["Code"]:
            print("The entered key was not recognized!! Please try again...")

        current_stock: int = self.get_stock(code)

        while current_stock:
            cost: int = self.get_cost(code)
            while (amount := int(input("Enter the amount: "))) < cost:
                print("Insufficicent funds!! Please try again...")

            self.change_stock(code, current_stock - 1)
            pr_str = f"Here is your {self.drinks.loc[self.drinks['Code'] == code, 'Name'].values[0]}!!"
            while amount - cost > 0:
                pr_str = pr_str + f" And the change of {amount - cost}"
                break

            print(pr_str)
            return
        
        print("The requested drink is out of stock!! Please try again...")
        self.get_drink()


vm_1 = VendingMachine()

menu_options: dict[str, callable] = {  # type: ignore
    "g": vm_1.get_drink,
    "REFILL": vm_1.refill,
    "q": quit,
    "s": lambda: print(vm_1),
}


def main() -> None:
    print(menu)
    while (option := input("Enter the key: ")) in menu_options.keys():
        menu_options[option]()
    print("The entered key was not recognised!! Please try again...")
    main()


if __name__ == "__main__":
    main()
