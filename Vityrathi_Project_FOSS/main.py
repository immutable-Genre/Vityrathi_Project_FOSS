"""
Main controller for Flight Operational Support Suite
"""

from maintenance import run_maintenance
from weather import run_weather
from fuel_calc import run_fuel_calc


def main():
    #Main menu for the entire system.
    while True:
        print("\n===== Flight Operational Tools Suite =====")
        print("1. Aircraft Maintenance System")
        print("2. Weather Takeoff Evaluation")
        print("3. Fuel & Flight Range Estimation")
        print("4. Exit")

        # Input validation loop
        choice = input("Enter choice (1-4): ").strip()

        # Only allow digits
        if not choice.isdigit():
            print("Please enter a number between 1-4.")
            continue

        # Convert input into integer
        choice = int(choice)

        # Menu routing with validation
        if choice == 1:
            try:
                run_maintenance()
            except Exception as e:
                print(f"Error running maintenance module: {e}")

        elif choice == 2:
            try:
                run_weather()
            except Exception as e:
                print(f"Error running weather module: {e}")

        elif choice == 3:
            try:
                run_fuel_calc()
            except Exception as e:
                print(f"Error running fuel module: {e}")

        elif choice == 4:
            print("Exiting program.... Goodbye!")
            break

        else:
            print("Invalid choice. Enter a number between 1-4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated manually by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")