import os
import datetime
import mysql.connector
from mysql.connector import errorcode

WIDTH = 96
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "FuelInventoryDB",
}


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def top():
    print("╭" + "─" * WIDTH + "╮")


def middle():
    print("├" + "─" * WIDTH + "┤")


def bottom():
    print("╰" + "─" * WIDTH + "╯")


def line(text=""):
    text = str(text)[:WIDTH]
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
    for _ in range(max(0, 12 - len(content))):
        line()
    middle()
    line("Q = Quit | B = Back")
    bottom()


def pause():
    input("\nPress Enter to continue...")


def format_cell(value):
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def draw_table(headers, rows):
    data = [[format_cell(x) for x in row] for row in rows]

    widths = []
    for i, h in enumerate(headers):
        values = [row[i] if i < len(row) else "" for row in data]
        widths.append(max(len(str(h)), *(len(v) for v in values)) + 2)

    def make_row(left, middle, right, fill):
        return left + middle.join(fill * w for w in widths) + right

    top = make_row("╭", "┬", "╮", "─")
    sep = make_row("├", "┼", "┤", "─")
    bottom = make_row("╰", "┴", "╯", "─")

    lines = [top]

    header = (
        "│"
        + "│".join(str(headers[i]).center(widths[i]) for i in range(len(headers)))
        + "│"
    )

    lines.append(header)
    lines.append(sep)

    for row in data:
        cells = []

        for cell in row:
            try:
                float(cell)
                cells.append(cell.rjust(widths[len(cells)]))
            except ValueError:
                cells.append(cell.ljust(widths[len(cells)]))

        line = "│" + "│".join(cells) + "│"
        lines.append(line)

    lines.append(bottom)

    return lines


def connect_server():
    config = DB_CONFIG.copy()
    config.pop("database", None)
    return mysql.connector.connect(**config)


def connect_database():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            show_error("Access denied. Update database settings.")
            prompt_database_settings()
            return connect_database()
        raise


def execute_query(query, params=None, commit=False):
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute(query, params or ())
    if commit:
        connection.commit()
    return connection, cursor


def execute_non_query(query, params=None):
    connection, cursor = execute_query(query, params, commit=True)
    close_connection(connection, cursor)


def fetch_all(query, params=None):
    connection, cursor = execute_query(query, params)
    rows = cursor.fetchall()
    close_connection(connection, cursor)
    return rows


def fetch_one(query, params=None):
    connection, cursor = execute_query(query, params)
    row = cursor.fetchone()
    close_connection(connection, cursor)
    return row


def close_connection(connection, cursor=None):
    if cursor:
        cursor.close()
    if connection:
        connection.close()


def get_next_id(table, field):
    row = fetch_one(f"SELECT COALESCE(MAX({field}), 0) + 1 FROM {table}")
    return int(row[0]) if row and row[0] is not None else 1


def get_input(prompt, default=None, required=False):
    while True:
        text = input(
            f"{prompt}{' [' + str(default) + ']' if default is not None else ''}: "
        ).strip()
        if text:
            return text
        if default is not None:
            return default
        if not required:
            return ""
        draw_screen("INPUT REQUIRED", ["Please enter a value before continuing."])


def get_int(prompt, default=None, required=False, minimum=None):
    while True:
        value = get_input(prompt, default, required)
        if value == "":
            return None
        try:
            number = int(value)
            if minimum is not None and number < minimum:
                raise ValueError
            return number
        except ValueError:
            draw_screen("INPUT ERROR", ["Please enter a valid whole number."])


def get_float(prompt, default=None, required=False, minimum=None):
    while True:
        value = get_input(prompt, default, required)
        if value == "":
            return None
        try:
            number = float(value)
            if minimum is not None and number < minimum:
                raise ValueError
            return number
        except ValueError:
            draw_screen("INPUT ERROR", ["Please enter a valid number."])


def show_message(title_text, lines):
    draw_screen(title_text, lines)
    pause()


def show_error(message):
    show_message("ERROR", [message])


