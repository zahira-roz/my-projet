import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import pandas as pd
import json
import os

# -------------------- Conversion Functions --------------------

# SQL to JSON
def sql_to_json(sql_file, table_name, output_file):
    try:
        conn = sqlite3.connect(sql_file)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        df.to_json(output_file, orient='records', indent=4)
        conn.close()
        messagebox.showinfo("Success", f"Table '{table_name}' converted to JSON successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# JSON to SQL
def json_to_sql(json_file, sql_file, table_name):
    try:
        df = pd.read_json(json_file)
        conn = sqlite3.connect(sql_file)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        messagebox.showinfo("Success", f"JSON converted to table '{table_name}' in SQL successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------- GUI --------------------

def browse_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_save_file(entry):
    filename = filedialog.asksaveasfilename(defaultextension=".json")
    entry.delete(0, tk.END)
    entry.insert(0, filename)

# Main window
root = tk.Tk()
root.title("SQL ↔ NoSQL Converter")
root.geometry("600x250")

# SQL → JSON
tk.Label(root, text="SQL File:").grid(row=0, column=0, padx=5, pady=5)
entry_sql_file = tk.Entry(root, width=40)
entry_sql_file.grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(entry_sql_file)).grid(row=0, column=2)

tk.Label(root, text="Table Name:").grid(row=1, column=0, padx=5, pady=5)
entry_table_sql = tk.Entry(root)
entry_table_sql.grid(row=1, column=1)

tk.Label(root, text="Save JSON as:").grid(row=2, column=0, padx=5, pady=5)
entry_json_save = tk.Entry(root, width=40)
entry_json_save.grid(row=2, column=1)
tk.Button(root, text="Choose Location", command=lambda: browse_save_file(entry_json_save)).grid(row=2, column=2)

tk.Button(root, text="Convert SQL → JSON", command=lambda: sql_to_json(entry_sql_file.get(), entry_table_sql.get(), entry_json_save.get())).grid(row=3, column=1, pady=10)

# JSON → SQL
tk.Label(root, text="JSON File:").grid(row=4, column=0, padx=5, pady=5)
entry_json_file = tk.Entry(root, width=40)
entry_json_file.grid(row=4, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(entry_json_file)).grid(row=4, column=2)

tk.Label(root, text="New SQL Table Name:").grid(row=5, column=0, padx=5, pady=5)
entry_table_json = tk.Entry(root)
entry_table_json.grid(row=5, column=1)

tk.Label(root, text="Save SQL as:").grid(row=6, column=0, padx=5, pady=5)
entry_sql_save = tk.Entry(root, width=40)
entry_sql_save.grid(row=6, column=1)
tk.Button(root, text="Choose Location", command=lambda: browse_save_file(entry_sql_save)).grid(row=6, column=2)

tk.Button(root, text="Convert JSON → SQL", command=lambda: json_to_sql(entry_json_file.get(), entry_sql_save.get(), entry_table_json.get())).grid(row=7, column=1, pady=10)

root.mainloop()
