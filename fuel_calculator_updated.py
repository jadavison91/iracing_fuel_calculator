import math
import tkinter as tk
from tkinter import messagebox

print("Starting script...")

root = tk.Tk()
root.title("Sim Racing Stint Calculator")

def convert_time_to_seconds(time_str, is_race_duration=False):
    """
    Convert time in HH:MM or MM:SS format to total seconds.

    Parameters:
        time_str (str): Time in HH:MM or MM:SS format.
        is_race_duration (bool): Whether the input represents the race duration (HH:MM).

    Returns:
        int: Time in seconds.
    """
    try:
        parts = list(map(int, time_str.split(":")))
        if is_race_duration:  # Expect HH:MM format
            if len(parts) == 2:
                hours, minutes = parts
                return hours * 3600 + minutes * 60
            else:
                raise ValueError("Invalid time format for race duration. Use HH:MM.")
        else:  # Expect MM:SS format for lap time
            if len(parts) == 2:
                minutes, seconds = parts
                return minutes * 60 + seconds
            else:
                raise ValueError("Invalid time format for lap time. Use MM:SS.")
    except ValueError:
        raise ValueError("Invalid time format. Use HH:MM for race duration or MM:SS for lap time.")

def format_seconds_to_minutes_seconds(seconds):
    """
    Convert total seconds to MM:SS format.

    Parameters:
        seconds (int): Time in seconds.

    Returns:
        str: Time in MM:SS format.
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02}"

def format_seconds_to_hours_minutes(seconds):
    """
    Convert total seconds to HH:MM format.

    Parameters:
        seconds (int): Time in seconds.

    Returns:
        str: Time in HH:MM format.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}:{minutes:02}"

def calculate_fuel_for_race():
    """
    Calculate the fuel needed for a race based on race length, average lap time, and fuel consumption.
    Display the results on the main page.
    """
    try:
        # Get inputs
        race_distance_seconds = convert_time_to_seconds(entry_race_distance.get(), is_race_duration=True)
        average_lap_time_seconds = convert_time_to_seconds(entry_lap_time.get())
        fuel_consumption_per_lap = float(entry_fuel_consumption.get())

        # Validate inputs
        if race_distance_seconds <= 0 or average_lap_time_seconds <= 0 or fuel_consumption_per_lap <= 0:
            raise ValueError("All inputs must be positive numbers.")

        # Calculate total laps and fuel needed
        total_laps = math.ceil(race_distance_seconds / average_lap_time_seconds)
        total_fuel_needed = total_laps * fuel_consumption_per_lap
        total_time = total_laps * average_lap_time_seconds

        # Adjust to ensure the total time is greater than race length but less than 1 lap over
        while total_time > race_distance_seconds + average_lap_time_seconds:
            total_laps -= 1
            total_fuel_needed = total_laps * fuel_consumption_per_lap
            total_time = total_laps * average_lap_time_seconds

        # Display results
        result_laps_label.config(text=f"Total Laps: {total_laps}")
        result_fuel_label.config(text=f"Fuel Needed: {total_fuel_needed:.2f} liters")
        result_time_label.config(text=f"Total Time: {format_seconds_to_minutes_seconds(total_time)}")

    except ValueError as e:
        messagebox.showerror("Input Error", f"Error: {e}")


def calculate_stints(race_distance_seconds, average_lap_time_seconds, fuel_values, fuel_consumption_per_lap, car_fuel_capacity):
    """
    Recalculate stints dynamically based on provided fuel values.

    Parameters:
        race_distance_seconds (int): Total race duration in seconds.
        average_lap_time_seconds (float): Average lap time in seconds.
        fuel_values (list): List of fuel values for each stint.
        fuel_consumption_per_lap (float): Fuel consumption per lap in liters.
        car_fuel_capacity (float): Maximum fuel capacity of the car in liters.

    Returns:
        list: Updated stint data with laps, fuel, and time per stint.
    """
    remaining_laps = math.ceil(race_distance_seconds / average_lap_time_seconds)
    cumulative_time = 0
    new_stints = []

    for fuel in fuel_values:
        if remaining_laps <= 0:
            break

        # Calculate the number of laps for this stint based on the available fuel
        laps_this_stint = min(math.floor(fuel / fuel_consumption_per_lap), remaining_laps)
        stint_fuel = laps_this_stint * fuel_consumption_per_lap  # Exact fuel needed for this stint
        stint_time = laps_this_stint * average_lap_time_seconds
        cumulative_time += stint_time
        remaining_laps -= laps_this_stint

        new_stints.append({
            "stint_laps": laps_this_stint,
            "stint_time": stint_time,
            "cumulative_time": cumulative_time,
            "stint_fuel": stint_fuel
        })

    # Add new stints dynamically if needed
    while remaining_laps > 0:
        laps_this_stint = min(math.floor(car_fuel_capacity / fuel_consumption_per_lap), remaining_laps)
        stint_fuel = laps_this_stint * fuel_consumption_per_lap
        stint_time = laps_this_stint * average_lap_time_seconds
        cumulative_time += stint_time
        remaining_laps -= laps_this_stint

        new_stints.append({
            "stint_laps": laps_this_stint,
            "stint_time": stint_time,
            "cumulative_time": cumulative_time,
            "stint_fuel": stint_fuel
        })

    return new_stints

