import os

WIDTH = 78


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def top():
    print("┌" + "─" * WIDTH + "┐")


def middle():
    print("├" + "─" * WIDTH + "┤")


def bottom():
    print("└" + "─" * WIDTH + "┘")


def line(text=""):
    text = str(text)
    text = text[:WIDTH]
    print("│" + text.ljust(WIDTH) + "│")


def title(text):
    line(text.center(WIDTH))


def draw_screen(title_text, content):
    clear()

    top()
    title("FUEL INVENTORY MANAGEMENT SYSTEM")
    middle()
    title(title_text)
    middle()

    for item in content:
        line(item)

    remaining = 12 - len(content)

    for _ in range(max(0, remaining)):
        line()

    middle()
    line("Q = Quit | B = Back")
    bottom()


def inventory_menu():
    while True:
        draw_screen(
            "INVENTORY MANAGEMENT",
            [
                "1. View Items",
                "2. Add Item",
                "3. Update Item",
                "4. Delete Item",
                "",
                "Currently using demo data...",
            ],
        )

        choice = input("\nChoice: ").strip().upper()

        if choice == "B":
            return

        if choice == "1":
            view_items()


def view_items():
    items = [[1, "Petrol", 5000], [2, "Diesel", 3500], [3, "2T Oil", 120]]

    clear()

    top()
    title("ITEM LIST")
    middle()

    line(f"{'ID':<10}{'NAME':<30}{'STOCK':>20}")
    middle()

    for item_id, name, stock in items:
        line(f"{item_id:<10}{name:<30}{stock:>20}")

    bottom()

    input("\nPress Enter to continue...")


def main_menu():
    while True:
        draw_screen(
            "MAIN MENU",
            [
                "1. Inventory Management",
                "2. Supplier Management",
                "3. Purchase Management",
                "4. Sales Management",
                "5. Reports",
                "",
                "Welcome to Fuel Inventory Management System",
            ],
        )

        choice = input("\nChoice: ").strip().upper()

        if choice == "1":
            inventory_menu()

        elif choice == "Q":
            break


if __name__ == "__main__":
    main_menu()
