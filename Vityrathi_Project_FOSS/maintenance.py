"""
Module: maintenance.py
Purpose: Manage aircraft database, store maintenance logs, view service history.

This module handles:
- Aircraft registration
- Maintenance logging
- Maintenance history retrieval
- Searching aircraft
- Filtering records by date/engineer
"""

import sqlite3

# ------------------------------------------------------ #
# Database Connection Utility
# ------------------------------------------------------ #
def get_db():
    """Returns a connection to the maintenance database."""
    return sqlite3.connect("databases/maintenance.db")


# ------------------------------------------------------ #
# Initialize database tables
# ------------------------------------------------------ #
def init_db():
    """Creates required tables if they do not already exist."""
    conn = get_db()
    cursor = conn.cursor()

    # Table of aircraft
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aircraft (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        model TEXT NOT NULL,
        manufacture_year INTEGER
    )
    """)

    # Table of maintenance logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintenance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aircraft_id INTEGER,
        description TEXT,
        date TEXT,
        engineer TEXT,
        cost REAL,
        status TEXT,
        FOREIGN KEY (aircraft_id) REFERENCES aircraft(id)
    )
    """)

    conn.commit()
    conn.close()


# ------------------------------------------------------ #
# Aircraft Functions
# ------------------------------------------------------ #
def add_aircraft():
    """Adds a new aircraft to the database with error handling."""

    # ---- Name validation ---- #
    while True:
        name = input("Enter aircraft name: ").strip()
        if name == "":
            print("Aircraft name cannot be empty.")
        else:
            break

    # ---- Model validation ---- #
    while True:
        model = input("Enter model: ").strip()
        if model == "":
            print("Model cannot be empty.")
        else:
            break

    # ---- Year validation ---- #
    while True:
        year = input("Enter manufacture year: ").strip()
        if not year.isdigit():
            print("Manufacture year must be a numeric value.")
            continue
        year = int(year)
        if year < 1950 or year > 2025:
            print("Enter a realistic year between 1950–2025.")
        else:
            break

    # ---- Insert into DB ---- #
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO aircraft (name, model, manufacture_year) VALUES (?, ?, ?)",
                       (name, model, year))
        conn.commit()
        conn.close()
        print("Aircraft added successfully.")

    except Exception as e:
        print("Database Error:", e)


def search_aircraft():
    """Search aircraft by name or model with error handling."""
    
    keyword = input("Enter search keyword: ").strip()
    if keyword == "":
        print("Search keyword cannot be empty.")
        return

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aircraft WHERE name LIKE ? OR model LIKE ?", 
                       (f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()
        conn.close()

        if len(rows) == 0:
            print("No matching aircraft found.")
        else:
            print("\nSearch Results:")
            for row in rows:
                print(row)
    except Exception as e:
        print("Database Error:", e)


def view_aircraft():
    """Displays all aircraft records with empty DB check."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aircraft")
        rows = cursor.fetchall()
        conn.close()

        if len(rows) == 0:
            print("No aircraft registered yet.")
        else:
            print("\nRegistered Aircraft:")
            for row in rows:
                print(row)
    except Exception as e:
        print("Database Error:", e)


# ------------------------------------------------------ #
# Maintenance Logging Functions
# ------------------------------------------------------ #
def log_maintenance():
    """Logs a maintenance record for an aircraft with validation."""

    # ---- Validate aircraft ID ---- #
    while True:
        aircraft_id = input("Enter aircraft ID: ").strip()
        if not aircraft_id.isdigit():
            print("Aircraft ID must be numeric.")
            continue

        # Check if ID exists
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aircraft WHERE id = ?", (aircraft_id,))
        exists = cursor.fetchone()
        conn.close()

        if exists is None:
            print("No aircraft exists with that ID.")
        else:
            aircraft_id = int(aircraft_id)
            break

    # ---- Description ---- #
    while True:
        desc = input("Enter maintenance description: ").strip()
        if desc == "":
            print("Description cannot be empty.")
        else:
            break

    # ---- Date format check ---- #
    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()
        if len(date) == 10 and date[4] == '-' and date[7] == '-':
            break
        else:
            print("Invalid date format. Use YYYY-MM-DD.")

    # ---- Engineer name ---- #
    while True:
        eng = input("Enter engineer name: ").strip()
        if eng == "":
            print("Engineer name cannot be empty.")
        else:
            break

    # ---- Cost ---- #
    while True:
        cost = input("Enter repair cost (₹): ").strip()
        try:
            cost = float(cost)
            if cost < 0:
                print("Cost must be positive.")
            else:
                break
        except ValueError:
            print("Enter a valid number for cost.")

    # ---- Status ---- #
    while True:
        status = input("Enter maintenance status (Completed/Pending): ").strip().lower()
        if status not in ("completed", "pending"):
            print("Status must be either 'Completed' or 'Pending'.")
        else:
            break

    # ---- Insert record ---- #
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO maintenance (aircraft_id, description, date, engineer, cost, status) VALUES (?, ?, ?, ?, ?, ?)",
            (aircraft_id, desc, date, eng, cost, status)
        )
        conn.commit()
        conn.close()

        print("Maintenance record added.")
    except Exception as e:
        print("Database Error:", e)


def view_maintenance():
    """Displays full maintenance logs for all aircraft."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM maintenance")
        rows = cursor.fetchall()
        conn.close()

        if len(rows) == 0:
            print("No maintenance records found.")
        else:
            print("\nMaintenance Records:")
            for row in rows:
                print(row)
    except Exception as e:
        print("Database Error:", e)


def view_maintenance_by_aircraft():
    """Displays maintenance logs filtered by aircraft ID with validation."""

    while True:
        aircraft_id = input("Enter aircraft ID: ").strip()
        if not aircraft_id.isdigit():
            print("ID must be numeric.")
        else:
            aircraft_id = int(aircraft_id)
            break

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM maintenance WHERE aircraft_id = ?", (aircraft_id,))
        rows = cursor.fetchall()
        conn.close()

        if len(rows) == 0:
            print("No maintenance records for this aircraft.")
        else:
            print("\nMaintenance Records for Aircraft ID", aircraft_id)
            for row in rows:
                print(row)
    except Exception as e:
        print("Database Error:", e)


# ------------------------------------------------------ #
# Module Menu
# ------------------------------------------------------ #
def run_maintenance():
    """Runs the maintenance system menu."""
    init_db()
    while True:
        print("\n--- Aircraft Maintenance Module ---")
        print("1. Add Aircraft")
        print("2. Search Aircraft")
        print("3. View Aircraft List")
        print("4. Add Maintenance Record")
        print("5. View All Maintenance Records")
        print("6. View Maintenance Records for Specific Aircraft")
        print("7. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            add_aircraft()
        elif choice == '2':
            search_aircraft()
        elif choice == '3':
            view_aircraft()
        elif choice == '4':
            log_maintenance()
        elif choice == '5':
            view_maintenance()
        elif choice == '6':
            view_maintenance_by_aircraft()
        elif choice == '7':
            break
        else:
            print("Invalid input, please try again.")
