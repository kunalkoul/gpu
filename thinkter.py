import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog
import subprocess

# Sample data for detection
sample_data = ["A1", "B1", "C1", "D1", "E1"]

def run_detection():
    # Update status
    status_label.config(text="Processing…")
    root.update_idletasks()

    # Get user input data
    user_data = user_input_entry.get()
    if not user_data:
        result_text.insert(tk.END, "Please enter data for detection.\n")
        status_label.config(text="Ready")
        return

    # Prepare input data for CUDA processing
    input_data = user_data.split(",")
    input_data = [value.strip() for value in input_data]  # Clean whitespace

    # Save input data to a temporary file or pass it as a command-line argument
    input_file_path = "input_data.txt"
    with open(input_file_path, 'w') as input_file:
        for item in input_data:
            input_file.write(f"{item}\n")

    # Run detection (pass input file to the CUDA executable)
    try:
        result = subprocess.run(["./malware_detection", input_file_path], capture_output=True, text=True)
        output = result.stdout
        # Replace matched signatures with the message
        output = output.replace("matched signature", "malware file is present")
        
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, output)
        status_label.config(text="Ready")
    except FileNotFoundError:
        result_text.insert(tk.END, "Error: 'malware_detection' binary not found.\n")
        status_label.config(text="Error")
    except Exception as e:
        result_text.insert(tk.END, f"Error running malware detection: {e}")
        status_label.config(text="Error")

def clear_input():
    user_input_entry.delete(0, tk.END)
    user_input_entry.insert(0, "Sample data: A, X, B, Y, C")

def clear_results():
    result_text.delete("1.0", tk.END)

def save_results():
    result = result_text.get("1.0", tk.END)
    if result.strip():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(result)

# Set up the main Tkinter window
root = tk.Tk()
root.title("Malware Detection UI")
root.geometry("600x550")

# Create notebook and Detection tab
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

detection_tab = tk.Frame(notebook)
notebook.add(detection_tab, text="Detection")

# Title label
title_label = tk.Label(detection_tab, text="CUDA-based Malware Detection", font=("Arial", 14))
title_label.pack(pady=10)

# Status indicator
status_label = tk.Label(detection_tab, text="Ready", font=("Arial", 10), fg="green")
status_label.pack(pady=5)

# User input for detection data with a sample input
user_input_label = tk.Label(detection_tab, text="Enter Data for Detection:", font=("Arial", 12))
user_input_label.pack(pady=5)

user_input_entry = tk.Entry(detection_tab, width=50, font=("Arial", 12))
user_input_entry.pack(pady=5)
user_input_entry.insert(0, "Sample data: A, X, B, Y, C")

# Sample data dropdown (single sample entry)
sample_var = tk.StringVar()
sample_var.set("Sample data: " + ", ".join(sample_data))  # Single default sample

def update_sample(*args):
    user_input_entry.delete(0, tk.END)
    user_input_entry.insert(0, sample_var.get())

sample_var.trace("w", update_sample)
sample_dropdown = tk.OptionMenu(detection_tab, sample_var, "Sample data: " + ", ".join(sample_data))
sample_dropdown.pack(pady=5)

# Buttons to run detection, clear input, and clear results
button_frame = tk.Frame(detection_tab)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Run Malware Detection", command=run_detection, font=("Arial", 12))
start_button.grid(row=0, column=0, padx=5)

clear_input_button = tk.Button(button_frame, text="Clear Input", command=clear_input, font=("Arial", 12))
clear_input_button.grid(row=0, column=1, padx=5)

clear_results_button = tk.Button(button_frame, text="Clear Results", command=clear_results, font=("Arial", 12))
clear_results_button.grid(row=0, column=2, padx=5)

# Button to save results to file
save_button = tk.Button(detection_tab, text="Save Results", command=save_results, font=("Arial", 12))
save_button.pack(pady=5)

# ScrolledText widget to display results
result_text = scrolledtext.ScrolledText(detection_tab, width=70, height=15, wrap=tk.WORD)
result_text.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()