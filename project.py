import sys
import csv
import os
import matplotlib.pyplot as plt

HISTORY_FILE = "health_history.csv"


# ---------- INPUT HANDLING ----------
def get_user_input():
    print("--- Health Calculator CLI ---")

    try:
        weight = float(input("Enter weight in kg: "))
        height = float(input("Enter height in meters: "))
        age = int(input("Enter age in years: "))

        gender = input("Enter gender (M/F): ").upper()
        if gender not in ["M", "F"]:
            raise ValueError("Gender must be M or F")

        print("\nChoose Activity Level:")
        print("1. Sedentary")
        print("2. Light")
        print("3. Moderate")
        print("4. Very Active")
        print("5. Extra Active")

        choices = {
            "1": "Sedentary",
            "2": "Light",
            "3": "Moderate",
            "4": "Very Active",
            "5": "Extra Active"
        }

        activity_choice = input("Enter option number (1-5): ")
        activity = choices.get(activity_choice, "Sedentary")

        return weight, height, age, gender, activity

    except ValueError as e:
        print(f"Input error: {e}")
        sys.exit(1)


# ---------- CALCULATIONS ----------
def calculate_bmi(weight_kg, height_m):
    if height_m <= 0:
        return None
    return round(weight_kg / (height_m ** 2), 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"


def calculate_bmr(weight, height, age, gender):
    height_cm = height * 100

    if gender == 'M':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height_cm) - (4.330 * age)

    return round(bmr, 2)


def calculate_tdee(bmr, activity):
    mult = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    return round(bmr * mult.get(activity, 1.2), 2)


# ---------- HISTORY LOGGING ----------
def save_to_history(weight, height, age, bmi, bmr, tdee):
    file_exists = os.path.isfile(HISTORY_FILE)

    with open(HISTORY_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Weight", "Height", "Age", "BMI", "BMR", "TDEE"])

        writer.writerow([weight, height, age, bmi, bmr, tdee])


def load_history():
    if not os.path.isfile(HISTORY_FILE):
        print("No history found.")
        return None

    data = []
    with open(HISTORY_FILE, newline="") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            data.append([float(x) for x in row])

    return data


# ---------- GRAPH FEATURES ----------
def show_graphs(bmi, bmr, tdee):
    labels = ["BMI", "BMR", "TDEE"]
    values = [bmi, bmr, tdee]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, values)
    plt.title("Your Health Metrics")
    plt.ylabel("Value")
    plt.show()


def show_history_graph():
    data = load_history()
    if not data:
        return

    bmi_values = [row[3] for row in data]
    tdee_values = [row[5] for row in data]

    plt.figure(figsize=(8, 5))
    plt.plot(bmi_values, marker='o', label="BMI")
    plt.plot(tdee_values, marker='s', label="TDEE")
    plt.title("Progress Over Time")
    plt.xlabel("Entries")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.show()


# ---------- MAIN ----------
def main():
    weight, height, age, gender, activity = get_user_input()

    bmi = calculate_bmi(weight, height)
    bmi_category = classify_bmi(bmi)
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity)

    print("\n--- RESULTS ---")
    print(f"BMI: {bmi} ({bmi_category})")
    print(f"BMR: {bmr} cal/day")
    print(f"TDEE: {tdee} cal/day")

    save_to_history(weight, height, age, bmi, bmr, tdee)

    print("\nDisplaying Graphs...")
    show_graphs(bmi, bmr, tdee)

    print("Showing History Trend...")
    show_history_graph()


if __name__ == "__main__":
    main()