def prompt_database_settings():
    draw_screen(
        "DATABASE SETTINGS",
        ["Enter database connection details.", "If unsure, ask your administrator."],
    )
    DB_CONFIG["host"] = get_input("Host", default=DB_CONFIG["host"], required=True)
    DB_CONFIG["user"] = get_input("User", default=DB_CONFIG["user"], required=True)
    DB_CONFIG["password"] = input("Password []: ").strip()
    DB_CONFIG["database"] = get_input(
        "Database", default=DB_CONFIG["database"], required=True
    )


def create_schema(cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Categories (categoryid INT PRIMARY KEY, categoryname VARCHAR(50) NOT NULL)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Items (itemid INT PRIMARY KEY, itemname VARCHAR(100) NOT NULL, categoryid INT, unit VARCHAR(30), sellingprice DECIMAL(10,2), FOREIGN KEY(categoryid) REFERENCES Categories(categoryid))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Suppliers (supplierid INT PRIMARY KEY, suppliername VARCHAR(100), phone VARCHAR(20), address VARCHAR(200))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Stock (itemid INT PRIMARY KEY, quantity DECIMAL(12,2), reorderlevel DECIMAL(12,2), FOREIGN KEY(itemid) REFERENCES Items(itemid))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Purchases (purchaseid INT PRIMARY KEY, supplierid INT, purchasedate DATE, totalamount DECIMAL(12,2), FOREIGN KEY(supplierid) REFERENCES Suppliers(supplierid))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS PurchaseDetails (purchasedetailid INT PRIMARY KEY, purchaseid INT, itemid INT, quantity DECIMAL(10,2), rate DECIMAL(10,2), FOREIGN KEY(purchaseid) REFERENCES Purchases(purchaseid), FOREIGN KEY(itemid) REFERENCES Items(itemid))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Sales (saleid INT PRIMARY KEY, itemid INT, saledate DATE, quantitysold DECIMAL(12,2), rate DECIMAL(10,2), totalamount DECIMAL(12,2), FOREIGN KEY(itemid) REFERENCES Items(itemid))"
    )


def initialize_database():
    try:
        connection = connect_database()
        cursor = connection.cursor()
        create_schema(cursor)
        connection.commit()
        close_connection(connection, cursor)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            server = connect_server()
            cursor = server.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
            cursor.execute(f"USE `{DB_CONFIG['database']}`")
            create_schema(cursor)
            server.commit()
            close_connection(server, cursor)
        else:
            raise
    seed_sample_data()


def seed_sample_data():
    count = fetch_one("SELECT COUNT(*) FROM Categories")
    if count and count[0] == 0:
        for values in [(1, "Fuel"), (2, "Lubricant")]:
            execute_non_query(
                "INSERT INTO Categories (categoryid, categoryname) VALUES (%s, %s)",
                values,
            )
        for values in [
            (1, "Petrol", 1, "Litres", 102.50),
            (2, "Diesel", 1, "Litres", 90.20),
            (3, "2T Oil", 2, "Bottle", 150.00),
            (4, "Engine oil", 2, "Bottle", 550.00),
            (5, "Premium petrol", 1, "Litres", 108.75),
            (6, "Gear oil", 2, "Bottle", 320.00),
        ]:
            execute_non_query(
                "INSERT INTO Items (itemid, itemname, categoryid, unit, sellingprice) VALUES (%s, %s, %s, %s, %s)",
                values,
            )
        for values in [
            (1, "Indian oil cooperation", "9876543210", "Kochi"),
            (2, "Bharat petroleum", "9876501234", "Thiruvananthapuram"),
            (3, "Hindustan petroleum", "998776655", "Kozhikode"),
            (4, "Reliance petroleum", "9123456789", "Ernakulam"),
        ]:
            execute_non_query(
                "INSERT INTO Suppliers (supplierid, suppliername, phone, address) VALUES (%s, %s, %s, %s)",
                values,
            )
        for values in [
            (1, 5000.00, 1000.00),
            (2, 3500.00, 800.00),
            (3, 120.00, 25.00),
            (4, 80.00, 20.00),
            (5, 2000.00, 500.00),
            (6, 60.00, 15.00),
        ]:
            execute_non_query(
                "INSERT INTO Stock (itemid, quantity, reorderlevel) VALUES (%s, %s, %s)",
                values,
            )


