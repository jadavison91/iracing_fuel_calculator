Sim Racing Fuel Calculator
The Sim Racing Fuel Calculator is a Python-based tool designed to assist sim racers in optimizing their fuel strategies during races. The application provides a 
user-friendly interface for calculating fuel requirements, analyzing race stints, and planning strategies for both short and endurance races.

This tool is ideal for racers looking to fine-tune their pit stop strategies and minimize unnecessary fuel weight during competitive racing.

Key Features

Fuel Requirement Calculation for Short Races: 
Enter race length, average lap time, and fuel consumption.
Automatically calculates: Total fuel needed. Total laps. Total race time (adjusted to ensure total time exceeds race length by less than one lap).

Dynamic Race Strategy Analysis:
Input race length, average lap time, fuel consumption, and maximum fuel capacity.
Calculates and displays: Total stints. Laps per stint. Fuel consumption per stint. Total cumulative race time. Dynamically adjusts stints if fuel is reduced for 
specific stints. 

Interactive Modification of Stints:
Modify specific stints through a dedicated modification window.
Automatically recalculates and redistributes laps and fuel across stints while ensuring fuel does not exceed the car's capacity.

Standalone Application:

The script has also been converted into a standalone executable file using PyInstaller, making it easy to use without requiring Python installation. The executable is 
located in the 'dist' folder.

Technologies Used
Python: Core programming language.
Tkinter: For the graphical user interface (GUI).
Math Module: For precise calculations of laps, fuel, and time.

How to Use
Clone or download the repository.
Install the required Python libraries (if running the script directly).

Run the script to:
Calculate fuel for short races.
Analyze and modify race strategies for endurance races.
