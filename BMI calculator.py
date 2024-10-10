import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Create a new Tkinter window
window = tk.Tk()
window.title("BMI Calculator")

# Define functions to handle BMI calculation, classification, and data storage
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = round(weight / (height ** 2), 2)
        
        # Categorize BMI value
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi <= 24.9:
            category = "Normal weight"
        elif 25 <= bmi <= 29.9:
            category = "Overweight"
        else:
            category = "Obesity"
        
        # Display results
        result_label.config(text=f"BMI: {bmi} ({category})")
        save_bmi(weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.")

def save_bmi(weight, height, bmi, category):
    # Save the data to SQLite database
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records 
                    (id INTEGER PRIMARY KEY, 
                    weight REAL, height REAL, 
                    bmi REAL, category TEXT, 
                    date TEXT)''')
    
    cursor.execute('''INSERT INTO bmi_records (weight, height, bmi, category, date) 
                    VALUES (?, ?, ?, ?, ?)''', (weight, height, bmi, category, datetime.now()))
    conn.commit()
    conn.close()

def show_history():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bmi_records")
    records = cursor.fetchall()
    conn.close()

    # Create a new window to show the history
    history_window = tk.Toplevel(window)
    history_window.title("BMI History")
    history_text = tk.Text(history_window, height=20, width=50)
    history_text.pack()

    for record in records:
        history_text.insert(tk.END, f"Date: {record[5]}, Weight: {record[1]}, Height: {record[2]}, "
                                    f"BMI: {record[3]}, Category: {record[4]}\n")

def show_trend():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, bmi FROM bmi_records")
    records = cursor.fetchall()
    conn.close()

    # Prepare data for plotting
    dates = [datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S.%f') for record in records]
    bmis = [record[1] for record in records]

    # Plot the BMI trend
    plt.figure(figsize=(8, 5))
    plt.plot(dates, bmis, marker='o')
    plt.title('BMI Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Set up labels and input fields
tk.Label(window, text="Weight (kg):").grid(row=0, column=0)
weight_entry = tk.Entry(window)
weight_entry.grid(row=0, column=1)

tk.Label(window, text="Height (m):").grid(row=1, column=0)
height_entry = tk.Entry(window)
height_entry.grid(row=1, column=1)

# Buttons to calculate BMI, show history, and show trend
calculate_button = tk.Button(window, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=2, column=0, columnspan=2)

history_button = tk.Button(window, text="View History", command=show_history)
history_button.grid(row=3, column=0, columnspan=2)

trend_button = tk.Button(window, text="View Trend", command=show_trend)
trend_button.grid(row=4, column=0, columnspan=2)

# Result label
result_label = tk.Label(window, text="Your BMI will appear here.")
result_label.grid(row=5, column=0, columnspan=2)

# Run the application
window.mainloop()