def table_screen(title_text, headers, rows, pause_after=True):
    content = draw_table(headers, [[str(v) for v in row] for row in rows])

    if pause_after:
        content.append("")
        content.append("Press Enter to continue.")

    draw_screen(title_text, content)

    if pause_after:
        pause()


def view_records(title_text, headers, query, params=None):
    rows = fetch_all(query, params)
    if not rows:
        show_message(title_text, ["No records available."])
        return
    table_screen(title_text, headers, rows)


def choose_category(default=None):
    categories = fetch_all(
        "SELECT categoryid, categoryname FROM Categories ORDER BY categoryid"
    )
    if categories:
        table_screen("CATEGORIES", ["ID", "Name"], categories, pause_after=False)
        return get_int("Select category ID", default=default)
    return default


def add_item():
    name = get_input("Item name", required=True)
    category_id = choose_category()
    unit = get_input("Unit", default="Litres", required=True)
    price = get_float("Selling price", required=True, minimum=0)
    quantity = get_float("Initial stock quantity", default=0, minimum=0)
    reorder = get_float("Reorder level", default=0, minimum=0)
    item_id = get_next_id("Items", "itemid")
    execute_non_query(
        "INSERT INTO Items (itemid, itemname, categoryid, unit, sellingprice) VALUES (%s, %s, %s, %s, %s)",
        (item_id, name, category_id, unit, price),
    )
    execute_non_query(
        "INSERT INTO Stock (itemid, quantity, reorderlevel) VALUES (%s, %s, %s)",
        (item_id, quantity, reorder),
    )
    show_message("ITEM ADDED", [f"Item '{name}' has been added to inventory."])


def update_item():
    table_screen(
        "ITEM LIST",
        ["ID", "Name"],
        fetch_all("SELECT itemid,itemname FROM Items ORDER BY itemid"),
        pause_after=False,
    )
    item_id = get_int("Item ID to update", required=True, minimum=1)
    item = fetch_one(
        "SELECT itemname, categoryid, unit, sellingprice FROM Items WHERE itemid = %s",
        (item_id,),
    )
    if not item:
        show_error("Item not found.")
        return
    name, category_id, unit, price = item
    stock = fetch_one(
        "SELECT quantity, reorderlevel FROM Stock WHERE itemid = %s", (item_id,)
    )
    reorder = stock[1] if stock else 0
    name = get_input("Item name", default=name, required=True)
    category_id = choose_category(default=category_id)
    unit = get_input("Unit", default=unit, required=True)
    price = get_float("Selling price", default=price, minimum=0)
    reorder = get_float("Reorder level", default=reorder, minimum=0)
    execute_non_query(
        "UPDATE Items SET itemname = %s, categoryid = %s, unit = %s, sellingprice = %s WHERE itemid = %s",
        (name, category_id, unit, price, item_id),
    )
    if stock:
        execute_non_query(
            "UPDATE Stock SET reorderlevel = %s WHERE itemid = %s", (reorder, item_id)
        )
    else:
        execute_non_query(
            "INSERT INTO Stock (itemid, quantity, reorderlevel) VALUES (%s, %s, %s)",
            (item_id, 0, reorder),
        )
    show_message("ITEM UPDATED", [f"Item '{name}' has been updated."])


def delete_item():
    table_screen(
        "ITEM LIST",
        ["ID", "Name"],
        fetch_all("SELECT itemid,itemname FROM Items ORDER BY itemid"),
        pause_after=False,
    )

    item_id = get_int("Item ID to delete", required=True, minimum=1)
    item = fetch_one("SELECT itemname FROM Items WHERE itemid = %s", (item_id,))
    if not item:
        show_error("Item not found.")
        return
    name = item[0]
    try:
        execute_non_query("DELETE FROM Stock WHERE itemid = %s", (item_id,))
        execute_non_query("DELETE FROM Items WHERE itemid = %s", (item_id,))
        show_message("ITEM DELETED", [f"Item '{name}' has been removed."])
    except mysql.connector.Error:
        show_error("Unable to delete item. It may be used in existing records.")


