# Vityrathi_Project_FOSS
# FOSS -> Flight Operational Support Suite

A Python-based collection of tools to assist with basic flight ground operations.  
The system provides three main modules:

1. **Aircraft Maintenance Management**
2. **Weather & Takeoff Clearance Evaluation**
3. **Fuel & Flight Range Estimation**

All modules are implemented in Python with SQLite databases for persistent storage.

---

## 1. Features

### Module 1: Aircraft Maintenance System
- Register aircraft with name, model, and manufacture year
- Log maintenance events with date, engineer, cost, and status
- View all aircraft
- View all maintenance records
- View maintenance records for a specific aircraft
- Search aircraft by name or model

### Module 2: Weather & Takeoff Module
- Record weather conditions (wind speed, temperature, humidity, visibility)
- Automatically evaluate takeoff clearance based on safety thresholds
- View full weather history
- View summarized clearance decisions

### Module 3: Fuel & Range Module
- Input fuel onboard, burn rate, and cruising speed
- Estimate flight range using a simple endurance model
- Store and view history of range calculations

---

## 2. Technologies Used

- **Language:** Python 3
- **Database:** SQLite (via Python's built-in `sqlite3` module)
- **Editor:** Visual Studio Code
- **OS:** Windows

---

## 3. Project Structure

```text
Vityrathi_Project_FOSS/
│
├── main.py               # Main menu controller
├── maintenance.py        # Aircraft maintenance module
├── weather.py            # Weather and clearance module
├── fuel_calc.py          # Fuel & range module
│
├── databases/
│   ├── maintenance.db    # SQLite DB for maintenance data
│   ├── weather.db        # SQLite DB for weather data
│   └── fuel.db           # SQLite DB for fuel & range data
│
├── README.md
└── statement.md
```

## 4. Steps to install & run the project

- Make sure Python 3 is installed.
- Clone or download this repository to your computer.
- Open a terminal in the project folder.
- Run:
  `main.py`
- Use the menu to choose:
    > Aircraft Maintenance
    > Weather & Takeoff Evaluation
    > Fuel & Range Estimation

## 5. Testing Instructions

1. Run the application using:
   > `main.py`

2. Use the main menu to test each feature:
- **1 — Maintenance Module:** Add aircraft, search aircraft, and record maintenance.
- **2 — Weather Module:** Input weather parameters and check takeoff clearance.
- **3 — Fuel Module:** Enter fuel, burn rate, and speed to calculate flight range.

3. Enter valid numeric inputs where required.  
If invalid input is provided, the program will request the user to re-enter the data.

4. After running any operations, the database files:
   > maintenance.db
   > weather.db
   > fuel.db
will be created inside the `databases` directory and will retain stored records.

5. You can close and re-run the program — previous data will remain saved.

6. Select:
  > 4 — Exit
  to safely terminate the program.

