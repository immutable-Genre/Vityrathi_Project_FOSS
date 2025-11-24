"""
Module: weather.py
Purpose: Record weather conditions & evaluate takeoff clearance.

This module handles:
- Weather data recording
- Clearance decision based on aviation safety thresholds
- Viewing historical weather conditions
- Filtering by clearance decisions
"""

import sqlite3

# ------------------------------------------------------ #
# Database Connection Utility
# ------------------------------------------------------ #
def get_db():
    # Returns a connection to the weather database.
    return sqlite3.connect("databases/weather.db")


# ------------------------------------------------------ #
# Initialize database tables
# ------------------------------------------------------ #
def init_db():
    # Creates weather tables if they do not exist.
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wind_speed REAL,
        temperature REAL,
        humidity REAL,
        visibility REAL,
        date TEXT,
        clearance TEXT
    )
    """)

    conn.commit()
    conn.close()


# ------------------------------------------------------ #
# Aviation Safety Logic
# ------------------------------------------------------ #
def evaluate_clearance(wind, temp, humidity, vis):
    """
    Determines whether takeoff is allowed.

    Rules:
    - wind speed must be < 35 knots
    - visibility must be > 3 km
    - temperature must be within -20°C to +50°C
    - humidity under 90% preferred
    """
    if wind > 35:
        return "NO - High wind"
    if vis < 3:
        return "NO - Low visibility"
    if temp < -20 or temp > 50:
        return "NO - Unsafe temperature"
    if humidity > 95:
        return "NO - High humidity risk"

    return "YES - Cleared for takeoff"


# ------------------------------------------------------ #
# Weather Recording
# ------------------------------------------------------ #
def record_weather():
    # Receives the weather data and stores it in database with error handling.

    # Wind speed input validation
    while True:
        wind_input = input("Enter wind speed (knots): ").strip()
        try:
            wind = float(wind_input)
            if wind < 0:
                print("Wind speed cannot be negative.")
                continue
            break
        except:
            print("Enter a valid number for wind speed.")

    # Temperature validation
    while True:
        temp_input = input("Enter temperature (°C): ").strip()
        try:
            temp = float(temp_input)
            break
        except:
            print("Enter a valid number for temperature.")

    # Humidity validation
    while True:
        hum_input = input("Enter humidity (%): ").strip()
        try:
            hum = float(hum_input)
            if hum < 0 or hum > 100:
                print("Humidity must be between 0 and 100%.")
                continue
            break
        except:
            print("Enter a valid number for humidity.")

    # Visibility validation
    while True:
        vis_input = input("Enter visibility (km): ").strip()
        try:
            vis = float(vis_input)
            if vis < 0:
                print("Visibility must be positive.")
                continue
            break
        except:
            print("Enter a valid number for visibility.")

    # Date validation - simple format check
    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()
        if len(date) == 10 and date[4] == "-" and date[7] == "-":
            break
        else:
            print("Invalid date format. Use YYYY-MM-DD.")

    # Evaluate takeoff clearance
    clearance = evaluate_clearance(wind, temp, hum, vis)

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO weather (wind_speed, temperature, humidity, visibility, date, clearance) VALUES (?, ?, ?, ?, ?, ?)",
            (wind, temp, hum, vis, date, clearance)
        )
        conn.commit()
        conn.close()

        print(f"\n Weather recorded successfully.")
        print(f"TAKEOFF CLEARANCE: {clearance}")

    except Exception as e:
        print("Database Error:", e)


# ------------------------------------------------------ #
# Record Viewing
# ------------------------------------------------------ #
def view_weather_logs():
    # Displays all weather logs.
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather")
        rows = cursor.fetchall()
        conn.close()

        if len(rows) == 0:
            print("No weather history found.")
        else:
            print("\nWeather History:")
            for row in rows:
                print(row)

    except Exception as e:
        print("Database Error:", e)


def view_clearance_status():
    # Displays only clearance related decisions.
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT date, wind_speed, visibility, clearance FROM weather")
        rows = cursor.fetchall()
        conn.close()

        if len(rows) == 0:
            print("No clearance records found.")
        else:
            print("\nClearance Summary:")
            for row in rows:
                print(row)

    except Exception as e:
        print("Database Error:", e)


# ------------------------------------------------------ #
# Weather Module Menu
# ------------------------------------------------------ #
def run_weather():
    # Runs the weather module menu.
    init_db()
    while True:
        print("\n---- Weather & Takeoff Clearance Module ----")
        print("1. Record Weather Data")
        print("2. View Weather Logs")
        print("3. View Clearance Results")
        print("4. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            record_weather()
        elif choice == '2':
            view_weather_logs()
        elif choice == '3':
            view_clearance_status()
        elif choice == '4':
            break
        else:
            print("Invalid input, try again.")