def add_supplier():
    name = get_input("Supplier name", required=True)
    phone = get_input("Phone", required=True)
    address = get_input("Address", required=True)
    supplier_id = get_next_id("Suppliers", "supplierid")
    execute_non_query(
        "INSERT INTO Suppliers (supplierid, suppliername, phone, address) VALUES (%s, %s, %s, %s)",
        (supplier_id, name, phone, address),
    )
    show_message("SUPPLIER ADDED", [f"Supplier '{name}' has been added."])


def update_supplier():
    table_screen(
        "SUPPLIER LIST",
        ["ID", "Name"],
        fetch_all("SELECT supplierid, suppliername FROM Suppliers ORDER BY supplierid"),
        pause_after=False,
    )

    supplier_id = get_int("Supplier ID to update", required=True, minimum=1)
    supplier = fetch_one(
        "SELECT suppliername, phone, address FROM Suppliers WHERE supplierid = %s",
        (supplier_id,),
    )
    if not supplier:
        show_error("Supplier not found.")
        return
    name, phone, address = supplier
    name = get_input("Supplier name", default=name, required=True)
    phone = get_input("Phone", default=phone, required=True)
    address = get_input("Address", default=address, required=True)
    execute_non_query(
        "UPDATE Suppliers SET suppliername = %s, phone = %s, address = %s WHERE supplierid = %s",
        (name, phone, address, supplier_id),
    )
    show_message("SUPPLIER UPDATED", [f"Supplier '{name}' has been updated."])


def delete_supplier():
    table_screen(
        "SUPPLIER LIST",
        ["ID", "Name"],
        fetch_all("SELECT supplierid, suppliername FROM Suppliers ORDER BY supplierid"),
        pause_after=False,
    )

    supplier_id = get_int("Supplier ID to delete", required=True, minimum=1)
    supplier = fetch_one(
        "SELECT suppliername FROM Suppliers WHERE supplierid = %s", (supplier_id,)
    )
    if not supplier:
        show_error("Supplier not found.")
        return
    name = supplier[0]
    try:
        execute_non_query("DELETE FROM Suppliers WHERE supplierid = %s", (supplier_id,))
        show_message("SUPPLIER DELETED", [f"Supplier '{name}' has been removed."])
    except mysql.connector.Error:
        show_error("Unable to delete supplier. It may be used in existing records.")


def add_purchase():
    suppliers = fetch_all(
        "SELECT supplierid, suppliername FROM Suppliers ORDER BY supplierid"
    )
    if not suppliers:
        show_error("No suppliers found. Add a supplier first.")
        return
    table_screen("SUPPLIERS", ["ID", "Name"], suppliers, pause_after=False)
    supplier_id = get_int("Supplier ID", required=True, minimum=1)
    if not fetch_one(
        "SELECT suppliername FROM Suppliers WHERE supplierid = %s", (supplier_id,)
    ):
        show_error("Supplier not found.")
        return
    purchase_id = get_next_id("Purchases", "purchaseid")
    purchase_date = datetime.date.today().isoformat()
    total_amount = 0.0
    details = []
    detail_id = get_next_id("PurchaseDetails", "purchasedetailid")
    while True:
        items = fetch_all(
            "SELECT itemid, itemname, sellingprice FROM Items ORDER BY itemid"
        )
        if not items:
            show_error("No items available to purchase.")
            return
        table_screen("ITEMS", ["ID", "Name", "Price"], items, pause_after=False)
        item_id = get_int("Item ID", required=True, minimum=1)
        item = fetch_one(
            "SELECT itemname, sellingprice FROM Items WHERE itemid = %s", (item_id,)
        )
        if not item:
            show_error("Item not found.")
            continue
        quantity = get_float("Quantity", required=True, minimum=1)
        rate = get_float("Rate", default=item[1], required=True, minimum=0)
        total_amount += quantity * rate
        details.append((detail_id, purchase_id, item_id, quantity, rate))
        detail_id += 1
        if input("Add another item? (Y/N): ").strip().upper() != "Y":
            break
    execute_non_query(
        "INSERT INTO Purchases (purchaseid, supplierid, purchasedate, totalamount) VALUES (%s, %s, %s, %s)",
        (purchase_id, supplier_id, purchase_date, total_amount),
    )
    for purchasedetailid, purchaseid, itemid, quantity, rate in details:
        execute_non_query(
            "INSERT INTO PurchaseDetails (purchasedetailid, purchaseid, itemid, quantity, rate) VALUES (%s, %s, %s, %s, %s)",
            (purchasedetailid, purchaseid, itemid, quantity, rate),
        )
        if fetch_one("SELECT quantity FROM Stock WHERE itemid = %s", (itemid,)):
            execute_non_query(
                "UPDATE Stock SET quantity = quantity + %s WHERE itemid = %s",
                (quantity, itemid),
            )
        else:
            execute_non_query(
                "INSERT INTO Stock (itemid, quantity, reorderlevel) VALUES (%s, %s, %s)",
                (itemid, quantity, 0),
            )
    show_message("PURCHASE SAVED", [f"Purchase {purchase_id} has been recorded."])


