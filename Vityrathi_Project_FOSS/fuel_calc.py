"""
Module: fuel_calc.py
Purpose: Estimate aircraft flight range based on fuel parameters.

This module handles:
- Fuel data input
- Range calculation based on consumption formulas
- Database storage of flight estimates
- Viewing history of fuel calculations
"""

import sqlite3

# ------------------------------------------------------ #
# Database Connection Utility
# ------------------------------------------------------ #
def get_db():
    #Returns a connection to the fuel database.
    return sqlite3.connect("databases/fuel.db")


# ------------------------------------------------------ #
# Initialize database tables
# ------------------------------------------------------ #
def init_db():
    #Creates fuel log tables if they do not exist.
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fueldata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fuel_capacity REAL,
        burn_rate REAL,
        cruising_speed REAL,
        estimated_range REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


# ------------------------------------------------------ #
# Fuel & Range Calculation
# ------------------------------------------------------ #
def calculate_range():
    #Calculates aircraft range using basic fuel model with error handling.

    # ---- Fuel input validation ---- #
    while True:
        fuel_input = input("Enter total fuel onboard (kg): ").strip()
        try:
            fuel = float(fuel_input)
            if fuel <= 0:
                print("Fuel must be a positive numeric value.")
                continue
            break
        except:
            print("Enter a valid numeric value for fuel.")

    # ---- Burn rate validation ---- #
    while True:
        burn_input = input("Enter fuel burn rate (kg/hour): ").strip()
        try:
            burn = float(burn_input)
            if burn <= 0:
                print("Burn rate must be positive.")
                continue
            break
        except:
            print("Enter a valid numeric value for burn rate.")

    # ---- Speed validation ---- #
    while True:
        speed_input = input("Enter cruising speed (km/h): ").strip()
        try:
            speed = float(speed_input)
            if speed <= 0:
                print("Speed must be positive.")
                continue
            break
        except:
            print("Enter a valid numeric value for speed.")

    # ---- Date validation ---- #
    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()
        if len(date) == 10 and date[4] == '-' and date[7] == '-':
            break
        else:
            print("Invalid date format. Use YYYY-MM-DD.")

    # ---- Endurance calculation ---- #
    try:
        endurance = fuel / burn  # hours
        flight_range = endurance * speed  # km
    except Exception as e:
        print("Error in calculation:", e)
        return

    # ---- Database recording ---- #
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fueldata (fuel_capacity, burn_rate, cruising_speed, estimated_range, date) VALUES (?, ?, ?, ?, ?)",
            (fuel, burn, speed, flight_range, date)
        )
        conn.commit()
        conn.close()

        print(f"\n Estimated range = {flight_range:.2f} km")
    except Exception as e:
        print("Database Error:", e)


# ------------------------------------------------------ #
# View range calculation history
# ------------------------------------------------------ #
def view_range_logs():
    #Shows historical fuel & range computations.
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fueldata")
        rows = cursor.fetchall()
        conn.close()

        if len(rows) == 0:
            print("No entries found in fuel database.")
        else:
            print("\nFuel & Range History:")
            for row in rows:
                print(row)

    except Exception as e:
        print("Database Error:", e)


# ------------------------------------------------------ #
# Module Menu
# ------------------------------------------------------ #
def run_fuel_calc():
    #Runs the fuel calculation module.
    init_db()
    while True:
        print("\n--- Fuel & Range Module ---")
        print("1. Calculate Flight Range")
        print("2. View Range Calculation History")
        print("3. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        # Numeric check
        if not choice.isdigit():
            print("Enter a number between 1–3.")
            continue

        choice = int(choice)

        if choice == 1:
            calculate_range()
        elif choice == 2:
            view_range_logs()
        elif choice == 3:
            break
        else:
            print("Invalid selection, try again.")