def recalculate(fuel_values, race_distance_seconds, average_lap_time_seconds, fuel_consumption_per_lap, car_fuel_capacity):
    """
    Recalculate stints dynamically based on updated fuel values.

    Parameters:
        fuel_values (list): Updated fuel values for recalculating stints.
        race_distance_seconds (int): Total race duration in seconds.
        average_lap_time_seconds (float): Average lap time in seconds.
        fuel_consumption_per_lap (float): Fuel consumption per lap in liters.
        car_fuel_capacity (float): Maximum fuel capacity of the car in liters.

    Returns:
        list: Updated stint data with laps, fuel, and time per stint.
    """
    remaining_laps = math.ceil(race_distance_seconds / average_lap_time_seconds)
    cumulative_time = 0
    new_stints = []

    # Process each stint based on the provided fuel values
    for i, fuel in enumerate(fuel_values):
        if remaining_laps <= 0:
            break

        # Ensure fuel does not exceed car fuel capacity
        fuel = min(fuel, car_fuel_capacity)

        # Calculate laps and time for this stint based on the available fuel
        laps_this_stint = min(math.floor(fuel / fuel_consumption_per_lap), remaining_laps)
        stint_time = laps_this_stint * average_lap_time_seconds
        stint_fuel = laps_this_stint * fuel_consumption_per_lap
        cumulative_time += stint_time
        remaining_laps -= laps_this_stint

        # Append the recalculated stint
        new_stints.append({
            "stint_laps": laps_this_stint,
            "stint_time": stint_time,
            "cumulative_time": cumulative_time,
            "stint_fuel": stint_fuel,
        })

        # Redistribute leftover fuel to the next stint, ensuring it does not exceed the car's capacity
        leftover_fuel = fuel - stint_fuel
        if leftover_fuel > 0 and i + 1 < len(fuel_values):
            fuel_values[i + 1] = min(fuel_values[i + 1] + leftover_fuel, car_fuel_capacity)

    # Add dynamically created stints for remaining laps
    while remaining_laps > 0:
        laps_this_stint = min(math.floor(car_fuel_capacity / fuel_consumption_per_lap), remaining_laps)
        stint_time = laps_this_stint * average_lap_time_seconds
        stint_fuel = laps_this_stint * fuel_consumption_per_lap
        cumulative_time += stint_time
        remaining_laps -= laps_this_stint

        new_stints.append({
            "stint_laps": laps_this_stint,
            "stint_time": stint_time,
            "cumulative_time": cumulative_time,
            "stint_fuel": stint_fuel,
        })

    return new_stints


def modify_stint_window(selected_stint, fuel_values):
    """
    Open a secondary window to modify a specific stint.

    Parameters:
        selected_stint (int): Index of the stint to modify.
        fuel_values (list): Current fuel values for each stint.
    """
    modify_window = tk.Toplevel(root)
    modify_window.title(f"Modify Stint {selected_stint + 1}")

    tk.Label(modify_window, text=f"Current Fuel for Stint {selected_stint + 1}: {fuel_values[selected_stint]:.2f} liters").pack(padx=10, pady=5)

    fuel_entry = tk.Entry(modify_window, width=10)
    fuel_entry.insert(0, f"{fuel_values[selected_stint]:.2f}")
    fuel_entry.pack(padx=10, pady=5)

    def save_changes():
        try:
            # Get the updated fuel value
            new_fuel = float(fuel_entry.get())
            fuel_values[selected_stint] = new_fuel

            # Recalculate and rebuild the analysis window
            rebuild_analysis_window(fuel_values)
            modify_window.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid fuel value.")

    tk.Button(modify_window, text="Save Changes", command=save_changes).pack(pady=10)