def add_sale():
    items = fetch_all(
        "SELECT I.itemid, I.itemname, I.sellingprice, COALESCE(S.quantity, 0) FROM Items I LEFT JOIN Stock S ON I.itemid = S.itemid ORDER BY I.itemid"
    )
    if not items:
        show_error("No items found. Add inventory items first.")
        return
    table_screen(
        "ITEM STOCK", ["ID", "Name", "Price", "Stock"], items, pause_after=False
    )
    item_id = get_int("Item ID", required=True, minimum=1)
    item = fetch_one(
        "SELECT I.itemname, I.sellingprice, COALESCE(S.quantity, 0) FROM Items I LEFT JOIN Stock S ON I.itemid = S.itemid WHERE I.itemid = %s",
        (item_id,),
    )
    if not item:
        show_error("Item not found.")
        return
    name, price, stock_qty = item
    if stock_qty <= 0:
        show_error("Stock is not available for this item.")
        return
    quantity = get_float("Quantity sold", required=True, minimum=1)
    if quantity > stock_qty:
        show_error("Not enough stock for this sale.")
        return
    rate = get_float("Price per unit", default=price, required=True, minimum=0)
    total = quantity * rate
    sale_id = get_next_id("Sales", "saleid")
    sale_date = datetime.date.today().isoformat()
    execute_non_query(
        "INSERT INTO Sales (saleid, itemid, saledate, quantitysold, rate, totalamount) VALUES (%s, %s, %s, %s, %s, %s)",
        (sale_id, item_id, sale_date, quantity, rate, total),
    )
    execute_non_query(
        "UPDATE Stock SET quantity = quantity - %s WHERE itemid = %s",
        (quantity, item_id),
    )
    show_message("SALE SAVED", [f"Sale {sale_id} has been recorded."])


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
                "Use inventory options to manage fuel stock.",
            ],
        )
        choice = input("\nChoice: ").strip().upper()
        if choice == "1":
            view_records(
                "ITEM LIST",
                ["ID", "Name", "Stock", "Unit", "Price", "Reorder"],
                "SELECT I.itemid, I.itemname, COALESCE(S.quantity, 0), I.unit, I.sellingprice, COALESCE(S.reorderlevel, 0) FROM Items I LEFT JOIN Stock S ON I.itemid = S.itemid ORDER BY I.itemid",
            )
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "B":
            return
        elif choice == "Q":
            exit()


def supplier_menu():
    while True:
        draw_screen(
            "SUPPLIER MANAGEMENT",
            [
                "1. View Suppliers",
                "2. Add Supplier",
                "3. Update Supplier",
                "4. Delete Supplier",
                "",
                "Use supplier options to track vendors.",
            ],
        )
        choice = input("\nChoice: ").strip().upper()
        if choice == "1":
            view_records(
                "SUPPLIER LIST",
                ["ID", "Name", "Phone", "Address"],
                "SELECT supplierid, suppliername, phone, address FROM Suppliers ORDER BY supplierid",
            )
        elif choice == "2":
            add_supplier()
        elif choice == "3":
            update_supplier()
        elif choice == "4":
            delete_supplier()
        elif choice == "B":
            return
        elif choice == "Q":
            exit()


def purchase_menu():
    while True:
        draw_screen(
            "PURCHASE MANAGEMENT",
            [
                "1. New Purchase",
                "2. Purchase History",
                "",
                "Use purchase options to record fuel purchases.",
            ],
        )
        choice = input("\nChoice: ").strip().upper()
        if choice == "1":
            add_purchase()
        elif choice == "2":
            view_records(
                "PURCHASE HISTORY",
                ["ID", "Supplier", "Date", "Total"],
                "SELECT P.purchaseid, S.suppliername, P.purchasedate, P.totalamount FROM Purchases P INNER JOIN Suppliers S ON P.supplierid = S.supplierid ORDER BY P.purchasedate",
            )
        elif choice == "B":
            return
        elif choice == "Q":
            exit()


def sales_menu():
    while True:
        draw_screen(
            "SALES MANAGEMENT",
            [
                "1. New Sale",
                "2. Sales History",
                "",
                "Use sales options to record fuel sales.",
            ],
        )
        choice = input("\nChoice: ").strip().upper()
        if choice == "1":
            add_sale()
        elif choice == "2":
            view_records(
                "SALES HISTORY",
                ["ID", "Item", "Date", "Qty", "Rate", "Total"],
                "SELECT S.saleid, I.itemname, S.saledate, S.quantitysold, S.rate, S.totalamount FROM Sales S INNER JOIN Items I ON S.itemid = I.itemid ORDER BY S.saledate",
            )
        elif choice == "B":
            return
        elif choice == "Q":
            exit()


def inventory_report():
    view_records(
        "INVENTORY REPORT",
        ["ID", "Item", "Stock", "Unit", "Price", "Value"],
        """
        SELECT
            I.itemid,
            I.itemname,
            S.quantity,
            I.unit,
            I.sellingprice,
            S.quantity * I.sellingprice
        FROM Items I
        JOIN Stock S ON I.itemid=S.itemid
        ORDER BY I.itemid
        """,
    )


def low_stock_report():
    view_records(
        "LOW STOCK REPORT",
        ["ID", "Item", "Stock", "Reorder"],
        """
        SELECT
            I.itemid,
            I.itemname,
            S.quantity,
            S.reorderlevel
        FROM Items I
        JOIN Stock S
        ON I.itemid=S.itemid
        WHERE S.quantity <= S.reorderlevel
        ORDER BY I.itemid
        """,
    )


def sales_report():
    view_records(
        "SALES REPORT",
        ["Sale", "Item", "Date", "Qty", "Rate", "Total"],
        """
        SELECT
            Sa.saleid,
            I.itemname,
            Sa.saledate,
            Sa.quantitysold,
            Sa.rate,
            Sa.totalamount
        FROM Sales Sa
        JOIN Items I
        ON Sa.itemid=I.itemid
        ORDER BY Sa.saledate DESC
        """,
    )


def purchase_report():
    view_records(
        "PURCHASE REPORT",
        ["Purchase", "Supplier", "Date", "Total"],
        """
        SELECT
            P.purchaseid,
            S.suppliername,
            P.purchasedate,
            P.totalamount
        FROM Purchases P
        JOIN Suppliers S
        ON P.supplierid=S.supplierid
        ORDER BY P.purchasedate DESC
        """,
    )


def reports_menu():
    while True:
        draw_screen(
            "REPORTS",
            [
                "1. Inventory Report",
                "2. Purchase Report",
                "3. Sales Report",
                "4. Low Stock Report",
                "",
                "Choose a report.",
            ],
        )

        choice = input("\nChoice: ").strip().upper()

        if choice == "1":
            inventory_report()

        elif choice == "2":
            purchase_report()

        elif choice == "3":
            sales_report()

        elif choice == "4":
            low_stock_report()

        elif choice == "B":
            return

        elif choice == "Q":
            exit()


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
                "Choose an option to continue.",
            ],
        )
        choice = input("\nChoice: ").strip().upper()
        if choice == "1":
            inventory_menu()
        elif choice == "2":
            supplier_menu()
        elif choice == "3":
            purchase_menu()
        elif choice == "4":
            sales_menu()
        elif choice == "5":
            reports_menu()
        elif choice == "Q":
            break


if __name__ == "__main__":
    initialize_database()
    main_menu()