def rebuild_analysis_window(fuel_values):
    """
    Kill the analysis window and rebuild it dynamically.

    Parameters:
        fuel_values (list): List of updated fuel values for recalculating stints.
    """
    try:
        race_distance_seconds = convert_time_to_seconds(entry_race_distance.get(), is_race_duration=True)
        average_lap_time_seconds = convert_time_to_seconds(entry_lap_time.get())
        car_fuel_capacity = float(entry_fuel_capacity.get())
        fuel_consumption_per_lap = float(entry_fuel_consumption.get())

        # Recalculate stints
        stints = recalculate(fuel_values, race_distance_seconds, average_lap_time_seconds, fuel_consumption_per_lap, car_fuel_capacity)

        # Clear the analysis window
        for widget in analysis_window.winfo_children():
            widget.destroy()

        tk.Label(analysis_window, text=f"Capacity: {car_fuel_capacity:.2f} liters").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(analysis_window, text=f"Consumption: {fuel_consumption_per_lap:.2f} liters").grid(row=0, column=1, padx=10, pady=5, sticky="w")

        for i, stint in enumerate(stints):
            tk.Label(analysis_window, text=f"Stint {i + 1}:").grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")
            tk.Label(analysis_window, text=f"Laps: {stint['stint_laps']}, Time: {format_seconds_to_minutes_seconds(stint['stint_time'])}, Fuel: {stint['stint_fuel']:.2f} liters").grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")

        # Add modification buttons
        def handle_modify(selected_stint):
            modify_stint_window(selected_stint, fuel_values)

        for i in range(len(stints)):
            tk.Button(analysis_window, text=f"Modify Stint {i + 1}", command=lambda i=i: handle_modify(i)).grid(row=i + 1, column=2, padx=10, pady=5)

        tk.Button(analysis_window, text="Recalculate", command=lambda: rebuild_analysis_window(fuel_values)).grid(row=len(stints) + 1, column=0, columnspan=3, pady=10)

    except ValueError as e:
        messagebox.showerror("Input Error", f"Error: {e}")

def analyze_strategy():
    """
    Open the analysis window and initialize fuel values with dynamic calculation.
    """
    global analysis_window
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Race Strategy Analysis")

    car_fuel_capacity = float(entry_fuel_capacity.get())
    race_distance_seconds = convert_time_to_seconds(entry_race_distance.get(), is_race_duration=True)
    fuel_consumption_per_lap = float(entry_fuel_consumption.get())

    # Initialize stints with full fuel capacity
    initial_fuel_values = [car_fuel_capacity] * math.ceil(race_distance_seconds / (car_fuel_capacity / fuel_consumption_per_lap))
    rebuild_analysis_window(initial_fuel_values)


tk.Label(root, text="Race Distance (HH:MM):").grid(row=0, column=0, padx=10, pady=5)
entry_race_distance = tk.Entry(root)
entry_race_distance.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Average Lap Time (MM:SS):").grid(row=1, column=0, padx=10, pady=5)
entry_lap_time = tk.Entry(root)
entry_lap_time.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Car Fuel Capacity (liters):").grid(row=2, column=0, padx=10, pady=5)
entry_fuel_capacity = tk.Entry(root)
entry_fuel_capacity.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Fuel Consumption per Lap (liters):").grid(row=3, column=0, padx=10, pady=5)
entry_fuel_consumption = tk.Entry(root)
entry_fuel_consumption.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Analysis", command=analyze_strategy).grid(row=4, column=0, padx=10, pady=10, sticky="w")
tk.Button(root, text="Calculate Fuel", command=calculate_fuel_for_race).grid(row=4, column=1, padx=10, pady=10, sticky="e")

# Add labels for displaying results on the main page
result_laps_label = tk.Label(root, text="Total Laps: ")
result_laps_label.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

result_fuel_label = tk.Label(root, text="Fuel Needed: ")
result_fuel_label.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

result_time_label = tk.Label(root, text="Total Time: ")
result_time_label.grid(row=7, column=0, columnspan=2, pady=5, sticky="w")

root.mainloop()
